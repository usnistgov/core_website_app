"""  Test send mail
"""

from django.core import mail
from django.test import TestCase, override_settings
from unittest.mock import patch

import core_website_app.components.contact_message.api as contact_message_api
from core_website_app.components.contact_message.models import ContactMessage


class TestSendEmailContactMessage(TestCase):
    """Test Send Email Contact Message"""

    def setUp(self):
        """setUp"""

        self.contact_message = _create_contact_message()

    @override_settings(SEND_EMAIL_WHEN_CONTACT_MESSAGE_IS_RECEIVED=True)
    @patch(
        "core_website_app.components.contact_message.models"
        ".ContactMessage.save"
    )
    def test_contact_message_send_mail(self, mock_save):
        """test_contact_message_send_mail"""

        # Arrange
        mock_save.return_value = self.contact_message

        # Act
        contact_message_api.upsert(self.contact_message)

        # Assert
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "[Django] New Contact Message"
        )

    @override_settings(SEND_EMAIL_WHEN_CONTACT_MESSAGE_IS_RECEIVED=True)
    @patch(
        "core_website_app.components.contact_message.models"
        ".ContactMessage.save"
    )
    def test_contact_message_send_mail_admins(self, mock_save):
        """test_contact_message_send_mail_admins"""

        # Arrange
        mock_save.return_value = self.contact_message

        # Act
        contact_message_api.upsert(self.contact_message)

        # Assert
        self.assertEqual(len(mail.outbox[0].to), 2)
        self.assertEqual(
            mail.outbox[0].to, ["admin1@example.com", "admin2@example.com"]
        )

    @patch.object(contact_message_api, "settings")
    @patch(
        "core_website_app.components.contact_message.models"
        ".ContactMessage.save"
    )
    def test_contact_message_does_not_send_mail_when_email_disabled(
        self, mock_save, mock_settings
    ):
        """test_contact_message_does_not_send_mail_when_email_disabled"""
        # Arrange
        mock_settings.SEND_EMAIL_WHEN_CONTACT_MESSAGE_IS_RECEIVED = False
        mock_save.return_value = self.contact_message

        # Act
        contact_message_api.upsert(self.contact_message)
        # Assert
        self.assertEqual(len(mail.outbox), 0)


def _create_contact_message(
    name="name",
    email="email@test.com",
    content="message",
):
    """Create a contact message

    Args:
        name:
        email:
        content:

    Returns:
    """

    return ContactMessage(name=name, email=email, content=content)
