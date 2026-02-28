from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .models import Author, Book, Publisher, Reservation, GENRE_CHOICES
from .forms import RegisterForm


# page d'accueil : affiche les stats generales
def home(request):
    nb_authors = Author.objects.count()
    nb_books = Book.objects.count()
    nb_publishers = Publisher.objects.count()

    context = {
        'nb_authors': nb_authors,
        'nb_books': nb_books,
        'nb_publishers': nb_publishers,
    }
    return render(request, 'catalogue/home.html', context)


# liste de tous les auteurs avec recherche par nom
def author_list(request):
    query = request.GET.get('q', '')
    authors = Author.objects.all()

    if query:
        authors = authors.filter(author__icontains=query)

    context = {
        'authors': authors,
        'query': query,
    }
    return render(request, 'catalogue/author_list.html', context)


# page detail d'un auteur avec la liste de ses livres
def author_detail(request, pk):
    author = Author.objects.get(id=pk)
    livres = author.books.all()

    return render(request, 'catalogue/author_detail.html', {
        'author': author,
        'books': livres,
    })


# liste des editeurs
def publisher_list(request):
    query = request.GET.get('q', '')
    publishers = Publisher.objects.all()

    if query:
        publishers = publishers.filter(name__icontains=query)

    return render(request, 'catalogue/publisher_list.html', {
        'publishers': publishers,
        'query': query,
    })


# detail d'un editeur avec ses livres
def publisher_detail(request, pk):
    publisher = Publisher.objects.get(id=pk)
    livres = publisher.books.all()

    return render(request, 'catalogue/publisher_detail.html', {
        'publisher': publisher,
        'books': livres,
    })


# liste des livres avec filtres
def book_list(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    availability = request.GET.get('disponible', '')
    publisher_id = request.GET.get('publisher', '')

    books = Book.objects.all()

    # filtre par titre
    if query:
        books = books.filter(title__icontains=query)

    if genre:
        books = books.filter(genre=genre)

    # disponible = 1, indisponible = 0
    if availability == '1':
        books = books.filter(available=True)
    elif availability == '0':
        books = books.filter(available=False)

    if publisher_id:
        books = books.filter(publisher__id=publisher_id)

    tous_editeurs = Publisher.objects.all()

    # print(books.query)  # debug

    return render(request, 'catalogue/book_list.html', {
        'books': books,
        'query': query,
        'selected_genre': genre,
        'selected_availability': availability,
        'selected_publisher': publisher_id,
        'genre_choices': GENRE_CHOICES,
        'publishers': tous_editeurs,
    })


# detail d'un livre
def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    book.author  # on accede a l'auteur pour l'afficher
    book.publisher  # idem pour l'editeur

    user_has_reserved = False
    if request.user.is_authenticated:
        nb = Reservation.objects.filter(user=request.user, book=book).count()
        if nb > 0:
            user_has_reserved = True

    return render(request, 'catalogue/book_detail.html', {
        'book': book,
        'user_has_reserved': user_has_reserved,
    })


# reserver un livre (utilisateur connecte seulement)
@login_required
def reserve_book(request, pk):
    book = get_object_or_404(Book, id=pk)

    # verifier que le livre est disponible
    if not book.available:
        messages.error(request, "Ce livre n'est pas disponible.")
        return redirect('catalogue:book_detail', pk=pk)

    # max 5 reservations par utilisateur (exigence fonctionnelle)
    nb_reservations = Reservation.objects.filter(user=request.user).count()
    if nb_reservations >= 5:
        messages.error(request, "Vous avez atteint la limite de 5 reservations.")
        return redirect('catalogue:book_detail', pk=pk)

    # creer la reservation
    Reservation.objects.create(user=request.user, book=book)
    messages.success(request, '"' + book.title + '" a ete reserve avec succes.')
    return redirect('catalogue:my_reservations')


# annuler une reservation
@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, book__pk=pk, user=request.user)
    titre = reservation.book.title
    reservation.delete()
    messages.success(request, 'Reservation annulee.')
    return redirect('catalogue:my_reservations')


# voir mes reservations en cours
@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'catalogue/my_reservations.html', {
        'reservations': reservations,
    })


# inscription d'un nouvel utilisateur
def register_view(request):
    # si deja connecte on redirige vers l'accueil
    if request.user.is_authenticated:
        return redirect('catalogue:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # connexion automatique apres inscription
            messages.success(request, 'Bienvenue ' + user.username + ' ! Compte cree avec succes.')
            return redirect('catalogue:home')
    else:
        form = RegisterForm()

    return render(request, 'catalogue/register.html', {'form': form})
