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
    
    # Number of visits to this view
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'books' : num_books,
        'instances' : num_instances,
        'available' : num_instances_available,
        'authors' : num_authors,
        'genres' : num_genres,
        'mindbooks' : num_mindbooks,
        'visits' : num_visits,
    }
    
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 6


class BookDetailView(generic.DetailView):
    model = Book


class AuthorsListView(generic.ListView):
    model = Author
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = Author

