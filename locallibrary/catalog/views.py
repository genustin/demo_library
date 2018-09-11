# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Owner, BookInstance, Genre

# homepage
def index(request):
    """View function for home page of site."""

    print "==debug: visit index=="
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_books_word = Book.objects.filter(title__contains='H').count()
    
    # Available books (status = 'a')
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_owners = Owner.objects.count()
    num_genres = Genre.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    print request.session

    context = {
        'num_books': num_books,
        'num_books_word' : num_books_word,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_owners': num_owners,
        'num_genres' : num_genres, 
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class OwnerListView(generic.ListView):
    model = Owner
    paginate_by = 10

class OwnerDetailView(generic.DetailView):
    model = Owner


# check loan book instance 
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksListView(LoginRequiredMixin, generic.ListView):
    """view listing all the loaned books for library admin."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_loaned.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm
from catalog.forms import RenewBookModelForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    print "==debug: visit book renew=="
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        # book_renewal_form = RenewBookForm(request.POST)
        book_renewal_form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if book_renewal_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.due_back = book_renewal_form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-loaned') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        book_renewal_form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

# 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'owner', 'summary', 'isbn', 'genre']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

class BookInstCreate(CreateView):
    model = BookInstance
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookInstUpdate(UpdateView):
    model = BookInstance
    fields = ['status', 'borrower', 'due_back']
    success_url = reverse_lazy('my-borrowed')

class OwnerCreate(CreateView):
    model = Owner
    fields = '__all__'

class OwnerUpdate(UpdateView):
    model = Owner
    fields = ['name', 'date_of_join']

class OwnerDelete(DeleteView):
    model = Owner
    success_url = reverse_lazy('owners')

# author is not important yet
from catalog.models import Author
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
