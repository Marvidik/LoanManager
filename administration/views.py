from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Sum,Count,Q
from .models import Loan,Customers,State,Branch
from managers.models import Manager
from generalmanagers.models import GeneralManager
from django.contrib.auth import authenticate, login
from .forms import CustomerRegistrationForm
from django.contrib.auth.models import User,Group
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.contrib import messages
from django.views.generic import  ListView
from .decorator import group_required
from django.contrib.auth.decorators import login_required
from administration.models import LoanApply



#  function that renders the admin page for the super user 
@login_required
def dashboard(request):
    customer_loan_data = []
    customers = Customers.objects.all()

    for customer in customers:
        active_loans = Loan.objects.filter(loanee=customer, status='active')
        total_borrowed = active_loans.aggregate(total=Sum('amount_collected'))['total'] or 0
        total_returned = active_loans.aggregate(total=Sum('amount_paid'))['total'] or 0

        if total_borrowed>0:
            ppaid=(total_returned/total_borrowed)*100 or 0
        else:
            ppaid=0
        customer_loan_data.append({
            'customer': customer,
            "image":customer.passport,
            'total_borrowed': total_borrowed,
            'total_returned': total_returned,
            "ppaid":ppaid,
        })

    total_amount = Loan.objects.aggregate(total_amount=Sum('amount_collected'))['total_amount']
    recovered = Loan.objects.aggregate(total_amount=Sum('amount_paid'))['total_amount']
    clients =Customers.objects.count()
    leaders =Manager.objects.count()
    active_loan_users_count = Customers.objects.filter(loan__status='active').annotate(active_loan_count=Count('loan')).filter(active_loan_count__gt=0).count()
   
    
    powing=(active_loan_users_count/clients)*100 or 0

    collected=(recovered/total_amount)*100 or 0

    context={
        "total":total_amount,
        "recovered":recovered,
        "collected":int(collected),
        "clients":clients,
        "leaders":leaders,
        "powing":powing,
        "data":customer_loan_data
    }

    return render(request,"administration/dashboard.html",context)


# function for the all the customers in the platform
@login_required
def customers(request):
    customers = Customers.objects.all()
    customer_loan_data = Customers.objects.annotate(
    total_borrowed=Sum('loan__amount_collected'),
    total_returned=Sum('loan__amount_paid')
).prefetch_related('loan_set')

    for customer in customer_loan_data:
        customer.loans = customer.loan_set.all().values('status', 'due_date')

    context={
        "data":customer_loan_data
    }

    return render(request,"administration/tables.html",context)

@login_required
def customer_details(request, customer_id):
    customer = get_object_or_404(Customers, pk=customer_id)
    loans = customer.loan_set.all()

    context = {
        'customer': customer,
        'loans': loans
    }

    return render(request, 'administration/profile.html', context)

@login_required
def loan_table(request):
    customer_loan_data = []
    customers = Customers.objects.all()

    for customer in customers:
        customer_loan_data = Customers.objects.annotate(
    total_borrowed=Sum('loan__amount_collected'),
    total_returned=Sum('loan__amount_paid'),
    
).prefetch_related('loan_set')
   
    for customer in customer_loan_data:
        if customer.total_borrowed:
            customer.loans = customer.loan_set.all().values('status', 'due_date')
            customer.ppaid =  (customer.total_returned/customer.total_borrowed)*100

    context={
        "data":customer_loan_data
    }

    return render(request,"administration/loans.html",context)


