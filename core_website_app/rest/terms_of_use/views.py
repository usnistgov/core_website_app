""" rest api for the terms of use
################################################################################
#
# File Name: views.py
# Application: api
# Purpose:
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
"""

# API
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
# Permissions
from mgi.permissions import api_staff_member_required
# Models
from core_website_app.components.terms_of_use.api import \
    terms_of_use_get as api_terms_of_use_get, \
    terms_of_use_post as api_terms_of_use_post
# Serializers
from ..serializers import WebPageSerializer

import logging
# logger = logging.getLogger("core_website_app.rest.terms_of_use")


def terms_of_use_get():
    """
    Get the terms of use
    :param request:
    :return:
    """
    help_page = api_terms_of_use_get()
    serializer = WebPageSerializer(help_page)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message': 'Serialization fail'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_staff_member_required()
def terms_of_use_post(request):
    """
    Post the terms of use
    :param request:
    :return:
    """
    try:
        # Get parameters
        help_content = request.DATA['content']
        try:
            help_page_content = api_terms_of_use_post(help_content)

            # Serialize the request
            serializer = WebPageSerializer(help_page_content)

            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                content = {'message': 'Serialization fail'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {'message': 'Expected parameters not provided.'}
        # logger.exception(e.message)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def terms_of_use(request):
    """
    Terms of Use
    :param request:
    :return:
    """
    if request.method == 'GET':
        return terms_of_use_get(request)
    elif request.method == 'POST':
        return terms_of_use_post(request)
