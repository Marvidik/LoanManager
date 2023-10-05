
from django.urls import path
from .views import *
from administration.views import dates 

urlpatterns = [
    path("dashboard",dashboard,name="manager-dashboard"),
    path("branch/customers/",branch_customer,name="branchcustomers"),
    path("branch/customers/search/",branch_customer_search,name="branchsearch"),
    path("branch/customers/loan/",branch_loans,name="branchloans"),
    path("branch/customers/loan-search",loan_search,name="loansearch"),
    path("branch/add_customer/",add_customer,name="add_customer"),
    path("branch/applied_loans/",applied,name="branchapplied"),
    path("branch/apply-loan/",process_application,name="apply"),
    path("branch/date/",dates,name="bracnch-date"),

    
]