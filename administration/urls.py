from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("dashboard/",dashboard,name="dashboard"),
    path("customers/",customers,name="customer_details"),
    path("profile/<int:customer_id>/",customer_details,name="detail"),
    path("loans/",loan_table,name="loans"),
    path("add_payment/",process_payment,name="payment"),
    path("general-manager_signup/",register_view,name="register"),
    path("manager_sign_up/",manager_sign_up,name="managersignup"),
    path('states/',states,name="states"),
    path('states/<int:state_id>/',state_detail, name='state-detail'),
    path('allsearch/',gsearch_users, name='gsearch_users'),
    path('allloan/',asearch_customer_loans, name='allloan_users'),
    path('applied_loans/',applied_loans,name="applied"),
    path('approve_loan/<int:loan_id>/', approve_loan, name='approve_loan'),
    path('reject_loan/<int:loan_id>/', reject_loan, name='reject_loan'),
    path('search/appliedloans/',search_applied_loans,name="searchapplied"),
    path("dates/",dates,name="dates"),
    path('dates/<int:paymentday_id>/', payment_day_details, name='payment_day_details'),
    path("registered/",reg_redirect,name="reg_redirect"),
    
 ]

# urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
