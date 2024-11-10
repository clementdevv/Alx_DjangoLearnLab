from django.contrib import admin

# Register your models here.
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Fields that can be used to filter the books
    list_filter = ('publication_year', 'author')
    
    # Fields that can be searched
    search_fields = ('title', 'author')
    
    # Fields to use for ordering
    ordering = ('title', 'publication_year')
    
    # Add fields that can be edited directly in the list view
    list_editable = ('publication_year',)
    
    # Number of items to display per page
    list_per_page = 20
    
    # Fields to display when adding/editing a book
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author')
        }),
        ('Publication Details', {
            'fields': ('publication_year',)
        }),
    )