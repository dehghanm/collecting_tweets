from django.db import transaction
from rest_framework import serializers

from core.models import TwitterAccount


class GetAllAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterAccount
        fields = ["uuid", "username", "orientation"]


class AccountsManagementSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super(AccountsManagementSerializer, self).__init__(*args, **kwargs)
        self.action = self.initial_data.get("action")
        if self.action and self.action in ["add", "update", "delete"]:
            if self.action == "add":
                self.fields["uuid"].allow_null = True
            elif self.action == "delete":
                self.fields["username"].allow_null = True
                self.fields["orientation"].allow_null = True
        else:
            raise serializers.ValidationError(
                {"action": "action is required. valid values : 1.add, 2.update, 3.delete."}
            )

    action = serializers.CharField(max_length=6)
    uuid = serializers.UUIDField(format='hex_verbose')
    username = serializers.CharField(max_length=200)
    orientation = serializers.IntegerField()

    def validate_uuid(self, value):
        if value and self.action in ["update", "delete"]:
            try:
                account = TwitterAccount.objects.get(uuid=value)
            except:
                raise serializers.ValidationError("account uuid is not valid.")
            else:
                return value
        return value

    def validate_username(self, value):
        if value and self.action in ["add"]:
            try:
                already_exist_account = TwitterAccount.objects.get(username=value)
            except:
                return value
            else:
                raise serializers.ValidationError("username already taken.")

        return value

    def validate_orientation(self, value):
        if value and self.action in ["add", "update"]:
            if value in [0, 1, 2]:
                return value
            else:
                raise serializers.ValidationError("orientation is not valid .")
        return value

    def validate(self, data):
        if self.action == "update":
            all_accounts_except_updating = TwitterAccount.objects.exclude(uuid=data["uuid"]).filter(
                username=data["username"]
            )
            if all_accounts_except_updating.exists():
                raise serializers.ValidationError({"username": "username already taken."})

        return data

    @staticmethod
    def add_new_account(**kwargs):
        new_account = TwitterAccount.objects.create(
            username=kwargs["username"],
            orientation=kwargs["orientation"]
        )
        return new_account

    @staticmethod
    def update_account(**kwargs):
        updating_account = TwitterAccount.objects.get(uuid=kwargs["uuid"])
        updating_account.username = kwargs["username"]
        updating_account.orientation = kwargs["orientation"]
        updating_account.save()

    @staticmethod
    def delete_account(**kwargs):
        TwitterAccount.objects.get(uuid=kwargs["uuid"]).delete()

    @transaction.atomic
    def do_action(self):
        if self.action == "add":
            new_account = self.add_new_account(**self.validated_data)
            response_message = {
                "message": "new account added successfully.",
                "new_account_uuid": str(new_account.uuid)
            }
            return response_message

        elif self.action == "update":
            self.update_account(**self.validated_data)
            response_message = {
                "message": "account updated successfully.",
            }
            return response_message

        elif self.action == "delete":
            self.delete_account(**self.validated_data)
            response_message = {
                "message": "account deleted successfully.",
            }
            return response_message
