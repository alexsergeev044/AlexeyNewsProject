from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory, Subscriber, Mailing


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(post_rating=0)
    nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице
    list_display = [field.name for field in Post._meta.get_fields() if field.name != "post_category" and
                    field.name != "postcategory" and field.name != "comment" and field.name != "mailings"]
    list_filter = ['post_author', 'post_type', 'post_date']
    search_fields = ['post_title', 'post_text']
    actions = [nullfy_rating]


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Subscriber)
admin.site.register(Mailing)