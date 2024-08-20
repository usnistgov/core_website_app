""" Unit tests for forms
"""

from unittest import TestCase
from unittest.mock import patch, Mock

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from core_website_app.views.user.forms import RequestAccountForm


class TestRequestAccountForm(TestCase):
    @patch(
        "core_website_app.components.account_request.api" "._get_user_by_email"
    )
    def test_request_account_form_clean_email_raises_validation_error_if_email_exists(
        self, mock_get_user_by_email
    ):
        """test_request_account_form_clean_email_raises_validation_error_if_email_exists

        Returns:

        """
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.username = "username"
        mock_get_user_by_email.return_value = mock_user
        form = RequestAccountForm()
        form.cleaned_data = {"email": "email"}

        # Act + Arrange
        with self.assertRaises(ValidationError):
            form.clean_email()

    @patch(
        "core_website_app.components.account_request.api" "._get_user_by_email"
    )
    def test_request_account_form_clean_email_returns_email_if_email_does_not_exist(
        self, mock_get_user_by_email
    ):
        """test_request_account_form_clean_email_returns_email_if_email_does_not_exist

        Returns:

        """
        # Arrange
        mock_get_user_by_email.side_effect = ObjectDoesNotExist()
        input_email = "email"

        form = RequestAccountForm()
        form.cleaned_data = {"email": input_email}

        # Act
        output_email = form.clean_email()

        # Assert
        self.assertEqual(input_email, output_email)
