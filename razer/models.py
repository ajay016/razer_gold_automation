from django.db import models

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8)
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
    STATUS_CHOICES = [
        (0, 'Pending'),   # Red
        (1, 'Received'),  # Blue
        (2, 'Checked'),   # Green
    ]

    name = models.CharField(max_length=255)
    product_url = models.URLField()  # Common for all variants
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    is_scheduled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    regions = models.ManyToManyField(Region, related_name='product_variants')

    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
    
class ProductSchedule(models.Model):
    REPEAT_CHOICES = [
        ('none', 'No Repeat'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='schedules')
    quantity = models.PositiveIntegerField(default=1)
    scheduled_time = models.DateTimeField()
    repeat = models.CharField(max_length=20, choices=REPEAT_CHOICES, default='none')
    is_active = models.BooleanField(default=True)
    last_run_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} scheduled at {self.scheduled_time}"