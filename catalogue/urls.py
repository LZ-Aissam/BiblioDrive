from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'catalogue'

urlpatterns = [
    path('', views.home, name='home'),

    # Auteurs
    path('auteurs/', views.author_list, name='author_list'),
    path('auteurs/<int:pk>/', views.author_detail, name='author_detail'),

    # Livres
    path('livres/', views.book_list, name='book_list'),
    path('livres/<int:pk>/', views.book_detail, name='book_detail'),
    path('livres/<int:pk>/reserver/', views.reserve_book, name='reserve_book'),
    path('livres/<int:pk>/annuler/', views.cancel_reservation, name='cancel_reservation'),

    # Editeurs
    path('editeurs/', views.publisher_list, name='publisher_list'),
    path('editeurs/<int:pk>/', views.publisher_detail, name='publisher_detail'),

    # Reservations
    path('mes-reservations/', views.my_reservations, name='my_reservations'),

    # Authentification
    path('connexion/', auth_views.LoginView.as_view(
        template_name='catalogue/login.html'
    ), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
    path('inscription/', views.register_view, name='register'),
    path('changer-mdp/', auth_views.PasswordChangeView.as_view(
        template_name='catalogue/change_password.html',
        success_url=reverse_lazy('catalogue:home')
    ), name='change_password'),
]
