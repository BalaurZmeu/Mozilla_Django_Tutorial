import datetime


from django.shortcuts import get_object_or_404, render
from .models import Author, Book, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from.django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

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
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorsListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class LoanedBooksLibrariansView(PermissionRequiredMixin, generic.ListView):
    """Class-based view listing books on loan only to librarians."""
    permission_required = ('catalog.can_mark_returned',)
    model = BookInstance
    template_name = 'catalog/bookinstance_list_librarians.html'
    paginate_by = 10
    
    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            
            return HttpResponseRedirect(reverse('all-borrowed'))
    
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    
    context = {
        'form': form,
        'book_instance': book_instance,
    }
    
    return render(request, 'catalog/book_renew_librarian.html', context)
