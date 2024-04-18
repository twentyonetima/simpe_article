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
        article = self.get_object()
        first_key = next(iter(dct))
        modified_content = article.content.replace('{{ ' + first_key + ' }}', dct[f'{first_key}'])
        for key in dct:
            if key == first_key:
                continue
            else:
                modified_content = modified_content.replace('{{ ' + key + ' }}', dct[f'{key}'])
        context['modified_content'] = modified_content
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
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        article_content = self.object.content

        modified_content = self.modify_content(article_content)
        context['modified_content'] = modified_content
        with open("modified_content_update.txt", "w") as file:
            file.write("Context: {}\n Article_content: {}\n".format(context['modified_content'], article_content))
        return context

    def modify_content(self, content):
        dct = dict_with_tag()
        first_key = next(iter(dct))

        modified_content = content.replace('{{ ' + first_key + ' }}', dct[first_key])
        for key in dct:
            if key == first_key:
                continue
            else:
                modified_content = modified_content.replace('{{ ' + key + ' }}', dct[key])
        return modified_content


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('article_list')
