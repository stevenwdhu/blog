from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy

from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment
from blog.custom_mixin import CustomFormMixin

# generic view
from django.views import generic


class PostComment(CustomFormMixin, generic.edit.ModelFormMixin, generic.FormView):
    form_class = CommentForm
    invalid_reverse_url = reverse_lazy('article:article-detail')
    model = Comment
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.queryset = self.get_queryset()
        self.article_id = kwargs['article_id']
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = get_object_or_404(ArticlePost, id=self.article_id)
            new_comment.user = request.user
            
            # 二级回复
            if kwargs.get('parent_id'):
                parent_comment = self.queryset.get(pk=kwargs['parent_id'])
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().pk
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return JsonResponse({"status": "success",
                                     "new_comment_id": new_comment.id
                                     })
            
            new_comment.save()
            redirect_url = reverse('article:article-detail', args=[self.article_id]) + "#comment_" + new_comment.id
            return redirect(redirect_url)
        else:
            return self.form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        comment_form = self.get_form()
        context = {
            'comment_form': comment_form,
            'article_id': kwargs['article_id'],
            'parent_id': kwargs['parent_id']
            }
        return render(request, 'comment/reply.html', context)
    
    def get_success_url(self):
        reverse('article:article-detail', args=[self.article_id])


def post_comment(request, article_pk):
    article = get_object_or_404(ArticlePost, pk=article_pk)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
