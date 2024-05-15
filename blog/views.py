from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, FormMixin
from django.views.generic import ListView, DetailView

from .forms import CreateUserForm, CreateBlogForm, CreateCommentForm
from .models import Blog, Author, Comment

# TODO: Add all blog written by the author on the authors page


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


class BlogDetailView(FormMixin, DetailView):
    model = Blog
    form_class = CreateCommentForm

    def get_success_url(self):
        return reverse("blog:blog-detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context["form"] = CreateCommentForm(
            initial={"blog": self.object.id, "creator": self.request.user}
        )
        return context

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        new_comment = Comment.objects.create(
            creator=self.request.user,
            blog=self.get_object(),
            content=form.cleaned_data["content"],
        )
        new_comment.save()
        return super(BlogDetailView, self).form_valid(form)


class AuthorListView(ListView):
    model = Author
    context_object_name = "authors"
    template_name = "blog/authors.html"


class AuthorDetailView(DetailView):
    model = Author
