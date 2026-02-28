from django.db import models
from django.contrib.auth.models import User


class Publisher(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    company_name = models.CharField(max_length=255, verbose_name="Raison sociale", blank=True)
    address = models.CharField(max_length=50, verbose_name="Adresse", blank=True)
    city = models.CharField(max_length=20, verbose_name="Ville", blank=True)
    state = models.CharField(max_length=10, verbose_name="Region", blank=True)
    zip_code = models.CharField(max_length=15, verbose_name="Code postal", blank=True)
    telephone = models.CharField(max_length=15, verbose_name="Telephone", blank=True)
    fax = models.CharField(max_length=15, verbose_name="Fax", blank=True)
    comments = models.TextField(verbose_name="Commentaires", blank=True)

    class Meta:
        verbose_name = "Editeur"
        verbose_name_plural = "Editeurs"
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    author = models.CharField(max_length=50, verbose_name="Nom de l'auteur")
    year_born = models.SmallIntegerField(verbose_name="Annee de naissance", null=True, blank=True)

    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"
        ordering = ['author']

    def __str__(self):
        return self.author


GENRE_CHOICES = [
    ('roman', 'Roman'),
    ('policier', 'Policier'),
    ('sf', 'Science-Fiction'),
    ('fantasy', 'Fantasy'),
    ('historique', 'Historique'),
    ('biographie', 'Biographie'),
    ('essai', 'Essai'),
    ('poesie', 'Poesie'),
    ('theatre', 'Theatre'),
    ('jeunesse', 'Jeunesse'),
    ('bd', 'Bande dessinee'),
    ('autre', 'Autre'),
]


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', verbose_name="Auteur")
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books', verbose_name="Editeur")
    isbn = models.CharField(max_length=20, verbose_name="ISBN", blank=True)
    summary = models.TextField(verbose_name="Resume", blank=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, verbose_name="Genre", default='roman')
    available = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        ordering = ['title']

    def __str__(self):
        return self.title


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name="Utilisateur")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations', verbose_name="Livre")
    date_reserved = models.DateTimeField(auto_now_add=True, verbose_name="Date de reservation")

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        unique_together = ('user', 'book')
        ordering = ['-date_reserved']

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
