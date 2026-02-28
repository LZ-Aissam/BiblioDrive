from django.db import models
from django.contrib.auth.models import User


# Modele pour les editeurs
# Champs repris depuis le modele relationnel du cahier des charges
class Publisher(models.Model):
    name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=10, blank=True)
    zip_code = models.CharField(max_length=15, blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name = "Editeur"
        verbose_name_plural = "Editeurs"
        ordering = ['name']

    # pour afficher le nom dans l'admin django
    def __str__(self):
        return self.name


# Modele auteur
class Author(models.Model):
    author = models.CharField(max_length=50, verbose_name="Nom de l'auteur")
    year_born = models.SmallIntegerField(verbose_name="Annee de naissance", null=True, blank=True)

    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"
        ordering = ['author']

    def __str__(self):
        return self.author


# Liste des genres disponibles pour les livres
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


# Modele principal : le livre
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    # un livre appartient a un auteur, si on supprime l'auteur ses livres sont supprimes aussi
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', verbose_name="Auteur")
    # l'editeur est optionnel (nullable)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books', verbose_name="Editeur")
    isbn = models.CharField(max_length=20, blank=True)
    summary = models.TextField(verbose_name="Resume", blank=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, verbose_name="Genre", default='roman')
    available = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        ordering = ['title']

    def __str__(self):
        return self.title


# Modele pour les reservations
# Un utilisateur peut avoir au maximum 5 reservations en meme temps
# source : cahier des charges section "Reserver un livre"
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    date_reserved = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        # empeche un user de reserver le meme livre 2 fois
        unique_together = ('user', 'book')
        ordering = ['-date_reserved']

    def __str__(self):
        return self.user.username + " - " + self.book.title
