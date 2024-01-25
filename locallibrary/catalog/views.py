from django.shortcuts import render
from .models import Author, Book, BookInstance, Genre
from django.views import generic


def index(request):
    """View function for home page of site."""
    
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()
    num_mindbooks = Book.objects.filter(title__icontains='mind').count()
    
    context = {
        'books' : num_books,
        'instances' : num_instances,
        'available' : num_instances_available,
        'authors' : num_authors,
        'genres' : num_genres,
        'mindbooks' : num_mindbooks,
    }
    
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book


