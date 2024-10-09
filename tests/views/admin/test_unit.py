""" Unit test for `views.admin.views` package.
"""

from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_website_app.views.admin.views import _build_requests_context


class TestBuildRequestsContext(SimpleTestCase):
    """Test Build Requests Context"""

    @patch(
        "core_website_app.components.account_request.api._get_user_by_username"
    )
    def test_build_requests_context_returns_list(
        self, mock_get_user_by_username
    ):
        """test_build_requests_context_returns_list

        Returns:

        """
        # Arrange
        mock_request = MagicMock()
        mock_request_list = [mock_request]
        mock_get_user_by_username.return_value = create_mock_user(2)
        # Act
        request_context = _build_requests_context(
            request_list=mock_request_list
        )
        # Assert
        self.assertTrue(isinstance(request_context, list))

    @patch(
        "core_website_app.components.account_request.api._get_user_by_username"
    )
    def test_build_requests_context_contains_requests_fields_and_edit_url(
        self, mock_get_user_by_username
    ):
        """test_build_requests_context_contains_requests_fields_and_edit_url

        Returns:

        """
        # Arrange
        mock_request = MagicMock()
        mock_request_list = [mock_request]
        mock_get_user_by_username.return_value = create_mock_user(2)
        # Act
        request_context = _build_requests_context(
            request_list=mock_request_list
        )
        # Assert
        self.assertTrue("id" in request_context[0])
        self.assertTrue("username" in request_context[0])
        self.assertTrue("first_name" in request_context[0])
        self.assertTrue("last_name" in request_context[0])
        self.assertTrue("email" in request_context[0])
        self.assertTrue("date" in request_context[0])
        self.assertTrue("edit_url" in request_context[0])

    @patch(
        "core_website_app.components.account_request.api._get_user_by_username"
    )
    def test_build_requests_context_edit_url_redirects_to_admin_user_page(
        self, mock_get_user_by_username
    ):
        """test_build_requests_context_edit_url_redirects_to_admin_user_page

        Returns:

        """
        # Arrange
        mock_request = MagicMock()
        mock_request_list = [mock_request]
        mock_user_id = 2
        mock_get_user_by_username.return_value = create_mock_user(mock_user_id)
        # Act
        request_context = _build_requests_context(
            request_list=mock_request_list
        )
        # Assert
        self.assertTrue(
            f"admin/auth/user/{str(mock_user_id)}/change"
            in request_context[0]["edit_url"]
        )
