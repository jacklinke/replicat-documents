class InvalidDocumentIssuer(Exception):
    """Invalid document issuer exception.

    This exception is raised when one tries to instantiate a document issuer
    that does not exist or is not enabled.
    """


class DocumentIssuerContextQueryValidationError(Exception):
    """Document issuer context_query validation error.

    This exception is raised when the input context_query for a document
    issuer does not validate the document issuer context_query schema.
    """


class DocumentIssuerContextValidationError(Exception):
    """Document issuer context validation error.

    This exception is raised when the context fetched by a document issuer
    does not validate the document issuer context schema.
    """


class DocumentIssuerMissingContext(Exception):
    """Document issuer missing context error.

    This exception is raised when the document issuer context is missing to
    perform an action, e.g. to create a document.
    """


class DocumentIssuerMissingContextQuery(Exception):
    """Document issuer missing context query error.

    This exception is raised when the document issuer context query is missing
    to perform an action, e.g. to create a document.
    """