@login_required
def loan_payment(request,customer_id):
    

    customer = get_object_or_404(Customers, pk=customer_id)
    loans = customer.loan_set.all()

    context={
        "range":25,
    }


    return render(request,"administration/payment.html",context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('manager-dashboard')  # Redirect to the dashboard after successful login
        else:
            error_message = "Invalid login credentials. Please try again."

    return render(request, "administration/sign-in.html")

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')
        
        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        new_leader=GeneralManager(name=user)
        new_leader.save()

        # assigns a user to a group
        # leader_group = Group.objects.get(name='leader')
        # user.groups.add(leader_group)

        messages.success(request, "Registration successful. You can now log in.")
        
        return redirect('generalmanagersdashboard')

    return render(request, 'administration/sign-up.html')

def manager_sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('managersignup')
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('managersignup')
        
        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        new_leader=Manager(name=user)
        new_leader.save()

        # assigns a user to a group
        # leader_group = Group.objects.get(name='leader')
        # user.groups.add(leader_group)

        messages.success(request, "Registration successful. You can now log in.")
        
        return redirect('manager-dashboard')

    return render(request, "administration/sign-up.html")

def add_customer(request):
    
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.leader = request.user.leaders
            customer.save()
            return redirect('success')  # Replace 'success' with the desired URL name
    else:
        form = CustomerRegistrationForm()

    context = {
        'form': form,
    }

    return render(request,"administration/index.html",context)

@login_required
def gsearch_users(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            users = Customers.objects.filter(name__icontains=query)

            for i in users:
                customer_loans = Loan.objects.filter(loanee=i)
        else:
            users = Customers.objects.filter()
        
        context = {
            'customer_data': users,
            'query': query,
            'loans':customer_loans
        }
        return render(request, 'administration/search.html', context)
    
@login_required
def asearch_customer_loans(request):
    if request.method == 'GET':
        ppaid=0
        query = request.GET.get('q')
        if query:
            loans = Loan.objects.filter(loanee__name__icontains=query)
        else:
            loans = Loan.objects.filter()

        for x in loans:
            if x:
                if x.amount_collected > 0:
                    ppaid=(x.amount_paid/x.amount_collected)*100
                else:
                    ppaid=0
            else:
                ppaid=0
        
        context = {
            'loans': loans,
            'query': query,
            'ppaid':ppaid
        }
        return render(request, 'administration/loansearch.html', context)



def states(request):
    states = State.objects.annotate(
        branch_count=Count('branch', distinct=True),
        customer_count=Count('branch__customers', distinct=True)
    )

    context = {
        "states": states
    }

    return render(request, "administration/states.html", context)


def state_detail(request, state_id):
    state = get_object_or_404(State, pk=state_id)
    branches = Branch.objects.filter(state=state).annotate(
        customer_count=Count('customers')
    )
    
    for branch in branches:
        branch.total_collected = Loan.objects.filter(loanee__branch=branch).aggregate(Sum('amount_collected'))['amount_collected__sum'] or 0
        branch.total_paid = Loan.objects.filter(loanee__branch=branch).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
    context = {
        "state": state,
        "branches": branches
    }
    
    return render(request, "administration/state_detail.html", context)


def applied_loans(request):
    applied=LoanApply.objects.filter(status="Pending")

    context={
        "applied":applied
    }


    return render(request,'administration/appliedloans.html',context)


from django.utils import timezone

def approve_loan(request, loan_id):
    loan = get_object_or_404(LoanApply, id=loan_id)
    
    # Create a Loan object for the approved loan
    new_loan = Loan.objects.create(
        loanee=loan.customer,
        amount_collected=loan.amount,
        amount_paid=0,  # Initial amount paid is 0
        due_date=timezone.now() + timezone.timedelta(days=25),
        status='Active',  # Assuming you want it to be 'Active'
        due=False,
    )
    
    loan.status = 'Approved'
    loan.save()
    new_loan.save()
    # You can also perform other actions here like sending notifications
    
    return redirect('applied')  # Redirect to the applied loans list




def reject_loan(request, loan_id):
    loan = get_object_or_404(LoanApply, id=loan_id)
    
    loan.status = 'Rejected'
    loan.save()
    # You can also perform other actions here like sending notifications
    
    return redirect('applied_loans')  # Redirect to the applied loans list




def search_applied_loans(request):
    query = request.GET.get('q')
    applied_loans = LoanApply.objects.filter(status='Pending')
    
    if query:
        applied = applied_loans.filter(customer__name__icontains=query)
    
    context = {
        'applied': applied,
        'query': query,
    }
    print()
    
    return render(request, 'administration/appliedloans.html', context)

