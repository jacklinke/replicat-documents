import uuid

from django.core.exceptions import FieldError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pydantic.error_wrappers import ValidationError as PydanticValidationError


class PydanticModelField(models.JSONField):
    """Pydantic Model Field.
    This field is a pydantic model field but with model validation when the model
    is provided.
    """

    def __init__(self, *args, **kwargs):
        self.pydantic_model = kwargs.pop("pydantic_model", None)
        super().__init__(*args, **kwargs)

    def _validate_pydantic_model(self, value, model_instance):
        """Perform pydantic model validation"""

        pydantic_model = self._get_pydantic_model(model_instance)

        # Disable validation when migrations are faked
        if self.model.__module__ == "__fake__":
            return

        # Validate either raw (JSON string) data or a serialized dict (before
        # saving the Django model).
        try:
            if isinstance(value, str):
                pydantic_model.parse_raw(value)
            elif isinstance(value, dict):
                pydantic_model(**value)
        except PydanticValidationError as error:
            raise DjangoValidationError(error, code="invalid") from error

    def _get_pydantic_model(self, model_instance):
        """Get field pydantic model from the expected model instance method"""

        if self.pydantic_model is None:
            try:
                return getattr(model_instance, f"get_{self.name}_pydantic_model")()
            except AttributeError as error:
                raise FieldError(
                    _(
                        f"A pydantic model is missing for the '{self.name}' field. "
                        "It should be provided thanks to the 'pydantic_model' "
                        "field argument or by adding a get_<FIELD_NAME>_pydantic_model "
                        "method to your model."
                    )
                ) from error
        return self.pydantic_model

    def validate(self, value, model_instance):
        """Add pydantic model validation to field validation"""

        # Validate JSON value
        super().validate(value, model_instance)

        self._validate_pydantic_model(value, model_instance)

    def pre_save(self, model_instance, add):
        """Ensure pydantic model validation occurs before saving"""

        value = super().pre_save(model_instance, add)
        if value and not self.null:
            self._validate_pydantic_model(value, model_instance)
        return value


class DocumentIssuerChoice(models.Model):
    """Provides the list of allowed issuers for documents."""

    issuer_path = models.TextField(
        _("Issuer Path"),
        help_text=_(
            "Full dot-notation path to the issuer class. e.g.: " "'account.issuers.documents.issuer_name.IssuerName'"
        ),
        unique=True,
        editable=False,
    )

    label = models.CharField(
        _("Label"),
        max_length=100,
        unique=True,
        editable=False,
        help_text=_("The descriptive label for this Document Issuer"),
    )

    def __str__(self):
        return f"{self.issuer_path}"


class ReplicatDocument(models.Model):
    """Document Model"""

    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        help_text=_("ID for the Document as an UUID"),
        default=uuid.uuid4,
        editable=False,
    )

    document_id = models.UUIDField(
        verbose_name=_("Document ID"),
        help_text=_("Generated document identifier"),
        null=True,
        unique=True,
    )

    issuer = models.ForeignKey(
        DocumentIssuerChoice,
        verbose_name=_("Issuer"),
        on_delete=models.CASCADE,
        help_text=_("The issuer of the document among allowed ones"),
    )

    context = PydanticModelField(
        pydantic_model=None,
        verbose_name=_("Collected context"),
        help_text=_("Context used to render the document's template"),
        editable=False,
        null=True,
        blank=True,
    )

    # ToDo: Is this really needed? Do we care about the original param string if we have the context?
    context_query = PydanticModelField(
        pydantic_model=None,
        verbose_name=_("Context query parameters"),
        help_text=_("Context will be fetched from those parameters"),
    )

    # For each file format, these fields record when the file was last saved in that format.
    rendered_to_pdf_at = models.DateTimeField(_("Rendered to PDF at"), null=True)

    created_at = models.DateTimeField(
        _("Created on"),
        help_text=_("Date and time at which the document was created"),
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        _("Updated on"),
        help_text=_("Date and time at which the document was last updated"),
        auto_now=True,
        editable=False,
    )

    def expire_files(self):
        """Remove associated rendered files and reset dates to None"""

        if self.rendered_to_pdf_at is not None:
            # ToDo: delete corresponding file
            self.rendered_to_pdf_at = None

        if self.rendered_to_pdf_at is not None:
            self.save()
