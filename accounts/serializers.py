# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from .models import *

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Customize token payload if needed
        # token['custom_field'] = user.custom_field
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Check if the user is active
        user = self.user
        if not user.is_active:
            raise AuthenticationFailed('User account is not active.')

        return data

# ///////// register user

class UserSerializer(serializers.ModelSerializer):
    # profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser                
        fields = [ 'number','email','username', 'password', 'about_you', 'bio', 'interest1', 'interest2', 'interest3', 'interest4', 'interest5', 'nameUser', 'forum_posts', 'photos_added', 'favorites','profile_image',]
        extra_kwargs = {'password': {'write_only': True}}

    # def get_profile_image_url(self, user):
    #     if user.profile_image and user.profile_image.get_image_url:
    #         return self.context['request'].build_absolute_uri(user.profile_image.get_image_url(self.context['request']))
    #     return None
    
    
    def validate_number(self, value):
        # Check if the number already exists in the database.
        if CustomUser.objects.filter(number=value).exists():
            raise serializers.ValidationError("This number is already in use.")
        return value
    # Check if the EMAIL already exists in the database.

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['number','otp']

# ////////////update profile //////////////////////////////
        
class UpdateUserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    about_you = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    interest1 = serializers.CharField(required=False)
    interest2 = serializers.CharField(required=False)
    interest3 = serializers.CharField(required=False)
    interest4 = serializers.CharField(required=False)
    interest5 = serializers.CharField(required=False)
    nameUser = serializers.CharField(max_length=30, required=False)
    forum_posts = serializers.IntegerField(required=False)
    photos_added = serializers.IntegerField(required=False)
    favorites = serializers.IntegerField(required=False)
    profile_image = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        # Update user profile based on validated data
        instance.bio = validated_data.get('bio', instance.bio)
        instance.forum_posts = validated_data.get('forum_posts', instance.forum_posts)
        instance.photos_added = validated_data.get('photos_added', instance.photos_added)
        instance.favorites = validated_data.get('favorites', instance.favorites)
        instance.about_you = validated_data.get('about_you', instance.about_you)
        instance.email = validated_data.get('email', instance.email)
        instance.nameUser = validated_data.get('nameUser', instance.nameUser)
        
        instance.interest1 = validated_data.get('interest1', instance.interest1)
        instance.interest2 = validated_data.get('interest2', instance.interest2)
        instance.interest3 = validated_data.get('interest3', instance.interest3)
        instance.interest4 = validated_data.get('interest4', instance.interest4)
        instance.interest5 = validated_data.get('interest5', instance.interest5)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        
        
        # Update profile image if provided
        profile_image = validated_data.get('profile_image_url', None)
        if profile_image:
            instance.profile_image_url = profile_image

        # Save the changes
        instance.save()
        return instance


# //////////////////////////////////////////  my_profile_images
# class MyProfileImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProfileImage
#         fields = '__all__'

# //////////////////////////////////////////  myimages

class MyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyImages
        fields = '__all__'
    
# ///////////////////////////////// my status images 
class MyStatusImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyStatusImages
        fields = '__all__'
