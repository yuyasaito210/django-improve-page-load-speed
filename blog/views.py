from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.core.paginator import Paginator
from blog.models import Post, SubscribeBlog
from bnboats_app.views import signin_signup_func, captain_setup

def index(request):
    if request.method == 'POST':
        if "email" in request.POST and request.POST['email'] != "":
            email = request.POST['email'] #request.POST.get('email', False)
            obj, created = SubscribeBlog.objects.get_or_create(email=email)
            if created:
                messages.add_message(request, messages.INFO, 'E-mail adicionado.')
            else:
                messages.add_message(request, messages.INFO, 'E-mail já cadastrado.')

    posts_list = Post.objects.published().order_by('-published_date')[2:]
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'newer_posts': Post.objects.published().order_by('-published_date')[:2],
        'posts': posts,
        'popular_posts': Post.objects.published().order_by('-hit', '-published_date')[:5],
    }

    context.update(signin_signup_func(request, context))

    # Check if user is an owner, prepare owner setup
    context.update(captain_setup(request))

    # if login was requested
    if 'signin' in request.GET and request.user.is_anonymous:
        context['signin'] = "True"
    else:
        if 'next' in request.GET:
            return redirect(request.GET['next'])

    return render(request, 'post/list.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.published().order_by('-hit', '-published_date')[:5]
        return context

    def get_object(self):
        obj = super().get_object()
        obj.hit = obj.hit + 1
        obj.save()
        return obj