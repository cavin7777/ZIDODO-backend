from rest_framework import serializers
from django.contrib.auth import get_user_model

from myapp.models import Location, Quest, Reward

User = get_user_model()


# ==========================
# LOCATION SERIALIZER
# ==========================
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

# ==========================
# QUEST SERIALIZER
# ==========================
class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = '__all__'

# ==========================
# REWARD SERIALIZER
# ==========================
class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

# ==========================
# REGISTRATION SERIALIZER
# ==========================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        # ✅ Use create_user to hash password
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
 

# ==========================
# GENERAL USER SERIALIZER (for listing/profile)
# ==========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']