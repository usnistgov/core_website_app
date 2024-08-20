""" Serializers used throughout the Contact Message Rest API
"""

from rest_framework.serializers import ModelSerializer

from core_website_app.components.contact_message.models import ContactMessage


class ContactMessageSerializer(ModelSerializer):
    """Represents the contact message serializer"""

    class Meta:
        """Meta"""

        model = ContactMessage
        fields = ["id", "name", "email", "content"]
        read_only_fields = ("id",)
