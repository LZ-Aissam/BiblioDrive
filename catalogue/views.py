from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Author, Book, Publisher, Reservation, GENRE_CHOICES
from .forms import RegisterForm


def home(request):
    nb_authors = Author.objects.count()
    nb_books = Book.objects.count()
    nb_publishers = Publisher.objects.count()
    return render(request, 'catalogue/home.html', {
        'nb_authors': nb_authors,
        'nb_books': nb_books,
        'nb_publishers': nb_publishers,
    })


def author_list(request):
    query = request.GET.get('q', '')
    authors = Author.objects.all()
    if query:
        authors = authors.filter(author__icontains=query)
    return render(request, 'catalogue/author_list.html', {
        'authors': authors,
        'query': query,
    })


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = author.books.select_related('publisher').all()
    return render(request, 'catalogue/author_detail.html', {
        'author': author,
        'books': books,
    })


def publisher_list(request):
    query = request.GET.get('q', '')
    publishers = Publisher.objects.all()
    if query:
        publishers = publishers.filter(
            Q(name__icontains=query) | Q(city__icontains=query)
        )
    return render(request, 'catalogue/publisher_list.html', {
        'publishers': publishers,
        'query': query,
    })


def publisher_detail(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    books = publisher.books.select_related('author').all()
    return render(request, 'catalogue/publisher_detail.html', {
        'publisher': publisher,
        'books': books,
    })


def book_list(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    availability = request.GET.get('disponible', '')
    publisher_id = request.GET.get('publisher', '')

    books = Book.objects.select_related('author', 'publisher').all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__author__icontains=query) |
            Q(isbn__icontains=query)
        )
    if genre:
        books = books.filter(genre=genre)
    if availability == '1':
        books = books.filter(available=True)
    elif availability == '0':
        books = books.filter(available=False)
    if publisher_id:
        books = books.filter(publisher__pk=publisher_id)

    publishers = Publisher.objects.all()
    return render(request, 'catalogue/book_list.html', {
        'books': books,
        'query': query,
        'selected_genre': genre,
        'selected_availability': availability,
        'selected_publisher': publisher_id,
        'genre_choices': GENRE_CHOICES,
        'publishers': publishers,
    })


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related('author', 'publisher'), pk=pk)
    user_has_reserved = False
    if request.user.is_authenticated:
        user_has_reserved = Reservation.objects.filter(user=request.user, book=book).exists()
    return render(request, 'catalogue/book_detail.html', {
        'book': book,
        'user_has_reserved': user_has_reserved,
    })


@login_required
def reserve_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.available:
        messages.error(request, "Ce livre n'est pas disponible a la reservation.")
        return redirect('catalogue:book_detail', pk=pk)
    if Reservation.objects.filter(user=request.user, book=book).exists():
        messages.warning(request, "Vous avez deja reserve ce livre.")
        return redirect('catalogue:book_detail', pk=pk)
    if Reservation.objects.filter(user=request.user).count() >= 5:
        messages.error(request, "Vous avez atteint la limite de 5 reservations simultanees.")
        return redirect('catalogue:book_detail', pk=pk)
    Reservation.objects.create(user=request.user, book=book)
    messages.success(request, f'"{book.title}" a ete reserve avec succes.')
    return redirect('catalogue:my_reservations')


@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, book__pk=pk, user=request.user)
    book_title = reservation.book.title
    reservation.delete()
    messages.success(request, f'La reservation de "{book_title}" a ete annulee.')
    return redirect('catalogue:my_reservations')


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(
        user=request.user
    ).select_related('book', 'book__author', 'book__publisher')
    return render(request, 'catalogue/my_reservations.html', {
        'reservations': reservations,
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalogue:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue, {user.username} ! Votre compte a ete cree.')
            return redirect('catalogue:home')
    else:
        form = RegisterForm()
    return render(request, 'catalogue/register.html', {'form': form})
