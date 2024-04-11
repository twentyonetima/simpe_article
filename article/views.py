from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from article.dictionary_with_tag import dict_with_tag
from article.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dct = dict_with_tag()
        context['release'] = dct['release']  # Assigning the release value to the context
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.kwargs['pk'])


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_form.html'
    fields = ['title', 'content']


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'article_form.html'
    fields = ['title', 'content', 'markdown_content']


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('article_list')
