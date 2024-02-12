from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpRequest
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from social_django.utils import psa
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .regesterUser import regesterUser
from .getAccessToken import getAccessToken
import json
import random

class HelloAPIView(APIView):
    authentication_classes =[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    
    renderer_classes = [JSONRenderer]
    def get(self, request):
        return Response({'message': 'Hello, this is your first API!'})
# //////////////////////////////////////////////////////

#  below logic for sign up api
class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
# ////////////////////////////////////////////////////////////////

def generate_otp():
    # Generate a 6-digit OTP
    otp = random.randint(100000, 999999)
    return otp

# //////////////////////////////////////////
# /////////////////send otp , verify otp , regester user////////////

class PostPhoneNumberView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract number from the request data
        number = request.data.get('number')

        # Check if the number already exists in the database
        try:
            phone_number_instance = PhoneNumber.objects.get(number=number)
            # If the number exists, update the OTP
            # otp = 111111
            otp = generate_otp()
            phone_number_instance.otp = otp
            phone_number_instance.save()
            jsonResponse={
                'status': True,
                'message': 'OTP sent successfully',
                'data': []
                }            
            return Response(jsonResponse, status=status.HTTP_200_OK)
        except PhoneNumber.DoesNotExist:
            # If the number doesn't exist, create a new record with a new OTP
            otp = generate_otp()
            # otp = 111111
            serializer = PhoneNumberSerializer(data={'number': number, 'otp': otp})
            if serializer.is_valid():
                serializer.save()
                jsonResponse={
                'status': True,
                'message': 'OTP sent successfully',
                'data': []
                }            
                return Response(jsonResponse, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOtpView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract number from the request data
        number = request.data.get('number')
        otp = request.data.get('otp')
        # print (otp)
        # verify number and otp
        try:
            PhoneNumber.objects.get(number=number)
            try:
                PhoneNumber.objects.get(number=number, otp=otp)
                newRegestrationFlag=True
                msg1 = regesterUser(number)
                # Check if the response contains the "number" key and the desired message
                if isinstance(msg1, str):
                    json_response = json.loads(msg1)
                    if 'number' in json_response and 'This number is already in use.' in json_response['number']:
                        newRegestrationFlag=False
                        msg1 = {"msg": "login successful"}
                    else:
                        msg1 = json_response  # Use the original response if conditions are not met
                msg2 = getAccessToken(number)
                # json_msg1 = json.dumps(msg1, indent=2)  # Convert msg1 to a JSON-formatted string
                # Proceed with the rest of your code
                json_msg2 = json.loads(msg2)
                # Construct the final JSON response
                jsonResponse={
                'status': True,
                'message': 'verification success',
                'newRegestration':newRegestrationFlag,
                'data': [{
                    'regestrationMsg': msg1,
                    'otpVerificationMsg': 'verification success',
                    'accessToken': json_msg2,
                }]
                }                                             
                return Response(jsonResponse, status=status.HTTP_200_OK)
            except:
                jsonResponse={
                'status': False,
                'message': 'otp verification failed',
                'data': []
                }                                             
                return Response(jsonResponse, status=status.HTTP_200_OK)    
            # If the number exists, update the OTP
        except PhoneNumber.DoesNotExist:
            # If the number doesn't exist, 
            return Response({'message': 'user not exist please sign up'}, status=status.HTTP_201_CREATED)
        
# ////////////////////////// update profile api/////////////////

def get_my_images_url(user_name, request: HttpRequest):
    my_images = MyImages.objects.filter(userName=user_name)

    if my_images.exists():
        image_urls = [
            {'userName': image.userName, 'image_url': request.build_absolute_uri(image.image_file)}
            for image in my_images
        ]
        return image_urls
    else:
        return None



from django.http import HttpRequest
from .models import CustomUser

def get_my_profile_images_url(user_name, request: HttpRequest):
    try:
        user = CustomUser.objects.get(username=user_name)
        if user.profile_image:
            return request.build_absolute_uri(user.profile_image.url)
    except CustomUser.DoesNotExist:
        pass  # Handle the case where the user doesn't exist or has no profile image
    return None  # Return None if the user doesn't exist or has no profile image


# def get_my_profile_images_url(user_name, request: HttpRequest):
    # profile_image = CustomUser.objects.filter(userName=user_name)

    # if profile_image.exists():
    #     image_urls = [
    #         {'userName': image.userName, 'image_url': request.build_absolute_uri(image.image_file)}
    #         for image in profile_image
    #     ]
    #     return image_urls
    # else:
    #     return None
    # return None

def get_my_status_images_url(user_name, request: HttpRequest):
    my_images = MyStatusImages.objects.filter(userName=user_name)

    if my_images.exists():
        image_urls = [
            {'userName': image.userName, 'image_url': request.build_absolute_uri(image.image_file)}
            for image in my_images
        ]
        return image_urls
    else:
        return None

class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        responce=serializer.data
        # responce['my_profile_images']=get_my_profile_images_url(responce.get('username'), request)
        responce['my_images']=get_my_images_url(responce.get('username'), request)
        responce['my_status_images']=get_my_status_images_url(responce.get('username'), request)

        jsonResponse={
                'status': True,
                'message': 'user profile retrieve.',
                'data': [responce]
                }            
            
        return Response(jsonResponse, status=status.HTTP_200_OK)
        
    def put(self, request):
        serializer = UpdateUserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            jsonResponse={
            'status': True,
            'message': 'user updated successfully.',
            'data': serializer.data
            }            

            return Response(jsonResponse, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        jsonResponse={
            'status': True,
            'message': 'User deleted successfully.',
            'data': []
            }            
        return Response(jsonResponse, status=status.HTTP_200_OK)

# ////////////////////////// myProfileImages Api
class CustomResponseMixin:
    def get_response_data(self, status, message, data=None):
        return {
            "status": status,
            "message": message,
            "data": data
        }


# class MyProfileImagesListCreateView(CustomResponseMixin, APIView):
#     serializer_class = MyProfileImagesSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         username = request.query_params.get('username', None)
#         if username is not None:
#             queryset = ProfileImage.objects.filter(userName=username)
#             serializer = MyProfileImagesSerializer(queryset, many=True)
#             data = self.get_response_data(True, "data retrieved.", serializer.data)
#             return Response(data)
#         return Response([])  # Adjust as needed if you want a different response when no username is provided

#     def post(self, request, format=None):
#         serializer = MyProfileImagesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             data = self.get_response_data(True, "Image created successfully.", serializer.data)
#             return Response(data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MyProfileImagesRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
#     queryset = ProfileImage.objects.all()
#     serializer_class = MyProfileImagesSerializer
#     permission_classes = [IsAuthenticated]

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         data = self.get_response_data(True, "Image deleted successfully.",None)
#         return Response(data, status=status.HTTP_200_OK)

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         data = self.get_response_data(True, "Image updated successfully.", serializer.data)
#         return Response(data)

# ////////////////////////// myImages Api

class MyImagesListCreateView(CustomResponseMixin, APIView):
    serializer_class = MyImagesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        username = request.query_params.get('username', None)
        if username is not None:
            queryset = MyImages.objects.filter(userName=username)
            serializer = MyImagesSerializer(queryset, many=True)
            data = self.get_response_data(True, "data retrieved.", serializer.data)
            return Response(data)
        return Response([])  # Adjust as needed if you want a different response when no username is provided

    def post(self, request, format=None):
        serializer = MyImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = self.get_response_data(True, "Image created successfully.", serializer.data)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyImagesRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = MyImages.objects.all()
    serializer_class = MyImagesSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = self.get_response_data(True, "Image deleted successfully.",None)
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = self.get_response_data(True, "Image updated successfully.", serializer.data)
        return Response(data)

# /////////////////////////////////////// my status images API

class MyStatusImagesListCreateView(CustomResponseMixin, APIView):
    serializer_class = MyStatusImagesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        username = request.query_params.get('username', None)
        if username is not None:
            queryset = MyStatusImages.objects.filter(userName=username)
            serializer = MyStatusImagesSerializer(queryset, many=True)
            data = self.get_response_data(True, "data retrieved.", serializer.data)
            return Response(data)
        return Response([])  # Adjust as needed if you want a different response when no username is provided

    def post(self, request, format=None):
        serializer = MyStatusImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = self.get_response_data(True, "Image created successfully.", serializer.data)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyStatusImagesRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = MyStatusImages.objects.all()
    serializer_class = MyStatusImagesSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = self.get_response_data(True, "Image deleted successfully.",None)
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = self.get_response_data(True, "Image updated successfully.", serializer.data)
        return Response(data)

