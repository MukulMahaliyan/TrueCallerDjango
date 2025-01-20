from rest_framework import serializers
from FindCallerApp.models import CustomUser , SpamReport ,Contact
from django.contrib.auth.hashers import make_password






# for serialization of user model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'phone_number'] 



# for deserialization of registration data 
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'password']

   
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already exists.")
        return value

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number is already in use.")
        return value
    
class SpamReportSerializer(serializers.ModelSerializer):
   #  spam_likelihood = serializers.SerializerMethodField()
     
     class Meta:
        model = SpamReport
        fields = ['created_by', 'phone_number']

  

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['contact_name', 'contact_phone_number']

