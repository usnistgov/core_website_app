""" Tests of the account request API
"""

from unittest.case import TestCase
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons.exceptions import ApiError
from core_website_app.components.account_request import (
    api as account_request_api,
)
from core_website_app.components.account_request.models import AccountRequest


class TestsAccountRequestGet(TestCase):
    """Tests Account Request Get"""

    @patch(
        "core_website_app.components.account_request.models"
        ".AccountRequest.get_by_id"
    )
    def test_account_request_get_return_request_object(self, mock_get_by_id):
        """test_account_request_get_return_request_object"""

        # Arrange
        request_id = "1"
        mock_get_by_id.return_value = _create_account_request()
        # Act
        result = account_request_api.get(request_id)
        # Assert
        self.assertIsInstance(result, AccountRequest)

    @patch(
        "core_website_app.components.account_request.models"
        ".AccountRequest.get_by_id"
    )
    def test_account_request_get_raise_api_error_if_request_not_found(
        self, mock_get_by_id
    ):
        """test_account_request_get_raise_api_error_if_request_not_found"""

        # Arrange
        request_id = "1"
        mock_get_by_id.side_effect = Exception()
        # Act # Assert
        with self.assertRaises(ApiError):
            account_request_api.get(request_id)


class TestsAccountRequestAccept(TestCase):
    """Tests Account Request Accept"""

    def setUp(self):
        """setUp"""

        self.account_request = _create_account_request()

    @patch(
        "core_website_app.components.account_request.models"
        ".AccountRequest.delete"
    )
    @patch(
        "core_website_app.components.account_request.api"
        "._get_user_by_username"
    )
    def test_account_request_accept_raise_api_error_if_user_does_not_exist(
        self, mock_get_user_by_username, mock_delete
    ):
        """test_account_request_accept_raise_api_error_
        if_user_does_not_exist"""

        # Arrange
        mock_get_user_by_username.side_effect = ObjectDoesNotExist()

        # Act # Assert
        with self.assertRaises(ApiError):
            account_request_api.accept(self.account_request)

    @patch(
        "core_website_app.components.account_request.models."
        "AccountRequest.delete"
    )
    @patch(
        "core_website_app.components.account_request.api."
        "_create_and_save_user"
    )
    @patch(
        "core_website_app.components.account_request.api."
        "_get_user_by_username"
    )
    def test_account_request_accept_return_user(
        self, mock_get_by_username, mock_create_and_save, mock_delete
    ):
        """test_account_request_accept_return_user"""

        # Arrange
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_get_by_username.return_value = mock_user
        mock_create_and_save.return_value = mock_user
        mock_delete.return_value = None

        # Act
        result = account_request_api.accept(self.account_request)

        #  Assert
        self.assertIsInstance(result, User)


class TestsAccountRequestDeny(TestCase):
    """Tests Account Request Deny"""

    def setUp(self):
        """setUp"""

        self.account_request = _create_account_request()

    @patch(
        "core_website_app.components.account_request.models."
        "AccountRequest.delete"
    )
    @patch(
        "core_website_app.components.account_request.api."
        "_get_user_by_username"
    )
    def test_account_request_deny_raise_api_error_if_user_does_not_exist(
        self, mock_get_user_by_username, mock_delete
    ):
        """test_account_request_deny_raise_api_error_
        if_user_does_not_exist"""

        # Arrange
        mock_get_user_by_username.side_effect = ObjectDoesNotExist()

        # Act # Assert
        with self.assertRaises(ApiError):
            account_request_api.deny(self.account_request, False, None)

    @patch(
        "core_website_app.components.account_request.models."
        "AccountRequest.delete"
    )
    @patch(
        "core_website_app.components.account_request.api."
        "_create_and_save_user"
    )
    @patch(
        "core_website_app.components.account_request.api."
        "_get_user_by_username"
    )
    def test_account_request_deny_without_body_return_none(
        self, mock_get_by_username, mock_create_and_save, mock_delete
    ):
        """test_account_request_deny_without_body_return_none"""

        # Arrange
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_get_by_username.return_value = mock_user
        mock_create_and_save.return_value = mock_user
        mock_delete.return_value = None

        # Act
        result = account_request_api.deny(self.account_request)

        #  Assert
        self.assertEqual(result, None)

    @patch(
        "core_website_app.components.account_request.models."
        "AccountRequest.delete"
    )
    @patch(
        "core_website_app.components.account_request.api."
        "_create_and_save_user"
    )
    @patch(
        "core_website_app.components.account_request.api."
        "_get_user_by_username"
    )
    def test_account_request_deny_with_body_return_none(
        self, mock_get_by_username, mock_create_and_save, mock_delete
    ):
        """test_account_request_deny_with_body_return_none"""

        # Arrange
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_get_by_username.return_value = mock_user
        mock_create_and_save.return_value = mock_user
        mock_delete.return_value = None

        # Act
        result = account_request_api.deny(
            self.account_request,
            True,
            email_params={"body": "test", "subject": "deny"},
        )

        #  Assert
        self.assertEqual(result, None)


