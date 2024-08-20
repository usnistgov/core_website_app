""" Tests of Terms Of Use API
"""

from unittest.case import TestCase

from unittest.mock import Mock, patch

from core_main_app.commons import exceptions
from core_website_app.components.terms_of_use import api as terms_of_use_api
from core_main_app.components.web_page.models import WebPage


class TestTermsOfUseGet(TestCase):
    """Test Terms Of Use Get"""

    @patch("core_main_app.components.web_page.api.get")
    def test_terms_of_use_get_return_term_of_use_page_name(self, mock_get):
        """test_terms_of_use_get_return_term_of_use_page_name"""

        # Arrange
        mock_get.return_value = "term_of_use"

        # Act
        result = terms_of_use_api.get()

        # Assert
        self.assertEqual(result, "term_of_use")


class TestTermsOfUseUpsert(TestCase):
    """Tests Terms Of Use Upsert"""

    def test_terms_of_use_upsert_raises_error_message(self):
        """test_terms_of_use_upsert_raises_error_message"""
        # Arrange
        term_of_use_page = Mock(spec=WebPage, type=1, content="test")

        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            terms_of_use_api.upsert(term_of_use_page)

    @patch("core_main_app.components.web_page.api.upsert")
    def test_terms_of_use_upsert_returns_correct_page(self, mock_upsert):
        """test_terms_of_use_upsert_returns_correct_page"""

        # Arrange
        term_of_use_page = Mock(spec=WebPage, type=0, content="test")
        mock_upsert.return_value = term_of_use_page
        # Act
        result = terms_of_use_api.upsert(term_of_use_page)

        # Assert
        self.assertEqual(result.type, 0)
