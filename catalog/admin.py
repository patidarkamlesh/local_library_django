from django.contrib import admin

from .models import Book, BookInstance, Author, Genre, Language

# Register your models here.

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'display_genre', 'language']
    inlines = [BooksInstanceInline]
admin.site.register(Book, BookAdmin)

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book','status', 'borrower','due_back','id']
    list_filter = ['status', 'due_back']
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
admin.site.register(BookInstance, BookInstanceAdmin)

class BooksInline(admin.TabularInline):
    model = Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'date_of_birth', 'date_of_death']
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Language)
admin.site.register(Genre)
