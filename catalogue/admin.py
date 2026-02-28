from django.contrib import admin
from .models import Author, Book, Publisher


# enregistrement des modeles dans l'interface admin de django

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'year_born']
    search_fields = ['author']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'genre', 'available']
    list_filter = ['genre', 'available']
