""" rest api views
"""

import logging

from django.http import Http404
from django.utils.decorators import method_decorator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    OpenApiParameter,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required
import core_website_app.components.account_request.api as account_request_api
from core_website_app.rest.account_request.abstract_views import (
    AbstractActionAccountRequest,
)
from core_website_app.rest.account_request.serializers import (
    AccountRequestSerializer,
    UserSerializer,
)

logger = logging.getLogger("core_website_app.rest.account_request.views")


@extend_schema(
    tags=["Account Request"],
    description="Create or get all Account Request",
)
class AccountRequestList(APIView):
    """Create or get all Account Request"""

    @extend_schema(
        summary="Get all account requests",
        description="Get all account requests",
        responses={
            200: AccountRequestSerializer(many=True),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def get(self, request):
        """Get all account requests
        Args:
            request: HTTP request
        Returns:
            - code: 200
              content: List of account requests
            - code: 500
              content: Internal server error
        """
        try:
            account_request_list = account_request_api.get_all()
            # Serialize object
            serializer = AccountRequestSerializer(
                account_request_list, many=True
            )
            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Create a new account request",
        description="Create a new account request",
        request=UserSerializer,
        responses={
            201: AccountRequestSerializer,
            400: OpenApiResponse(
                description="Validation error / missing parameters"
            ),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def post(self, request):
        """Create a new account request
        Parameters:
            {
              "username": "username",
              "first_name": "first_name",
              "last_name": "last_name",
              "password": "password",
              "email": "email"
            }
        Args:
            request: HTTP request
        Returns:
            - code: 201
              content: Account Request
            - code: 400
              content: Validation error / missing parameters
        """
        try:
            # Build serializer
            serializer = UserSerializer(data=request.data)
            # Validate request
            serializer.is_valid(raise_exception=True)
            # Save request
            account_request = serializer.save()
            # Account request serializer
            account_request_serializer = AccountRequestSerializer(
                account_request
            )
            # Return the serialized user request
            return Response(
                account_request_serializer.data, status=status.HTTP_201_CREATED
            )
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Account Request"],
    description="Get an Account Request",
)
class AccountRequestDetail(APIView):
    """Get an Account Request"""

    def get_object(self, pk):
        """Get Account Request from db
        Args:
            pk: ObjectId
        Returns:
            Account Request
        """
        try:
            return account_request_api.get(pk)
        except exceptions.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Retrieve an Account Request",
        description="Retrieve an Account Request",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="AccountRequest ID",
            ),
        ],
        responses={
            200: AccountRequestSerializer,
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def get(self, request, pk):
        """Retrieve an Account Request
        Parameters:
            {
              "pk": "account_request_id"
            }
        Args:
            request: HTTP request
            pk: ObjectId
        Returns:
            - code: 200
              content: Account Request
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            account_request_object = self.get_object(pk)
            # Serialize object
            serializer = AccountRequestSerializer(account_request_object)
            # Return response
            return Response(serializer.data)
        except Http404:
            content = {"message": "Account request not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Account Request"],
    description="Deny an Account Request",
)
class AccountRequestDeny(AbstractActionAccountRequest):
    """Deny an Account Request"""

    @extend_schema(
        summary="Deny an Account Request",
        description="Deny an Account Request",
        request=None,
        responses={
            200: OpenApiResponse(description="Account request denied"),
            404: OpenApiResponse(description="Account request not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def perform(self, account_request_object):
        """Deny an Account Request
        Args:
            account_request_object: account_request
        """
        account_request_api.deny(account_request_object)


@extend_schema(
    tags=["Account Request"],
    description="Accept an Account Request",
)
class AccountRequestAccept(AbstractActionAccountRequest):
    """Accept an Account Request"""

    @extend_schema(
        summary="Accept an Account Request",
        description="Accept an Account Request",
        request=None,
        responses={
            200: OpenApiResponse(description="Account request accepted"),
            404: OpenApiResponse(description="Account request not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def perform(self, account_request_object):
        """Accept an Account Request
        Args:
            account_request_object: account_request
        """
        account_request_api.accept(account_request_object)
