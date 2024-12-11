"""contact message API
"""

import logging
from core_website_app import settings
import core_main_app.utils.notifications.mail as send_mail_api
from core_main_app.commons import exceptions
from core_website_app.components.contact_message.models import ContactMessage


logger = logging.getLogger("core_website_app.components.contact_message.api")


def get_all():
    """List all messages

    Returns:

    """
    return ContactMessage.get_all()


def get_count():
    """Count number of contact messages currently in the database.

    Returns:
        int: number of contact messages
    """
    return len(get_all())


def get(message_id):
    """Get a message

    Args:
        message_id:

    Returns:

    """
    try:
        return ContactMessage.get_by_id(message_id)
    except Exception as exception:
        logger.error(str(exception))
        raise exceptions.ApiError(
            "No message could be found with the given id."
        )


def upsert(contact_message):
    """Insert or update a given message

    Args:
        contact_message:

    Returns:

    """
    try:
        # Check if new contact message
        if contact_message.id is None:
            if settings.SEND_EMAIL_WHEN_CONTACT_MESSAGE_IS_RECEIVED:
                context = {"URI": settings.SERVER_URI}
                template_path = (
                    "core_website_app/admin/email"
                    "/contact_message_for_admin.html"
                )

                send_mail_api.send_mail_to_website_contacts(
                    subject="New Contact Message",
                    path_to_template=template_path,
                    context=context,
                )

        # save method return self
        return contact_message.save()
    except Exception as exception:
        logger.error(str(exception))
        raise exceptions.ApiError("Save message failed")


def delete(contact_message):
    """Delete a message

    Args:
        contact_message:

    Returns:

    """
    try:
        contact_message.delete()
    except Exception as exception:
        logger.error(str(exception))
        raise exceptions.ApiError("Impossible to delete contact message.")
