from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import View

from .forms import CreateUserForm


def index(request: HttpRequest):
    if request.method == "GET":
        return render(request, "blog/index.html")


# For reference: https://learndjango.com/tutorials/django-login-and-logout-tutorial
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
