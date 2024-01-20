from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language


# admin.site.register(Author)

class AuthorAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Author, AuthorAdmin)

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Language)
