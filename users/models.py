from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 100, unique = True)
    password = models.CharField(max_length = 200)
    mobile_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    email_subscription = models.BooleanField()
    membership_point = models.PositiveIntegerField()
    pet_type = models.ForeignKey('PetType', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name 


class PetType(models.Model):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'pet_types'

    def __str__(self):
        return self.name 
