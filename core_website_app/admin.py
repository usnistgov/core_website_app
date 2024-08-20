""" Url router for the administration site
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_main_app.admin import core_admin_site
from core_main_app.components.web_page.models import WEB_PAGE_TYPES
from core_main_app.views.admin.views import WebPageView
import core_website_app.components.help.api as help_api
import core_website_app.components.privacy_policy.api as privacy_policy_api
import core_website_app.components.rules_of_behavior.api as rules_of_behavior_api
import core_website_app.components.terms_of_use.api as terms_of_use_api
from core_website_app.views.admin import (
    views as admin_views,
    ajax as admin_ajax,
)

admin_urls = [
    re_path(
        r"^user-requests$",
        admin_views.user_requests,
        name="core_website_app_user_requests",
    ),
    re_path(
        r"^accept_request",
        admin_ajax.accept_request,
        name="core_website_app_accept_user_request",
    ),
    re_path(
        r"^deny_request",
        admin_ajax.deny_request,
        name="core_website_app_deny_user_request",
    ),
    re_path(
        r"^get_deny_email_template",
        admin_ajax.get_deny_email_template,
        name="core_website_app_get_deny_email_template",
    ),
    re_path(
        r"^request_count",
        admin_ajax.account_request_count,
        name="core_website_app_request_count",
    ),
    re_path(
        r"^contact-messages$",
        admin_views.contact_messages,
        name="core_website_app_contact_messages",
    ),
    re_path(
        r"^remove_message",
        admin_ajax.remove_message,
        name="core_website_app_remove_contact_message",
    ),
    re_path(
        r"^message_count",
        admin_ajax.contact_message_count,
        name="core_website_app_message_count",
    ),
    re_path(
        r"^privacy-policy$",
        staff_member_required(
            WebPageView.as_view(
                api=privacy_policy_api,
                get_redirect="core_website_app/admin/privacy_policy.html",
                post_redirect="core-admin:core_website_app_privacy",
                web_page_type=WEB_PAGE_TYPES["privacy_policy"],
            )
        ),
        name="core_website_app_privacy",
    ),
    re_path(
        r"^terms-of-use$",
        staff_member_required(
            WebPageView.as_view(
                api=terms_of_use_api,
                get_redirect="core_website_app/admin/terms_of_use.html",
                post_redirect="core-admin:core_website_app_terms",
                web_page_type=WEB_PAGE_TYPES["terms_of_use"],
            )
        ),
        name="core_website_app_terms",
    ),
    re_path(
        r"^help$",
        staff_member_required(
            WebPageView.as_view(
                api=help_api,
                get_redirect="core_website_app/admin/help.html",
                post_redirect="core-admin:core_website_app_help",
                web_page_type=WEB_PAGE_TYPES["help"],
            )
        ),
        name="core_website_app_help",
    ),
    re_path(
        r"^rules_of_behavior$",
        staff_member_required(
            WebPageView.as_view(
                api=rules_of_behavior_api,
                get_redirect="core_website_app/admin/rules_of_behavior.html",
                post_redirect="core-admin:core_website_app_rules_of_behavior",
                web_page_type=WEB_PAGE_TYPES["rules_of_behavior"],
            )
        ),
        name="core_website_app_rules_of_behavior",
    ),
]

urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
