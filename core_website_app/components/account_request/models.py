""" Account requests model
"""

import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions


class AccountRequest(models.Model):
    """Represents a request sent by a user to get an account"""

    username = models.CharField(
        blank=False, max_length=200
    )  #: Username associated with the request
    first_name = models.CharField(blank=False, max_length=200)
    last_name = models.CharField(blank=False, max_length=200)
    email = models.CharField(blank=False, max_length=200)
    date = models.DateTimeField(default=datetime.datetime.now, blank=False)

    @staticmethod
    def get_by_id(request_id):
        """Get a request given its primary key

        Parameters:
            request_id (str): Primary key of the request

        Returns:
            Request object corresponding to the given id
        """
        try:
            return AccountRequest.objects.get(pk=str(request_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Get all Account Request

        Returns:

        """
        return AccountRequest.objects.all()
