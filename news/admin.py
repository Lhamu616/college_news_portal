from django.contrib import admin
from .models import Article, Category, Tag, Profile, Comment, Like, Reaction

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Reaction)