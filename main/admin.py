from django.contrib import admin

from main.models import Category, Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    max_num = 10
    min_num = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, ]


admin.site.register(Category)
# admin.site.register(Post)
# admin.site.register(PostImage)

