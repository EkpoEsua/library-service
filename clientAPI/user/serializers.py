import imp
from rest_framework import serializers
from user.models import User
from source import emit_command
import json


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )

    def save(self, **kwargs):
        instance: User = super().save(**kwargs)
        instance_dict: dict = instance.__dict__
        instance_dict.pop("_state")
        emit_command(json.dumps(instance_dict), "adminapi.register_user")
        return instance
