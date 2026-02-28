from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Author, Book, Publisher, Reservation, GENRE_CHOICES
from .forms import RegisterForm


# page d'accueil
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


# liste des auteurs
def author_list(request):
    query = request.GET.get('q', '')
    authors = Author.objects.all()

    if query:
        authors = authors.filter(author__icontains=query)

    return render(request, 'catalogue/author_list.html', {
        'authors': authors,
        'query': query,
    })


# detail d'un auteur
def author_detail(request, pk):
    try:
        author = Author.objects.get(id=pk)
    except Author.DoesNotExist:
        messages.error(request, "Auteur introuvable.")
        return redirect('catalogue:author_list')

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


# detail d'un editeur
def publisher_detail(request, pk):
    try:
        publisher = Publisher.objects.get(id=pk)
    except Publisher.DoesNotExist:
        messages.error(request, "Editeur introuvable.")
        return redirect('catalogue:publisher_list')

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

    # recherche par titre ou par auteur
    if query:
        from django.db.models import Q  # import ici car j'avais oublie en haut
        books = books.filter(
            Q(title__icontains=query) | Q(author__author__icontains=query)
        )

    if genre:
        books = books.filter(genre=genre)

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

    # verifier si l'utilisateur a deja reserve ce livre
    user_has_reserved = False
    if request.user.is_authenticated:
        nb = Reservation.objects.filter(user=request.user, book=book).count()
        if nb > 0:
            user_has_reserved = True

    return render(request, 'catalogue/book_detail.html', {
        'book': book,
        'user_has_reserved': user_has_reserved,
    })


# reserver un livre
@login_required
def reserve_book(request, pk):
    book = get_object_or_404(Book, id=pk)

    # verifier que le livre est disponible
    if not book.available:
        messages.error(request, "Ce livre n'est pas disponible.")
        return redirect('catalogue:book_detail', pk=pk)

    # verifier que l'user n'a pas deja reserve ce livre
    deja_reserve = Reservation.objects.filter(user=request.user, book=book)
    if len(deja_reserve) > 0:
        messages.warning(request, "Vous avez deja reserve ce livre.")
        return redirect('catalogue:book_detail', pk=pk)

    # verifier le quota (max 5)
    nb_reservations = Reservation.objects.filter(user=request.user).count()
    if nb_reservations >= 5:
        messages.error(request, "Vous avez atteint la limite de 5 reservations.")
        return redirect('catalogue:book_detail', pk=pk)

    Reservation.objects.create(user=request.user, book=book)
    messages.success(request, '"' + book.title + '" a ete reserve !')
    return redirect('catalogue:my_reservations')


# annuler une reservation
@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, book__pk=pk, user=request.user)
    reservation.delete()
    messages.success(request, 'Reservation annulee.')
    return redirect('catalogue:my_reservations')


# mes reservations
@login_required
def my_reservations(request):
    # recuperer toutes les reservations de l'utilisateur connecte
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'catalogue/my_reservations.html', {
        'reservations': reservations,
    })


# inscription
def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalogue:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Bienvenue ' + user.username + ' !')
            return redirect('catalogue:home')
    else:
        form = RegisterForm()

    return render(request, 'catalogue/register.html', {'form': form})
