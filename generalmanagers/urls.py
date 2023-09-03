from django.urls import path,include
from .views import *

urlpatterns = [
   path("dashboard/",dashboard,name="generalmanagersdashboard"),
   path("customers/",state_customers,name="statecustomers"),
   path("loans/",state_loans,name="stateloans"),
   path("customers/search/", customer_search,name="generalcustomersearch"),
   path("customers/loans/",loan_search,name="generalloansearch"),
   path('state/branches/',branches,name="branches")
]
