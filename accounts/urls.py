from django.urls import path,include
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloAPIView.as_view(), name='hello-api'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('get_user_profile/', GetUserProfileView.as_view(), name='get_user_profile'),
    path('send_otp/', PostPhoneNumberView.as_view(), name='send_otp'),
    path('verify_otp/', VerifyOtpView.as_view(), name='verify_otp'),    
    # path('myprofileimages/', MyProfileImagesListCreateView.as_view(), name='myprofileimages-list-create'),
    # path('myprofileimages/<int:pk>/', MyProfileImagesRetrieveUpdateDestroyView.as_view(), name='myprofileimages-detail'),
    path('myimages/', MyImagesListCreateView.as_view(), name='myimages-list-create'),
    path('myimages/<int:pk>/', MyImagesRetrieveUpdateDestroyView.as_view(), name='myimages-detail'),
    path('mystatusimages/', MyStatusImagesListCreateView.as_view(), name='my-status-images-list-create'),
    path('mystatusimages/<int:pk>/', MyStatusImagesRetrieveUpdateDestroyView.as_view(), name='my-status-images-detail'),
]