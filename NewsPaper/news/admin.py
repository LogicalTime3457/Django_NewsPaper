from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    fk_name = 'postThrough'
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInLine]
    list_display = ('author', 'title', 'dateCreation', 'rating')
    list_filter = ('author', 'title', 'dateCreation', 'rating')
    search_fields = ('author__authorUser__username', 'title', 'rating')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor',)
    list_filter = ('authorUser__username', 'ratingAuthor',)
    search_fields = ('authorUser__username', 'ratingAuthor',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

