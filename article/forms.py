from django import forms
from .models import ArticlePost


class ArticleForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ['title', 'image', 'column', 'tag', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.fields
        for field_name in fields:
            field = fields[field_name]
            field.label_suffix = ''
            field.widget.attrs.update({'class': 'form-control'})

        fields['image'].widget.attrs['class'] = 'form-control-file'
        # fields['image'].widget.initial_text = 'Current Image'
        fields['column'].widget.attrs['class'] += ' w-auto'
        fields['tag'].widget.attrs['class'] += ' w-auto'
        fields['body'].widget.attrs['rows'] = 15

