from django.contrib import admin

from .models import ReplicatDocument


@admin.register(ReplicatDocument)
class ReplicatDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document_id",
        "created_at",
        "updated_at",
        "rendered_to_pdf_at",
    )

    list_filter = ("issuer",)
    readonly_fields = (
        "id",
        "document_id",
        "context",
        "rendered_to_pdf_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (None, {"fields": ("id", "document_id", "issuer", "context", "context_query")}),
        (
            "Dates",
            {
                "fields": ("rendered_to_pdf_at", "created_at", "updated_at"),
            },
        ),
    )
