"""Rules of behavior page api"""

import core_main_app.components.web_page.api as web_page_api
from core_main_app.commons.exceptions import ApiError
from core_website_app.commons.enums import WEB_PAGE_TYPES

RULES_OF_BEHAVIOR_PAGE_NAME = "rules_of_behavior"
RULES_OF_BEHAVIOR_PAGE_TYPE = WEB_PAGE_TYPES[RULES_OF_BEHAVIOR_PAGE_NAME]


def get():
    """Get the help if exist

    Returns: rules of behavior web page
    """
    return web_page_api.get(RULES_OF_BEHAVIOR_PAGE_NAME)


def upsert(rules_of_behavior_page):
    """Post the rules of behavior

    Parameters:
        rules_of_behavior_page (WebPage): Webpage for the rules of behavior

    Returns: rules_of_behavior_page web page
    """
    if rules_of_behavior_page.type != RULES_OF_BEHAVIOR_PAGE_TYPE:
        raise ApiError(
            "Webpage type not coherent (expected: %s; actual %s"
            % (
                str(RULES_OF_BEHAVIOR_PAGE_TYPE),
                str(rules_of_behavior_page.type),
            )
        )

    return web_page_api.upsert(rules_of_behavior_page)
