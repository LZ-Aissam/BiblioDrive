from django.contrib import admin
from .models import Author, Book, Publisher, Reservation


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'telephone')
    search_fields = ('name', 'city')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'year_born')
    search_fields = ('author',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publisher', 'genre', 'available')
    list_filter = ('genre', 'available', 'publisher')
    search_fields = ('title', 'author__author', 'isbn')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'date_reserved')
    list_filter = ('date_reserved',)
    search_fields = ('user__username', 'book__title')
