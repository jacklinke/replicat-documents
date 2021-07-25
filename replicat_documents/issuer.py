import uuid
from abc import ABC, abstractmethod
from typing import Union

from django.conf import settings
from django.template import Context
from django.template.engine import Engine
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import re_camel_case
from django.utils.translation import gettext_lazy as _
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from replicat_documents.exceptions import (
    DocumentIssuerContextQueryValidationError,
    DocumentIssuerContextValidationError,
    DocumentIssuerMissingContext,
    DocumentIssuerMissingContextQuery,
)


class AbstractDocumentIssuer(ABC):
    """Base document issuer.

    To define a new document, one should inherit from this interface and
    implement the `fetch_context` abstract method.
    """

    label = ""

    # Models
    context_model: BaseModel = None
    context_query_model: BaseModel = None

    # def __init__(self, identifier: uuid.UUID = None, context_query: Union[str, dict] = None):

    #     # Document
    #     self.identifier = self.generate_identifier(identifier)
    #     self.document_path = self.get_document_path()

    #     # Data
    #     self.context = None
    #     self.context_query = self.validate_context_query(context_query) if context_query is not None else None

    #     # Templates
    #     self.css = None
    #     self.html = None

    #     super().__init__()

    # @classmethod
    # def validate_context(cls, context: Union[str, dict]) -> BaseModel:
    #     """Use required context pydantic model to validate input context."""

    #     if cls.context_model is None:
    #         raise DocumentIssuerMissingContext(str(_("Context model is missing")))

    #     try:
    #         if isinstance(context, str):
    #             context = cls.context_model.parse_raw(context)
    #         elif isinstance(context, dict):
    #             context = cls.context_model(**context)
    #     except ValidationError as error:
    #         raise DocumentIssuerContextValidationError(
    #             _(f"Document issuer context string is not valid: {error}")
    #         ) from error
    #     return context

    # @classmethod
    # def validate_context_query(cls, context_query: Union[str, dict]) -> BaseModel:
    #     """Use required context query pydantic model to validate input context query."""

    #     if cls.context_query_model is None:
    #         raise DocumentIssuerMissingContextQuery(str(_("Context query model is missing")))

    #     try:
    #         if isinstance(context_query, str):
    #             context_query = cls.context_query_model.parse_raw(context_query)
    #         if isinstance(context_query, dict):
    #             context_query = cls.context_query_model(**context_query)
    #     except ValidationError as error:
    #         raise DocumentIssuerContextQueryValidationError(
    #             _(f"Document issuer context query string is not valid: {error}")
    #         ) from error
    #     return context_query

    # @cached_property
    # def __default_template_basename(self):
    #     """Get default template base name given its class name.
    #     Example subsequent class name transformations:
    #       DummyDocument
    #         -> _Dummy_Document
    #         -> Dummy_Document
    #         -> dummy_document
    #         -> dummy
    #     """

    #     return re_camel_case.sub(r"_\1", self.__class__.__name__).strip("_").lower().replace("_document", "")

    # def __get_template(self, template_path):
    #     """Get a template from its relative path.
    #     This method always tries to return a template using the default
    #     template engine if it is not set.
    #     """
    #     if self.template_engine is None:
    #         template_engine = self.get_template_engine()
    #     return template_engine.get_template(template_path)

    # def generate_identifier(self, identifier=None):
    #     """Generate the document identifier.
    #     If the identifier has been set or is provided as an argument, it will
    #     be returned, or else a new UUID is generated.
    #     """

    #     if hasattr(self, "identifier") and self.identifier is not None:
    #         return self.identifier
    #     if identifier is not None:
    #         return str(identifier)
    #     return str(uuid.uuid4())

    # def get_document_path(self):
    #     """Get (generated) document path.
    #     Return default (or set) document path as a pathlib.Path object.
    #     """

    #     if hasattr(self, "document_path") and self.document_path is not None:
    #         return self.document_path
    #     return defaults.DOCUMENTS_ROOT.joinpath(f"{self.identifier}.pdf")

    # def get_document_url(self, host=None, schema="https"):
    #     """Get (generated) document URL.
    #     If the host argument is provided a fully qualified URL will be
    #     returned, or else, an absolute URL will be generated.
    #     """
    #     relative_path = self.get_document_path().relative_to(defaults.DOCUMENTS_ROOT)
    #     relative_url = f"{settings.MEDIA_URL}{relative_path}"
    #     if host is None:
    #         return relative_url
    #     return f"{schema}://{host}{relative_url}"

    # def get_css(self):
    #     """Get CSS template instance"""

    #     if self.css is not None:
    #         return self.css
    #     return self.__get_template(self.get_css_template_path())

    # def get_css_template_path(self):
    #     """Get CSS template path.
    #     Return default (or set) CSS template path as a pathlib.Path object.
    #     """

    #     if self.css_template_path is not None:
    #         return self.css_template_path
    #     return defaults.DOCUMENTS_TEMPLATE_ROOT.joinpath(f"{self.__default_template_basename}.css")

    # def get_html(self):
    #     """Get HTML template instance"""

    #     if self.html is not None:
    #         return self.html
    #     return self.__get_template(self.get_html_template_path())

    # def get_html_template_path(self):
    #     """Get HTML template path.
    #     Return default (or set) HTML template path as a pathlib.Path object.
    #     """

    #     if self.html_template_path is not None:
    #         return self.html_template_path
    #     return defaults.DOCUMENTS_TEMPLATE_ROOT.joinpath(f"{self.__default_template_basename}.html")

    # def get_template_engine(self):
    #     """Get template engine.
    #     Return default (or set) template engine.
    #     """
    #     if self.template_engine is not None:
    #         return self.template_engine
    #     return Engine.get_default()

    # @abstractmethod
    # def fetch_context(self) -> dict:
    #     """Fetch document context given context query parameters.
    #     This method should be implemented while using this interface for a
    #     custom document class.
    #     Note that it is highly recommended to validate the context_query using
    #     the validate_context_query method in your implementation to ensure data
    #     consistency.
    #     Returns fetched context as a dictionnary.
    #     """

    # def set_context(self, context: dict):
    #     """Validate and set context passed as a dictionary instance"""
    #     self.context = self.validate_context(context)

    # def get_django_context(self) -> Context:
    #     """Get the Django Context instance from the context model instance."""
    #     return Context(self.context.dict())

    # def create(self):
    #     """Create document.
    #     Given an HTML template, a CSS template and the required context to
    #     compile them, we render the document HTML that will be used by
    #     Chrome's headless web browser to generate the document as a PDF
    #     file.
    #     The path of the document is returned as a pathlib.Path instance.
    #     """

    #     if self.context is None:
    #         self.set_context(self.fetch_context())

    #     document_path = self.get_document_path()
    #     django_context = self.get_django_context()
    #     html_str = self.get_html().render(django_context)
    #     css_str = self.get_css().render(django_context)

    #     font_config = FontConfiguration()
    #     html = HTML(string=html_str, url_fetcher=static_file_fetcher)
    #     css = CSS(string=css_str, font_config=font_config)

    #     document = html.render(stylesheets=[css], font_config=font_config)
    #     document.metadata = self.metadata
    #     document.write_pdf(target=document_path, zoom=1)

    #     return document_path
