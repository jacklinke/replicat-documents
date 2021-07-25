from django.urls import path

from replicat_documents import views

app_name = "replicat_documents"

urlpatterns = [
    path("documents/<uuid:id>", views.document_view_html, name="document_view_html"),
    path("documents/<uuid:id>.pdf", views.document_view_pdf, name="document_view_df"),
]
