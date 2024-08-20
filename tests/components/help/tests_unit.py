""" Tests of Help API
"""

from unittest.case import TestCase

from unittest.mock import Mock, patch

from core_main_app.commons import exceptions
from core_website_app.components.help import api as help_api
from core_main_app.components.web_page.models import WebPage


class TestHelpGet(TestCase):
    """Test help Get"""

    @patch("core_main_app.components.web_page.api.get")
    def test_help_get_return_help_page_name(self, mock_get):
        """test_help_get_return_help_page_name"""

        # Arrange
        mock_get.return_value = "help"

        # Act
        result = help_api.get()

        # Assert
        self.assertEqual(result, "help")


class TestHelpUpsert(TestCase):
    """Tests Help Upsert"""

    def test_help_upsert_raises_error_message(self):
        """test_help_upsert_raises_error_message"""

        # Arrange
        help_page = Mock(spec=WebPage, type=1, content="test")

        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            help_api.upsert(help_page)

    @patch("core_main_app.components.web_page.api.upsert")
    def test_help_upsert_returns_correct_page(self, mock_upsert):
        """test_help_upsert_returns_correct_page"""

        # Arrange
        help_page = Mock(spec=WebPage, type=2, content="test")
        mock_upsert.return_value = help_page
        # Act
        result = help_api.upsert(help_page)

        # Assert
        self.assertEqual(result.type, 2)
