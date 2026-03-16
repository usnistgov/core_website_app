"""Url router for the Rest API"""

from django.urls import re_path

import core_main_app.rest.web_page.views as web_page_views
import core_website_app.rest.account_request.views as account_request_views
import core_website_app.rest.contact_message.views as contact_message_views

urlpatterns = [
    re_path(
        r"^user-requests/$",
        account_request_views.AccountRequestList.as_view(),
        name="core_website_app_rest_account_request_list",
    ),
    re_path(
        r"^user-requests/(?P<pk>\w+)/$",
        account_request_views.AccountRequestDetail.as_view(),
        name="core_website_app_rest_account_request_detail",
    ),
    re_path(
        r"^user-requests/(?P<pk>\w+)/accept/$",
        account_request_views.AccountRequestAccept.as_view(),
        name="core_website_app_rest_account_request_accept",
    ),
    re_path(
        r"^user-requests/(?P<pk>\w+)/deny/$",
        account_request_views.AccountRequestDeny.as_view(),
        name="core_website_app_rest_account_request_deny",
    ),
    re_path(
        r"^messages/$",
        contact_message_views.ContactMessageList.as_view(),
        name="core_website_app_rest_message_list",
    ),
    re_path(
        r"^messages/(?P<pk>\w+)/$",
        contact_message_views.ContactMessageDetail.as_view(),
        name="core_website_app_rest_message_detail",
    ),
    re_path(
        r"^help/$",
        web_page_views.WebPageList.as_view(web_page_type="help"),
        name="core_website_app_rest_help_list",
    ),
    re_path(
        r"^privacy_policy/$",
        web_page_views.WebPageList.as_view(web_page_type="privacy_policy"),
        name="core_website_app_rest_privacy_policy_list",
    ),
    re_path(
        r"^terms_of_use/$",
        web_page_views.WebPageList.as_view(web_page_type="terms_of_use"),
        name="core_website_app_rest_terms_of_use_list",
    ),
]
