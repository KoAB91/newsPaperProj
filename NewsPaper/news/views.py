from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_notifications
# Create your views here.


class PostListView(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class PostSearchView(ListView):
    model = Post
    ordering = '-date'
    template_name = 'post_search.html'
    context_object_name = 'post_search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'post_add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        send_notifications.delay(post.pk)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_add.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class CategoryListView(ListView):
    model = Category
    ordering = 'name'
    template_name = 'categories.html'
    context_object_name = 'categories'
    paginate_by = 10


class PostsByCategoryView(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['category']
        context['posts'] = Post.objects.filter(category=category.id)
        context['not_subscribed'] = self.request.user not in category.subscribers.all()
        return context


@login_required
def subscribe_me(request, **kwargs):
    user = request.user
    id = kwargs.get('pk')
    category = Category.objects.get(pk=id)
    # if not user in category.subscribers.all():
    #     subscription = UserCategory(user=user, category=category)
    #     subscription.save()
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей в категории'
    # return redirect('/news/categories/' + str(id))
    return render(request, 'subscribe.html', {'category': category, 'message': message})