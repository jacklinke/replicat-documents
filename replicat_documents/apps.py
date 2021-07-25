"""AppConfig for the replicat-documents application"""

import functools
import logging
import os
import pkgutil
import sys
from importlib import import_module

import django
from django.apps import AppConfig, apps
from django.conf import settings
from django.db.models.signals import post_migrate

logger = logging.getLogger("replicat_documents")


def find_document_issuers(issuers_dir):
    """
    Given a path to an issuers directory, return a list of all the document issuer
    names that are available.
    """
    document_issuers_dir = os.path.join(issuers_dir, "documents")
    return [
        name
        for _, name, is_pkg in pkgutil.iter_modules([document_issuers_dir])
        if not is_pkg and not name.startswith("_")
    ]


def load_document_issuer_class(document_issuer_name, app_name):
    """
    Given a document issuer name and an application name, return the DocumentIssuer
    class instance. Allow all errors raised by the import process
    (ImportError, AttributeError) to propagate.
    """
    module = import_module("%s.issuers.documents.%s" % (app_name, document_issuer_name))
    return module.DocumentIssuer()


@functools.lru_cache(maxsize=None)
def get_document_issuers():
    """
    Return a dictionary mapping document issuer module names to a dictionary of its
    callback application and issuer label.

    Look for a issuers.documents package in django.core, and in each installed
    application -- if a documents package exists, register all document issuers
    in that package.

    Core document issuers are always included. If a settings module has been
    specified, also include user-defined document issuers.

    The dictionary is in the format {document_issuer_name: app_name}.

    Key-value pairs from this dictionary can then be used in calls to
    load_document_issuer_class(app_name, document_issuer_name)

    The dictionary is cached on the first call and reused on subsequent calls.
    """
    document_issuers = {}

    if not settings.configured:
        return document_issuers

    for app_config in reversed(list(apps.get_app_configs())):
        path = os.path.join(app_config.path, "issuers")

        for name in find_document_issuers(path):
            label = load_document_issuer_class(name, app_config.name).label
            document_issuers.update({name: {"app_name": app_config.name, "label": label}})

    return document_issuers


# pylint: disable=unused-argument
def register_issuer_objects(sender, **kwargs):
    """Registers Issuer Model instances

    Registration includes creating a new DocumentIssuerChoice instance if it does not exist,
    enabling it if it does already exist, and disabling any non-existent issuers.
    """
    from replicat_documents.models import DocumentIssuerChoice

    for key, value in get_document_issuers().items():
        obj, created = DocumentIssuerChoice.objects.update_or_create(
            issuer_module_name=key, app_name=value["app_name"], label=value["label"]
        )

        if not created:
            obj.enable()

    # Set `enabled=False` for DocumentIssuerChoice instances which no longer have an associated issuer module
    DocumentIssuerChoice.objects.exclude(issuer_module_name__in=get_document_issuers().keys()).update(enabled=False)


class ReplicatDocumentsConfig(AppConfig):
    """Replicat Documents application configuration"""

    default = False
    name = "replicat_documents"
    verbose_name = "Replicat Documents"

    def ready(self):
        logger.debug("ReplicatDocumentsConfig ready method")
        post_migrate.connect(register_issuer_objects, sender=self)
