from django.contrib import admin
from .models import Customers,Loan,Payment,Branch,State,LoanApply

# Register your models here.

admin.site.register(Customers)
admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(Branch)
admin.site.register(State)
admin.site.register(LoanApply)