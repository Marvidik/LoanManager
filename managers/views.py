from django.shortcuts import render,redirect
from .models import Manager
from administration.models import Customers,Branch,Loan,LoanApply
from django.contrib.auth.models import User
from django.db.models import Sum
from administration.forms import CustomerRegistrationForm

# Create your views here.


from django.db.models import Sum, F,ExpressionWrapper,FloatField

def dashboard(request):
    user = User.objects.get(username=request.user.username)
    manager = Manager.objects.get(name=user.id)
    branch = Branch.objects.get(manager=manager.id)
    
    total_loans = Loan.objects.filter(loanee__branch=branch).aggregate(total_loans=Sum('amount_collected'))['total_loans'] or 0
    total_paid = Loan.objects.filter(loanee__branch=branch).aggregate(total_paid=Sum('amount_paid'))['total_paid'] or 0
    total_customers = Customers.objects.filter(branch=branch).count()
    
    customers = Customers.objects.filter(branch=branch.id).annotate(
        total_collected=Sum('loan__amount_collected'),
        total_paid=Sum('loan__amount_paid'),
        loan_status=F('loan__status'),
        latest_due_date=F('loan__due_date'),
        ppaid=ExpressionWrapper(
            100 * F('total_paid') / F('total_collected'), 
            output_field=FloatField()
        )
    )

    context = {
        'manager': manager,
        'customers': customers,
        'branch': branch,
        'total_loans': total_loans,
        'total_paid': total_paid,
        'total_customers': total_customers,
    }

    return render(request, "managers/dashboard.html", context)




from django.db.models import Sum,F

def branch_customer(request):
    user = User.objects.get(username=request.user.username)
    manager = Manager.objects.get(name=user.id)
    branch = Branch.objects.get(manager=manager.id)
    
    # Annotate customers with aggregated loan information
    customers = Customers.objects.filter(branch=branch.id).annotate(
        total_collected=Sum('loan__amount_collected'),
        total_paid=Sum('loan__amount_paid'),
        latest_due_date=F('loan__due_date'),
        loan_status=F('loan__status')
    )

    context = {
        "customers": customers,
    }
    return render(request, "managers/branchcustomers.html", context)


def branch_customer_search(request):
    user=User.objects.get(username=request.user.username)
    manager = Manager.objects.get(name=user.id)
    branch=Branch.objects.get(manager=manager.id)
    customers = Customers.objects.filter(branch=branch.id)
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            users = Customers.objects.filter(branch=branch, name__icontains=query)

            if users:
                for i in users:            
                    customer_loans = Loan.objects.filter(loanee=i)   
            else:
                customer_loans=None

        else:
            users = Customers.objects.filter()
        
        context = {
            'customer_data': users,
            'query': query,
            'loans':customer_loans
        }
        return render(request, 'managers/customersearch.html', context)


    return render(request,"managers/customersearch.html")

def branch_loans(request):
    user = User.objects.get(username=request.user.username)
    manager = Manager.objects.get(name=user.id)
    branch = Branch.objects.get(manager=manager.id)
    customers = Customers.objects.filter(branch=branch.id)

    customers_data = []

    for cust in customers:
        loans = Loan.objects.filter(loanee=cust.id)
        total_giving = loans.aggregate(total_collected=Sum('amount_collected'))['total_collected'] or 0
        total_paid = loans.aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0

        customer_loans = []
        for lo in loans:
            if lo.amount_collected == 0:
                customer_loans.append({
                    'ppaid': 0,
                })
            else:
                ppaid = (lo.amount_paid / lo.amount_collected) * 100
                customer_loans.append({
                    'loan': lo,
                    'ppaid': ppaid,
                    'status':lo.status
                })

        customers_data.append({
            'customer': cust,
            'loans': customer_loans,
            'ppaid': ppaid,
            'given': total_giving,
            'collected': total_paid,
            'status':lo.status
        })

    context = {
        "customers_data": customers_data,
    }

    return render(request, "managers/branchloan.html", context)


def loan_search(request):
    user=User.objects.get(username=request.user.username)
    manager = Manager.objects.get(name=user.id)
    branch=Branch.objects.get(manager=manager.id)
    customers = Customers.objects.filter(branch=branch.id)
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            users = Customers.objects.filter(branch=branch, name__icontains=query)

            if users:
                for i in users:            
                    customer_loans = Loan.objects.filter(loanee=i)   
                    total_giving = customer_loans.aggregate(total_collected=Sum('amount_collected'))['total_collected'] or 0
                    for lo in customer_loans:
                        if lo==0:
                            pass
                        else:
                            ppaid=(lo.amount_paid/lo.amount_collected)*100
            else:
                customer_loans=None
                total_giving=None
                ppaid=None

        else:
            users = Customers.objects.filter()
        
        context = {
            'customer_data': users,
            'query': query,
            'loans':customer_loans,
            "given":total_giving,
            "ppaid":ppaid
        }
        return render(request, 'managers/loansearch.html', context)
    
    return render(request,"managers/loansearch.html")


def add_customer(request):
    user=User.objects.get(username=request.user.username)
    manager = Manager.objects.get(name=user.id)
    branch=Branch.objects.get(manager=manager.id)


    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.branch = branch
            customer.save()
            return redirect('manager-dashboard') 
        else:
            print("There was an error with this form")
    else:
        form = CustomerRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, "managers/f.html", context)



def applied(request):
    user = request.user
    manager = Manager.objects.get(name=user.id)
    branch = Branch.objects.get(manager=manager.id)
    customers = Customers.objects.filter(branch=branch.id)
    
    applied = LoanApply.objects.filter(customer__in=customers, status='Pending')

    context = {
        "applied": applied
    }

    return render(request, "managers/applied.html", context)
