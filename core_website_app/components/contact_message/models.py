""" Contact messages models
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions


class ContactMessage(models.Model):
    """Represents a message sent via the Contact form"""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()

    @staticmethod
    def get_by_id(message_id):
        """Get a message using its primary key

        Args:
            message_id:

        Returns:
        """
        try:
            return ContactMessage.objects.get(pk=str(message_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Get all messages

        Returns:
        """
        return ContactMessage.objects.all()
