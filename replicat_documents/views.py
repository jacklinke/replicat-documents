import uuid

from django.template.response import TemplateResponse


def document_view_html(request, id):
    """Renders the document as html"""
    obj = get_object_or_404(Post, pk=uuid.UUID(id))

    template = "detail_view.html"
    context = {}

    context["data"] = MyModel.objects.get(id=id)

    return TemplateResponse(request, template, context)


def document_view_pdf(request, id):
    """Renders the document as a PDF"""

    # Check if a pdf version exists, and if so, serve it

    # If not, render to PDF and then serve the file
