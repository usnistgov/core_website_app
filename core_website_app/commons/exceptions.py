"""
Core website exceptions
"""


class WebsiteAjaxError(Exception):
    """
    Exception raised by the Website package from ajax
    """

    def __init__(self, message):
        self.message = message
