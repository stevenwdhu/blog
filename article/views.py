# urls and templates
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.core.paginator import Paginator
from django.db.models import Q

# exception
from django.core.exceptions import PermissionDenied

# generic view
from django.views import generic

# custom import
from .models import ArticlePost
from .forms import ArticleForm
from blog.custom_mixin import CustomFormMixin, CustomLoginRequiredMixin
from comment.models import Comment
from comment.forms import CommentForm

import markdown

md = markdown.Markdown(extensions=[
    # 包含 缩写、表格等常用扩展
    'markdown.extensions.extra',
    # 语法高亮扩展
    'markdown.extensions.codehilite',
    # Table of Content
    'markdown.extensions.toc'
])


# Create your views here.
class ArticleListView(generic.ListView):
    queryset = ArticlePost.objects.all()
    # context_object_name = 'list'
    template_name = 'article/list.html'
    paginate_by = 3
    ordering = '-create_time'
    URL_ARGS = {}
    
    def get_queryset(self):
        data = self.request.GET
        self.URL_ARGS = {}
        search = data.get('search')
        order = data.get('order')
        column_id = data.get('column_id')
        tag = data.get('tag')
        
        # get search
        if search:
            self.queryset = self.queryset.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
            self.URL_ARGS.update({'search': search})
        
        if order == 'hot':
            self.ordering = '-views'
            self.URL_ARGS.update({'order': order})
        
        if column_id and column_id.isdigit():
            self.queryset = self.queryset.filter(column_id=column_id)
            self.URL_ARGS.update({'column_id': column_id})
        
        if tag:
            self.queryset = self.queryset.filter(tag__name__iexact=tag)
            self.URL_ARGS.update({'tag': tag})
        
        self.extra_context = {'urlarg': self.URL_ARGS, 'search': search}
        
        return super().get_queryset()


class ArticleDetailView(generic.DetailView):
    context_object_name = 'article'
    model = ArticlePost
    template_name = 'article/detail.html'
    comment_form = CommentForm()
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        comments = Comment.objects.filter(article=self.object.pk)
        if self.request.session.get('viewed_article'):
            if self.object.pk not in self.request.session['viewed_article']:
                self.request.session['viewed_article'] += [self.object.pk]
                self.object.views += 1
                self.object.save(update_fields=['views'])
        else:
            self.request.session['viewed_article'] = [self.object.pk]
            self.object.views += 1
            self.object.save(update_fields=['views'])
        
        self.object.body = md.convert(self.object.body)
        self.extra_context = {'toc': md.toc, 'comments': comments, 'form': self.comment_form}
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ArticleCreateView(CustomLoginRequiredMixin, CustomFormMixin, generic.CreateView):
    # custom form mixin
    invalid_reverse_url = reverse_lazy('article:article-create')
    
    # create view
    model = ArticlePost
    template_name = 'article/create.html'
    form_class = ArticleForm
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        return redirect(self.get_success_url())


class ArticleUpdateView(CustomLoginRequiredMixin, CustomFormMixin, generic.UpdateView):
    # custom form mixin
    invalid_reverse_url = reverse_lazy('article:article-update')
    
    # update view
    context_object_name = 'article'
    model = ArticlePost
    form_class = ArticleForm
    template_name = 'article/update.html'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        return redirect(self.get_success_url())
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.author:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.author:
            raise PermissionDenied
        return super().post(request, *args, **kwargs)


class ArticleDeleteView(CustomLoginRequiredMixin, generic.DeleteView):
    # delete view
    model = ArticlePost
    success_url = reverse_lazy('article-list')
    
    def get(self, request, *args, **kwargs):
        raise PermissionDenied
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.author:
            raise PermissionDenied
        return super().post(request, *args, **kwargs)


class IncreaseLikesView(generic.base.View):
    def post(self, request, *args, **kwargs):
        article = get_object_or_404(ArticlePost, pk=kwargs.get('pk'))
        article.likes += 1
        article.save(update_fields=['likes'])
        return HttpResponse('success')
