from rest_framework import serializers
#
from applications.users.models import User
#
from applications.account.models import Account, TypeAccount



# La clase `AccountSerializer` en Python valida la entrada del usuario para crear nuevas cuentas, verificando
# si el usuario existe y si ya tiene una cuenta del tipo especificado.
class AccountSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    account_type = serializers.CharField(required=True, max_length=1)

    def validate(self, data):
        user_exists = User.objects.filter(user_id=data['user_id']).exists()
        
        if not user_exists:
            raise serializers.ValidationError("El usuario no existe")
        
        cuentas = TypeAccount.objects.filter(account__user_id__user_id=data['user_id'])
        for c in cuentas:
            if data['account_type'] == c.account_type:
                raise serializers.ValidationError("El usuario ya tiene una cuenta de ese tipo")
            break     

        return data