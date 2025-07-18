from django.urls import path
from .views import ArticleUpdateView, CategoryViewDashboard, article_detail, home, dashboard, ArticleListView, ArticleAJAXView,ArticleDeleteView
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('article/', ArticleListView.as_view(), name='article-list'),
    path('ajax-articles/', ArticleAJAXView.as_view(), name='ajax-articles'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('articles/create/', views.create_article, name='create-article'),
    path('articles/<slug:slug>/',article_detail,name='article-detail'),
    path('articles/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article-edit'),

    path('articles/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article-delete'),

    path('category/create',views.create_category,name='create-category'),
    path('dashboard/category/', CategoryViewDashboard.as_view(),name='dashboard=category'),

]