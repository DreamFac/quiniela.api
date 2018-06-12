from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

class UserProfile(BaseModel):

    user = models.OneToOneField('auth.User', related_name='user_profile',on_delete=models.DO_NOTHING)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    country =  models.CharField(max_length=150)