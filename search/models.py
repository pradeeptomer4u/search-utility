from django.db import models

# Create your models here.
class Products(models.Model):
    TYPE=(
        ('S','Shop Clues'),
        ('P', 'Paytm Mall'),
        ('T', 'Tata Cliq')
    )
    product_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    catagory_name= models.CharField(max_length=255,blank=True,null=True)
    instock = models.BooleanField(default=True)
    catagory_id = models.CharField(max_length=255, blank=True, null=True)
    sub_catagory_name= models.CharField(max_length=255,blank=True,null=True)
    discounted_price = models.CharField(max_length=255, blank=True, null=True)
    vendor = models.CharField(max_length=1,choices=TYPE,default='P')
    price= models.CharField(max_length=255)
    image_url= models.CharField(max_length=255)
    product_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True,blank=True, null=True)

    class Meta:
        unique_together = ('product_id', 'product_name')

