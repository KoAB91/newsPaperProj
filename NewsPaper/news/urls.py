from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostListView, PostDetail, PostSearchView, PostCreateView, PostUpdateView, PostDeleteView, \
    CategoryListView, PostsByCategoryView, subscribe_me

urlpatterns = [
    path('', cache_page(300)(PostListView.as_view())),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('add/', PostCreateView.as_view(), name='post_add'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('categories/', cache_page(30)(CategoryListView.as_view()), name='categories'),
    path('categories/<int:pk>', PostsByCategoryView.as_view(), name='category'),
    path('categories/subscribe/<int:pk>', subscribe_me, name='category_subscribe'),
]
