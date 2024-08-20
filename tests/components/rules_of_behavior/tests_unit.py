""" Tests of Rules Of Behavior API
"""

from unittest.case import TestCase

from unittest.mock import Mock, patch

from core_main_app.commons import exceptions
from core_website_app.components.rules_of_behavior import (
    api as rules_of_behavior_api,
)
from core_main_app.components.web_page.models import WebPage


class TestRulesOfBehaviorGet(TestCase):
    """Test Rules Of Behavior Get"""

    @patch("core_main_app.components.web_page.api.get")
    def test_rules_of_behavior_get_return_rules_of_behavior_page_name(
        self, mock_get
    ):
        """test_rules_of_behavior_get_return_rules_of_behavior_page_name"""

        # Arrange
        mock_get.return_value = "rules_of_behavior"

        # Act
        result = rules_of_behavior_api.get()

        # Assert
        self.assertEqual(result, "rules_of_behavior")


class TestRulesOfBehaviorUpsert(TestCase):
    """Tests Rules Of Behavior Upsert"""

    def test_rules_of_behavior_upsert_raises_error_message(self):
        """test_rules_of_behavior_upsert_raises_error_message"""

        # Arrange
        rules_of_behavior_page = Mock(spec=WebPage, type=1, content="test")

        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            rules_of_behavior_api.upsert(rules_of_behavior_page)

    @patch("core_main_app.components.web_page.api.upsert")
    def test_rules_of_behavior_upsert_returns_correct_page(self, mock_upsert):
        """test_rules_of_behavior_upsert_returns_correct_page"""

        # Arrange
        rules_of_behavior_page = Mock(spec=WebPage, type=4, content="test")
        mock_upsert.return_value = rules_of_behavior_page
        # Act
        result = rules_of_behavior_api.upsert(rules_of_behavior_page)

        # Assert
        self.assertEqual(result.type, 4)
