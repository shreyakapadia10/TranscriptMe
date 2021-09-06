from transcriptions.models import Document
from django.contrib import admin
from .models import Document
from .forms import DocumentForm

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm
    search_fields = ('media_type', 'uploaded_at', ) 
    list_display = ('name', 'user', 'media_type', 'uploaded_at',)
    list_display_links = ('name',)
    list_filter = ('media_type', 'uploaded_at', )
    ordering = ('-uploaded_at', )


admin.site.register(Document, DocumentAdmin)