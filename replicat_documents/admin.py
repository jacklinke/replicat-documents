from django.contrib import admin

from .models import ReplicatDocument


@admin.register(ReplicatDocument)
class ReplicatDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "document_id",
        "created_at",
        "updated_at",
        "rendered_to_pdf_at",
    ]
