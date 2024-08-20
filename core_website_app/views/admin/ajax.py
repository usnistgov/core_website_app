"""
    Ajax views for the admin part
"""

import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.views.decorators.http import require_http_methods

from xml_utils.commons.exceptions import HTMLError
from xml_utils.html_tree.parser import parse_html
from core_main_app.commons import exceptions as main_exceptions
from core_main_app.templatetags.stripjs import stripjs
import core_website_app.components.account_request.api as account_request_api
import core_website_app.components.contact_message.api as contact_message_api
from core_website_app.commons import exceptions
from core_website_app.settings import (
    SERVER_URI,
    SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_DENIED,
)


@staff_member_required
def accept_request(request):
    """
    Accepts a request and creates the user account
    :param request:
    :return:
    """
    try:
        request_id = request.POST["requestid"]
        account_request_from_api = account_request_api.get(request_id)
        account_request_api.accept(account_request_from_api)
        message = "Request Accepted"
    except main_exceptions.ApiError as error:
        raise exceptions.WebsiteAjaxError(str(error))
    except Exception as exception:
        raise exceptions.WebsiteAjaxError(str(exception))

    return HttpResponse(
        json.dumps({"message": message}), content_type="application/json"
    )


@staff_member_required
def deny_request(request):
    """
    Denies an account request
    :param request:
    :return:
    """

    try:
        email_params = None
        send_email = (
            request.POST.get("sendEmail") == "true"
            and SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_DENIED
        )
        request_id = request.POST.get("requestid")
        email_subject = request.POST.get("emailParams[subject]")
        email_body = request.POST.get("emailParams[body]")

        if request_id and send_email and email_subject and email_body:

            # check the HTML syntax
            parse_html(email_body, "div")

            # check dangerous script injection
            if email_body != stripjs(email_body):
                return HttpResponseBadRequest("Unsafe HTML.")

            email_params = {
                "subject": email_subject,
                "body": email_body,
            }
        elif not request_id:
            raise ("Wrong parameters.")

        account_request_from_api = account_request_api.get(request_id)
        account_request_api.deny(
            account_request_from_api, send_email, email_params
        )
        message = "Request denied"

    except HTMLError:
        return HttpResponseBadRequest("HTML is not generated properly.")
    except main_exceptions.ApiError as error:
        raise exceptions.WebsiteAjaxError(str(error))
    except Exception as exception:
        raise exceptions.WebsiteAjaxError(str(exception))

    return HttpResponse(
        json.dumps({"message": message}), content_type="application/json"
    )


@staff_member_required
def remove_message(request):
    """
    Remove a message from the list of messages
    :param request:
    :return:
    """

    try:
        contact_message = contact_message_api.get(request.POST["messageid"])
        contact_message_api.delete(contact_message)
        message = "Message deleted"
    except exceptions.WebsiteAjaxError as error:
        message = str(error)
    except Exception as exception:
        message = str(exception)

    return HttpResponse(
        json.dumps({"message": message}), content_type="application/json"
    )


@staff_member_required
def get_deny_email_template(request):
    """get_deny_email_template

    Args:
        request:

    Returns:

    """
    request_id = request.GET.get("requestid")

    if not request_id:
        return HttpResponseBadRequest("Missing account request id.")

    account_request = account_request_api.get(request_id)

    context = {
        "lastname": account_request.last_name,
        "firstname": account_request.first_name,
        "URI": SERVER_URI,
    }

    template = loader.get_template(
        "core_website_app/admin/email/request_account_denied.html"
    )
    content = template.render(context)

    return HttpResponse(
        json.dumps({"template": content}), content_type="application/json"
    )


@staff_member_required
@require_http_methods(["POST"])
def account_request_count(request):
    """Account request count"""
    return HttpResponse(
        json.dumps({"count": account_request_api.get_count()}),
        content_type="application/json",
    )


@staff_member_required
@require_http_methods(["POST"])
def contact_message_count(request):
    """Contact message count"""
    return HttpResponse(
        json.dumps({"count": contact_message_api.get_count()}),
        content_type="application/json",
    )
