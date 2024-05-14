from django.contrib import admin

from .models import Blog, User, Author, Comment


class BlogInline(admin.TabularInline):
    model = Blog
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("user", "writes_since")
    inlines = [BlogInline]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Blog)
admin.site.register(User)
admin.site.register(Comment)
