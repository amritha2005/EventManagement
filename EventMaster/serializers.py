from rest_framework import serializers
from django.contrib.auth.models import User
from EventMaster.models import CategoryDb, EventDb, BookingDb

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryDb
        fields = '__all__'
class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventDb
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDb
        fields = '__all__'
        read_only_fields = [
            'created_by',
            'booking_date',
            'total_amount'
        ]