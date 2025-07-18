from django.db import models

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name
    
    

class UserAccount(models.Model):
    STATUS_CHOICES = [ 
        (0, 'Offline'),
        (1, 'Online'),
    ]  
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=255)  # Not a real password field
    auth_key = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='users')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    session_path = models.CharField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.name
    
    

class Product(models.Model):
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    user_account = models.ForeignKey('UserAccount', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=255)
    product_url = models.URLField()
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name