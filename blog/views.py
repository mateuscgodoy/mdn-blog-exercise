from django.shortcuts import render
from django.http import HttpRequest


def index(request: HttpRequest):
    if request.method == "GET":
        return render(request, "blog/index.html")
