from django.contrib import admin
from .models import Author, Book, Publisher, Reservation


# enregistrement des modeles dans l'interface admin de django

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'telephone']
    search_fields = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'year_born']
    search_fields = ['author']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'publisher', 'genre', 'available']
    list_filter = ['genre', 'available']
    search_fields = ['title', 'author__author']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'date_reserved']
    search_fields = ['user__username', 'book__title']
