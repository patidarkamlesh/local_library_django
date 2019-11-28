from django.shortcuts import render, get_object_or_404
from .models import Book, BookInstance, Author
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RenewBookForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def index(request):
    # Count of books
    num_book = Book.objects.all().count()
    # Count of Book Instances
    num_book_instances = BookInstance.objects.all().count()
    # Count of Authors
    num_author = Author.objects.all().count()
    # Number of book available
    num_book_available = BookInstance.objects.filter(status__exact='a').count()
    # Book title contains first
    num_book_first = Book.objects.filter(title__icontains='first').count()
    # Horror Genre book
    #num_horror_genre = Book.genre.get(name__exact='Horror').count()
    # Number of time Home page visited
    num_home_visted = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_home_visted + 1
    context = {
        'num_book' : num_book,
        'num_book_instances' : num_book_instances,
        'num_author' : num_author,
        'num_book_available' : num_book_available,
        'num_book_first' : num_book_first,
        'num_home_visted' : num_home_visted
        #'num_horror_genre' : num_horror_genre
    }

    return render(request, 'catalog/index.html', context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 1


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksByAllListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, id = pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)

        if form.is_valid():
            #renew_date = form.cleaned_data['renewal_date']
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # Redirect to new URL
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_new_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date' : proposed_new_date})

    context = {
        'form' : form,
        'book_instance' : book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    initial = {'date_of_birth' : datetime.timedelta(weeks= -10)}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'

class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')