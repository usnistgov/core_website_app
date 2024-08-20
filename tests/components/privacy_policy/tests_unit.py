""" Tests of privacy policy API
"""

from unittest.case import TestCase

from unittest.mock import Mock, patch

from core_main_app.commons import exceptions
from core_website_app.components.privacy_policy import (
    api as privacy_policy_api,
)
from core_main_app.components.web_page.models import WebPage


class TestPrivacyPolicyGet(TestCase):
    """Test Privacy Policy Get"""

    @patch("core_main_app.components.web_page.api.get")
    def test_privacy_policy_returns_privacy_policy_page_name(self, mock_get):
        """test_privacy_policy_get_return_privacy_policy_page_name"""

        # Arrange
        mock_get.return_value = "privacy_policy"

        # Act
        result = privacy_policy_api.get()

        # Assert
        self.assertEqual(result, "privacy_policy")


class TestPrivacyPolicyUpsert(TestCase):
    """Tests Privacy Policy Upsert"""

    def test_help_upsert_raises_error_message(self):
        """test_privacy_policy_upsert_raises_error_message"""

        # Arrange
        privacy_policy_page = Mock(spec=WebPage, type=2, content="test")
        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            privacy_policy_api.upsert(privacy_policy_page)

    @patch("core_main_app.components.web_page.api.upsert")
    def test_help_upsert_returns_correct_page(self, mock_upsert):
        """test_privacy_policy_upsert_returns_correct_page"""

        # Arrange
        privacy_policy_page = Mock(spec=WebPage, type=1, content="test")
        mock_upsert.return_value = privacy_policy_page
        # Act
        result = privacy_policy_api.upsert(privacy_policy_page)

        # Assert
        self.assertEqual(result.type, 1)
