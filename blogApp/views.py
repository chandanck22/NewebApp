from django.shortcuts import render, get_object_or_404
from .models import Article, Tag, Profile
from django.db.models import Q

# def home(request):
#     return render(request, 'index.html')

def home(request):
    featured = Article.articlemanager.filter(featured=True)[0:3]
    context = {
        'articles': featured
    }
    return render(request, 'index.html', context)

def article(request, article):
    article = get_object_or_404(Article, slug=article, status='published')
    context = {
        'article': article
    }
    return render(request, 'article.html', context)

def articles(request):
    # get query from request
    query = request.GET.get('query')
    if query == None:
        query = ''

    # article = Article.articlemanager.all()
    # search for query in headline, sub_headline, body
    articles = Article.articlemanager.filter(
        Q(headline__icontains=query) |
        Q(sub_headline__icontains=query) |
        Q(body__icontains=query)
    )

    tags = Tag.objects.all()

    context = {
        'articles': articles,
        'tags': tags,
    }

    return render(request, 'articles.html', context)