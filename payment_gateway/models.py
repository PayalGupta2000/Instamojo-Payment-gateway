import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    upadted_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Product(BaseModel):
    product_name=models.CharField(max_length=50)
    product_image=models.ImageField(upload_to="media")
    prduct_price=models.IntegerField()

    def __str__(self):
        return self.product_name
    
class Order(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)
    oredr_id=models.CharField(max_length=500)
    instamojo_response=models.TextField(null=True,blank=True)