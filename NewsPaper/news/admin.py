from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment
from modeltranslation.admin import TranslationAdmin


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


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdminTranslate(TranslationAdmin):
    model = Post


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