class TestsAccountRequestInsert(TestCase):
    """Tests Account Request Insert"""

    def setUp(self):
        """setUp"""

        self.mock_account_request = _create_account_request()

    @patch(
        "core_website_app.components.account_request.api"
        "._get_user_by_username"
    )
    def test_account_request_insert_raise_api_error_if_username_already_exist(
        self, mock_get_user_by_username
    ):
        """test_account_request_insert_raise_api_error
        _if_username_already_exist"""

        # Arrange
        mock_user = Mock(spec=User)
        mock_user.username = "username"
        mock_get_user_by_username.return_value = mock_user

        # Act # Assert
        with self.assertRaises(ApiError):
            account_request_api.insert(mock_user)

    @patch(
        "core_website_app.components.account_request.models"
        ".AccountRequest.save"
    )
    @patch(
        "core_website_app.components.account_request.api"
        "._get_user_by_username"
    )
    @patch(
        "core_website_app.components.account_request.api" "._get_user_by_email"
    )
    def test_account_request_raises_error_if_email_already_exists(
        self, mock_get_user_by_email, mock_get_user_by_username, mock_save
    ):
        """test_account_request_insert_return_request"""

        # Arrange
        mock_user = Mock(spec=User)
        mock_user.username = "username"
        mock_get_user_by_username.side_effect = ObjectDoesNotExist()
        mock_get_user_by_email.return_value = mock_user
        mock_save.return_value = self.mock_account_request

        # Act # Assert
        with self.assertRaises(ApiError):
            account_request_api.insert(mock_user)

    @patch(
        "core_website_app.components.account_request.models"
        ".AccountRequest.save"
    )
    @patch(
        "core_website_app.components.account_request.api"
        "._get_user_by_username"
    )
    @patch(
        "core_website_app.components.account_request.api" "._get_user_by_email"
    )
    def test_account_request_insert_return_request(
        self, mock_get_user_by_email, mock_get_user_by_username, mock_save
    ):
        """test_account_request_insert_return_request"""

        # Arrange
        mock_user = Mock(spec=User)
        mock_user.username = "username"
        mock_get_user_by_username.side_effect = ObjectDoesNotExist()
        mock_get_user_by_email.side_effect = ObjectDoesNotExist()
        mock_save.return_value = self.mock_account_request

        # Act
        result = account_request_api.insert(mock_user)

        # Assert
        self.assertIsInstance(result, AccountRequest)


class TestsAccountRequestGetCount(TestCase):
    """Tests Account Request Get Count"""

    def test_account_request_get_count_returns_count(self):
        """test_account_request_get_count_return_count"""

        # Act
        result = account_request_api.get_count()
        # Assert
        self.assertEqual(result, 0)

    @patch.object(User, "save")
    def test_account_request_get_count_returns_number_account(self, mock_save):
        """test_account_request_get_count_returns_number_account"""

        # Arrange
        user = User(username="test")
        mock_save.return_value = user
        account_request_api.insert(user)

        # Act
        result = account_request_api.get_count()

        # Assert
        self.assertEqual(result, 1)


def _create_account_request(username="username"):
    """
    Create an AccountRequest object using default parameters

    Parameters:
        username (str):

    Returns:
        AccountRequest object
    """
    return AccountRequest(username=username, email="test@example.com")
