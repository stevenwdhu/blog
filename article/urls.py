from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    # path('about', views.about_view, name='about'),
    # path('', list_view, name='article-list'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('create/', views.ArticleCreateView.as_view(), name='article-create'),
    path('<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('<int:pk>/like', views.IncreaseLikesView.as_view(), name='article-like'),

]
