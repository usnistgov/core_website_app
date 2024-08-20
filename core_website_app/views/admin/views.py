""" Admin views
"""

from django.contrib.admin.views.decorators import staff_member_required

import core_website_app.components.account_request.api as account_request_api
import core_website_app.components.contact_message.api as contact_message_api
from core_main_app.utils.rendering import admin_render
from core_website_app.settings import (
    EMAIL_DENY_SUBJECT,
    SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_DENIED,
)


@staff_member_required
def user_requests(request):
    """Page that allows to accept or deny user requests

    Args:
        request:

    Returns:
    """
    # Call the API
    requests = account_request_api.get_all()

    assets = {
        "js": [
            {
                "path": "core_website_app/admin/js/user_requests.js",
                "is_raw": False,
            },
        ],
    }

    modals = [
        "core_website_app/admin/account_requests/modals/deny_request.html",
    ]

    return admin_render(
        request,
        "core_website_app/admin/user_requests.html",
        assets=assets,
        modals=modals,
        context={
            "requests": requests,
            "send_email_when_account_request_is_denied": SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_DENIED,
            "default_email_subject": EMAIL_DENY_SUBJECT,
        },
    )


@staff_member_required
def contact_messages(request):
    """List messages from the contact page

    Args:
        request:

    Returns:
    """

    # Call the API
    messages_contact = contact_message_api.get_all()

    assets = {
        "js": [
            {"path": "core_website_app/admin/js/messages.js", "is_raw": False},
        ],
        "css": ["core_website_app/admin/css/messages.css"],
    }

    modals = [
        "core_website_app/admin/contact_messages/modals/delete_message.html",
    ]

    return admin_render(
        request,
        "core_website_app/admin/contact_messages.html",
        assets=assets,
        modals=modals,
        context={"contacts": messages_contact},
    )
