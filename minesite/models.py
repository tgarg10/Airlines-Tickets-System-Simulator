from functools import total_ordering
from django.db.models import *

# Create your models here.
class LoginModel(Model):
    username = CharField(max_length=32)
    password = CharField(max_length=32)
    name = CharField(max_length=32)
    email = EmailField(max_length=32, null = True)

    class Meta:
        db_table = "User_Details"
        
class FlightDetails(Model):
    date = DateField()
    code = CharField(max_length=6)
    time = TimeField()
    fromplace = CharField(max_length=32)
    toplace = CharField(max_length=32)
    e_numseats = IntegerField()
    b_numseats = IntegerField()
    e_price = IntegerField()
    b_price = IntegerField()
    status = CharField(max_length=12, default="CONFIRMED")

    class Meta:
        db_table = "Flight_Details"

class Transactions(Model):
    transaction_num = IntegerField(default=0)
    username = CharField(max_length=32)
    code = CharField(max_length=6)
    time = TimeField(null=True)
    fromplace = CharField(max_length=32)
    toplace = CharField(max_length=32)
    num_passangers = IntegerField()
    total = IntegerField()
    paymentmode = CharField(max_length=16)
    flightclass = CharField(max_length=8)
    seatnumbers = CharField(max_length=4 , default="")
    mealpreferance = CharField(max_length=16, default="Vegetarian")
    flightdate = DateField(default="2021-06-17")
    flighttime = TimeField(default="12:00:00")

    def __str__(self):
        return self.seatnumbers

    class Meta:
        db_table = "Transactions"
