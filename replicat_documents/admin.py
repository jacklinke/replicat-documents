from django.contrib import admin

from .models import DocumentIssuerChoice, ReplicatDocument


@admin.register(DocumentIssuerChoice)
class DocumentIssuerChoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "app_name",
        "issuer_module_name",
        "label",
        "read_only",
        "enabled",
    )

    list_filter = (
        "app_name",
        "read_only",
        "enabled",
    )
    readonly_fields = (
        "id",
        "app_name",
        "issuer_module_name",
        "label",
        "enabled",
    )

    fieldsets = (
        (None, {"fields": ("id", "app_name", "issuer_module_name", "label")}),
        (
            "Status",
            {
                "fields": ("read_only", "enabled"),
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ReplicatDocument)
class ReplicatDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "updated_at",
        "rendered_to_pdf_at",
    )

    list_filter = ("issuer",)
    readonly_fields = (
        "id",
        "context",
        "rendered_to_pdf_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (None, {"fields": ("id", "issuer", "context", "context_query", "metadata")}),
        (
            "Dates",
            {
                "fields": ("rendered_to_pdf_at", "created_at", "updated_at"),
            },
        ),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        # Prevent creating new `issuer` within admin
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "issuer":
            formfield.widget.can_add_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_delete_related = False
        return formfield

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["issuer"].queryset = DocumentIssuerChoice.objects.filter(enabled=True, read_only=False)
        return form
