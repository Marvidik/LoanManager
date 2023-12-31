from django.db import models
from django.contrib.auth.models import User
from managers.models import Manager
from generalmanagers.models import GeneralManager
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
status_choices=[
    ("active","active"),
    ("inactive","inactive")
]

class State(models.Model):
    name=models.CharField(max_length=100,unique=True)
    general_manager=models.OneToOneField(GeneralManager,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name=models.CharField(max_length=100)
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    manager=models.OneToOneField(Manager,on_delete=models.CASCADE,null=True)


    def __str__(self):

        return self.name

class Customers(models.Model):
    name=models.CharField(max_length=100)
    branch=models.ForeignKey(Branch,on_delete=models.PROTECT,null=True,default=None)
    gender=models.CharField(max_length=100, null=True)
    occupation=models.CharField(max_length=100, null=True)
    state=models.CharField(max_length=100, null=True)
    passport=models.ImageField()
    business_name=models.CharField(max_length=100)
    bussiness_address=models.CharField(max_length=100)
    age=models.IntegerField()
    phone_number=models.IntegerField(null=True)
    home_address=models.CharField(max_length=100)
    card_number=models.IntegerField()
    

    guarantors_name=models.CharField(max_length=100)
    guarantors_phone=models.IntegerField()
    guarantors_address=models.CharField(max_length=100)
    goccupation=models.CharField(max_length=100,null=True)
    gstate=models.CharField(max_length=100,null=True)

    def __str__(self):

        return self.name
    
class Loan(models.Model):
    loanee=models.ForeignKey(Customers,on_delete=models.CASCADE)
    amount_collected=models.IntegerField()
    amount_paid=models.IntegerField()
    due_date=models.DateTimeField()
    status=models.CharField(max_length=100,choices=status_choices,default="active")
    due=models.BooleanField()
    expected_payment_days=models.IntegerField(default=25)

    def update_amount_paid(self):
        paid_amount = Paid.objects.filter(loan=self).aggregate(total_amount=models.Sum('amount'))['total_amount']
        self.amount_paid = paid_amount + self.amount_paid or 0
        self.save()

    def __str__(self):

        return self.loanee.name

class PaymentDay(models.Model):
    payment_date=models.DateField()


class Paid(models.Model):
    paymentday=models.ForeignKey(PaymentDay,on_delete=models.CASCADE)
    amount=models.IntegerField()
    loan=models.ForeignKey(Loan,on_delete=models.CASCADE)




class LoanApply(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    amount=models.IntegerField()
    status=models.CharField(max_length=100,choices=[
    ("Approved","Approved"),
    ("Pending","Pending"),
    ("Rejected","Rejected")
])

    def __str__(self):

        return self.customer.name

