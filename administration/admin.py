from django.contrib import admin
from .models import Customers,Loan,PaymentDay,Branch,State,LoanApply,Paid

# Register your models here.

admin.site.register(Customers)
admin.site.register(Loan)
admin.site.register(PaymentDay)
admin.site.register(Branch)
admin.site.register(State)
admin.site.register(LoanApply)
admin.site.register(Paid)