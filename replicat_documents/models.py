import uuid

from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import FieldError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from pydantic.error_wrappers import ValidationError as PydanticValidationError

CACHED_DOCUMENT_ISSUER_KEY = "cached_document_issuers"


def flatten_json(input, delimeter="_"):
    """Returns a flat dictionary by flattening nested objects using the given delimeter"""
    output = {}

    def flatten(element, name=""):
        if type(element) is dict:
            for item in element:
                flatten(element[item], name + item + delimeter)
        elif type(element) is list:
            i = 0
            for item in element:
                flatten(item, name + str(i) + delimeter)
                i += 1
        else:
            output[name[:-1]] = element

    flatten(input)
    return output


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


class DocumentIssuerChoiceQuerySet(models.QuerySet):
    def enabled(self):
        """Filters out any disabled issuers"""
        return self.filter(enabled=True)

    def writable(self):
        """Filters out any read_only issuers"""
        return self.exclude(read_only=True)


class DocumentIssuerChoiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def clear_cached_instances(self):
        """Sets and returns a cache entry with all enabled DocumentIssuerChoice instances,
        optionally filtering out read_only instances.
        """
        cache.set(CACHED_DOCUMENT_ISSUER_KEY, None)
        return None

    def set_cached_instances(self, allow_read_only=False):
        """Sets and returns a cache entry with all enabled DocumentIssuerChoice instances,
        optionally filtering out read_only instances.
        """
        if not allow_read_only:
            document_issuer_choices = serializers.serialize("json", self.enabled().writable())
        else:
            document_issuer_choices = serializers.serialize("json", self.enabled())

        cache.set(CACHED_DOCUMENT_ISSUER_KEY, document_issuer_choices)
        return document_issuer_choices

    def get_cached_instances(self, allow_read_only=False, refresh=False):
        """Returns the cached DocumentIssuerChoice instances, refreshing the data if desired"""
        if cache.get(CACHED_DOCUMENT_ISSUER_KEY, default=None) is None or refresh == True:
            cached = self.set_cached_instances(allow_read_only=allow_read_only)

        document_issuer_choices = cache.get(CACHED_DOCUMENT_ISSUER_KEY, default=None)
        return document_issuer_choices


CombinedDocumentIssuerChoiceManager = DocumentIssuerChoiceManager.from_queryset(DocumentIssuerChoiceQuerySet)


class DocumentIssuerChoice(models.Model):
    """Provides the list of allowed issuers for documents."""

    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("ID for the Document Issuer Choice as an UUID"),
    )

    app_name = models.CharField(
        _("Issuer App"),
        max_length=100,
        editable=False,
        help_text=_("App which contains this document issuer"),
    )

    issuer_module_name = models.CharField(
        _("Issuer Module Name"),
        max_length=100,
        editable=False,
        help_text=_("Issuer module name of this document issuer"),
    )

    label = models.CharField(
        _("Label"),
        max_length=100,
        unique=True,
        editable=False,
        help_text=_("The descriptive label for this Document Issuer"),
    )

    read_only = models.BooleanField(
        _("Read Only"),
        default=False,
        help_text=_(
            "Setting to True allows existing documents to be rendered, but disallows creation "
            "of new documents with this issuer."
        ),
    )

    enabled = models.BooleanField(
        _("Enabled"),
        default=True,
        editable=False,
        help_text=_(
            "If the issuer has been removed, this value will automatically be set to False, "
            "preventing creation or rendering of associated documents."
        ),
    )

    objects = CombinedDocumentIssuerChoiceManager()

    def __str__(self):
        return f"{self.label}"

    class Meta:
        verbose_name = _("Document Issuer")
        verbose_name_plural = _("Document Issuers")

        unique_together = ("app_name", "issuer_module_name")

    def writable(self):
        return self.enabled and not self.read_only

    def enable(self):
        self.enabled = True
        self.save()


class ReplicatDocument(models.Model):
    """Replicat Document Model"""

    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("ID for the Document as an UUID"),
    )

    issuer = models.ForeignKey(
        DocumentIssuerChoice,
        verbose_name=_("Issuer"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("The issuer for this document"),
    )

    context = PydanticModelField(
        pydantic_model=None,
        verbose_name=_("Collected context"),
        editable=False,
        null=True,
        blank=True,
        help_text=_("Context used to render the document's template"),
    )

    # ToDo: Is this really needed? Do we care about the original param string if we have the context?
    context_query = PydanticModelField(
        pydantic_model=None,
        verbose_name=_("Context query parameters"),
        help_text=_("Context will be fetched from those parameters"),
    )

    metadata = models.JSONField(
        _("Metadata"),
        default=dict,
        help_text=_("Metadata in JSON format for the rendered PDF document"),
    )

    # For each file format, these fields record when the file was last saved in that format.
    rendered_to_pdf_at = models.DateTimeField(
        _("Rendered to PDF at"),
        null=True,
        help_text=_("Date and time at which the document was last rendered as pdf"),
    )

    created_at = models.DateTimeField(
        _("Created on"),
        auto_now_add=True,
        editable=False,
        help_text=_("Date and time at which the document was created"),
    )

    updated_at = models.DateTimeField(
        _("Updated on"),
        auto_now=True,
        editable=False,
        help_text=_("Date and time at which the document was last updated"),
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = _("Replicat Document")
        verbose_name_plural = _("Replicat Document")

    def get_absolute_url(self):
        return reverse("document_view_html", kwargs={"id": self.id})

    def expire_files(self):
        """Remove associated rendered files and reset dates to None"""

        if self.rendered_to_pdf_at is not None:
            # ToDo: delete corresponding file
            self.rendered_to_pdf_at = None
            self.save()

    @property
    def flat_metadata(self):
        return flatten_json(self.metadata)

    def render_to_pdf(self):
        """Attempts to render the file to PDF using the id as filename

        If successfull, returns True, otherwise returns False"""
        return False
