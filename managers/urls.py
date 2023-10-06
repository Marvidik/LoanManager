
from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard",dashboard,name="manager-dashboard"),
    path("branch/customers/",branch_customer,name="branchcustomers"),
    path("branch/customers/search/",branch_customer_search,name="branchsearch"),
    path("branch/customers/loan/",branch_loans,name="branchloans"),
    path("branch/customers/loan-search",loan_search,name="loansearch"),
    path("branch/add_customer/",add_customer,name="add_customer"),
    path("branch/applied_loans/",applied,name="branchapplied"),
    path("branch/apply-loan/",process_application,name="apply"),
    path('branch/dates/',dates,name="datesss"),
    path("branch/dates/<int:paymentday_id>/",payment_day_details,name='payment_day_detailsss')

    
]