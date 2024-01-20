from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language


# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Genre)
admin.site.register(Language)
