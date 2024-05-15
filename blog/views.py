from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView

from .forms import CreateUserForm, CreateBlogForm
from .models import Blog, Author


def index(request: HttpRequest):
    if request.method == "GET":
        return render(request, "blog/index.html")


# For reference: https://learndjango.com/tutorials/django-login-and-logout-tutorial
#! Not suited for this context, but good for learning
# class RegisterView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/register.html"

#     class Meta:
#         model = get_user_model()


class Register(View):
    def get(self, request):
        form = CreateUserForm()
        context = {"form": form}
        return render(request, "registration/register.html", context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        context = {"form": form}
        return render(request, "registration/register.html", context)


class BlogCreate(CreateView):
    model = Blog
    form_class = CreateBlogForm
    template_name = "blog/new.html"
    success_url = ""

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        form.instance.author = author
        form.save()
        #! TODO: Change it to Blog View once it's created
        return HttpResponseRedirect(reverse("blog:index"))


class BlogListView(ListView):
    model = Blog
    context_object_name = "blogs"
    template_name = "blog/blogs.html"


class BlogDetailView(DetailView):
    model = Blog


class AuthorListView(ListView):
    model = Author
    context_object_name = "authors"
    template_name = "blog/authors.html"


class AuthorDetailView(DetailView):
    model = Author
