from django.db import models
from django.db.models import Manager 
from datetime import date, time, datetime


# Create your models here.

class Custommanager(models.Manager):     
    def filterdata(self, a):
        return super().get_queryset().filter(location=a)

class Service(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media")
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=50)
    provider = models.CharField(max_length=50)
    location = models.CharField(max_length=50, default='location')
    price = models.FloatField()
    duration = models.FloatField()
    rating = models.FloatField(default='3.0')
    review = models.CharField(max_length=100, default='review')
    additional_info = models.CharField(max_length=300, default='additional info')

    cserviceobj = Custommanager()
    objects = Manager()

    class Meta:
        db_table = 'service'

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=500)    
    usertype = models.CharField(max_length=50)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50, default='area')
    city = models.CharField(max_length=50, default='city')
    state = models.CharField(max_length=50, default='state')
    pincode = models.BigIntegerField()
    contact = models.BigIntegerField()

    class Meta:
        db_table = 'user'

class SPService(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media")
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=50)
    provider = models.CharField(max_length=50)
    location = models.CharField(max_length=50, default='location')
    price = models.FloatField()
    duration = models.FloatField()   
    status = models.CharField(max_length=50, default='pending')
    rating = models.FloatField(default='3.0')
    review = models.CharField(max_length=100, default='review')
    additional_info = models.CharField(max_length=300, default='additional info')
  
    
    cspserviceobj = Custommanager()
    objects = Manager()

    class Meta:
        db_table = 'spservice'


class cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_id = models.ForeignKey(SPService, on_delete=models.CASCADE)
    service_date = models.DateField()
    service_time = models.TimeField()
    totalamount = models.FloatField()
    status = models.CharField(max_length=50, default='pending') 
    

    class Meta:
        db_table='cart'

class Booking(models.Model):        
    booking_number = models.CharField(max_length=100)
    booking_date = models.DateField(auto_now=True)
    booking_time = models.TimeField(auto_now=True)
    booking_status = models.CharField(max_length=100, default='pending') 
    cart_id = models.ForeignKey(cart, on_delete=models.CASCADE, default="")      

    class Meta:
        db_table = 'booking'

class Order(models.Model):
    ordernumber = models.CharField(max_length=100)
    orderdate = models.DateField(max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phonenumber = models.BigIntegerField()
    pincode = models.BigIntegerField()
    orderstatus = models.CharField(max_length=50)

    class Meta:
        db_table = 'order'

class Payment(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    paymentmode = models.CharField(max_length=100, default='paypal')
    paymentstatus = models.CharField(max_length=100, default='pending')
    transactionid = models.CharField(max_length=200)    

    class Meta:
        db_table = 'payment'

class Orderdetail(models.Model):    
    ordernumber = models.CharField(max_length=100)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    serviceid = models.ForeignKey(SPService, on_delete=models.CASCADE)   
    totalprice = models.IntegerField()
    paymentid = models.ForeignKey(Payment, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'orderdetail'