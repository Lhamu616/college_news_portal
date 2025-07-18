import django_filters
from .models import Article, Category

class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Search Title')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Filter by Category')

    class Meta:
        model = Article
        fields = ['title', 'category']
