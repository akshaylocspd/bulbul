from django.contrib.auth.models import AbstractUser
from django.db import models
# class ProfileImage(models.Model):
#     userName = models.CharField(max_length=15, blank=True, null=True)
#     image_file = models.ImageField(upload_to='userImages/',blank=True, null=True,)    
#     def __str__(self):
#         # return self.image_file
#         return  str(self.image_file)
#     def get_image_url(self, request):
#         return request.build_absolute_uri(self.image_file.url)
class MyImages(models.Model):
    userName = models.CharField(max_length=15, blank=True, null=True)
    image_file = models.ImageField(upload_to='userImages/',blank=True, null=True,)    
    def __str__(self):
        # return self.image_file
        return  str(self.image_file)
    def get_image_url(self, request):
        return request.build_absolute_uri(self.image_file.url)

class MyStatusImages(models.Model):
    userName = models.CharField(max_length=15, blank=True, null=True)
    image_file = models.ImageField(upload_to='userImages/',blank=True, null=True,)    
    def __str__(self):
        # return self.image_file
        return  str(self.image_file)
    def get_image_url(self, request):
        return request.build_absolute_uri(self.image_file.url)

# profile_image = models.OneToOneField(ProfileImage,on_delete=models.CASCADE, blank=True, null=True)
    
class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    my_images = models.ManyToManyField(MyImages, blank=True,related_name='my_images')
    my_status_images = models.ManyToManyField(MyStatusImages, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    about_you = models.CharField(max_length=255, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    interest1 = models.CharField(max_length=50, blank=True, null=True)	
    interest2 = models.CharField(max_length=50, blank=True, null=True)	
    interest3 = models.CharField(max_length=50, blank=True, null=True)	
    interest4 = models.CharField(max_length=50, blank=True, null=True)	
    interest5 = models.CharField(max_length=50, blank=True, null=True)	
    nameUser = models.CharField(max_length=30, blank=True, null=True)
    forum_posts = models.PositiveIntegerField(default=0)
    photos_added = models.PositiveIntegerField(default=0)
    favorites = models.PositiveIntegerField(default=0)

    groups = models.ManyToManyField(
        "auth.Group", related_name="customuser_set", related_query_name="customuser", blank=True, help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="customuser_set", related_query_name="customuser", blank=True, help_text="Specific permissions for this user.",
    )

    def __str__(self):
        return self.username
# below code no need to register in admin.py its only for otp verification
# for storing otp and number
    
from django.db import models
class PhoneNumber(models.Model):
    number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.number
