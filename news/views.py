from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from rest_framework import serializers, viewsets
from django.utils.text import slugify
import datetime
from .models import Article, Category
from .forms import ArticleForm, CategoryForm
from .filters import ArticleFilter
from django.contrib.auth.models import User
from .tasks import send_article_mail
from django.contrib import messages


def home(request):
    articles = Article.objects.filter(status='published').order_by('-published_at')
    return render(request, 'home.html', {'articles': articles})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if not category.slug:
                category.slug = slugify(category.name)
            category.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

def dashboard(request):
    context = {
        'article_count': Article.objects.count(),
        'category_count': Category.objects.count(),
        'user_count': User.objects.count()
    }
    return render(request, 'dashboard.html', context)

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = Article.objects.filter(status='published').order_by('-published_at')
        self.filterset = ArticleFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class ArticleAJAXView(View):
    def get(self, request, *args, **kwargs):
        articles = list(Article.objects.filter(status='published').values())
        return JsonResponse(articles, safe=False)

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            if not article.slug:
                article.slug = slugify(article.title)
            if article.status == 'published' and not article.published_at:
                article.published_at = datetime.datetime.now()
            article.save()
            form.save_m2m()
            send_article_email.delay(article.title,article.slug)

            messages.success(request,'Article Created Successfully')

            return redirect('dashboard')
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'article_detail.html', {'article': article})

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'
    context_object_name = 'article'

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'slug': self.object.slug})

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_staff



class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    context_object_name = 'article'

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect to dashboard after delete

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_staff


class CategoryViewDashboard(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard_category.html'
    context_object_name = 'category'
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.all().order_by('name')

# --- urls.py ---
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('article/', views.ArticleListView.as_view(), name='article-list'),
    path('ajax-articles/', views.ArticleAJAXView.as_view(), name='ajax-articles'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('articles/create/', views.create_article, name='create-article'),
    path('articles/<slug:slug>/', views.article_detail, name='article-detail'),
    path('articles/<slug:slug>/edit/', views.ArticleUpdateView.as_view(), name='article-edit'),
    path('articles/<slug:slug>/delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('category/create/', views.create_category, name='create-category'),
    path('dashboard/category/', views.CategoryViewDashboard.as_view(), name='dashboard-category'),
]
