from django.shortcuts import render
from django.contrib.auth.models import User
from .models import GeneralManager
from administration.models import Branch,Customers,State,Loan
from django.db.models import Sum

# Create your views here.


from django.db.models import Sum, F, ExpressionWrapper, FloatField

def dashboard(request):
    user = User.objects.get(username=request.user.username)
    general_manager = GeneralManager.objects.get(name=user.id)
    state = State.objects.get(general_manager=general_manager.id)
    branches = Branch.objects.filter(state=state.id)
    
    customer_loans = {}  # Dictionary to store customer loan statistics
    total_collected_state = 0
    total_paid_state = 0
    total_customers_state = 0
    


    for branch in branches:
        customers = Customers.objects.filter(branch=branch)
        
        for customer in customers:
            loans = Loan.objects.filter(loanee=customer)
            total_giving = loans.aggregate(total_collected=Sum('amount_collected'))['total_collected'] or 0
            total_paid = loans.aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0
            loan_statuses = [loan.status for loan in loans]

            try:
                if loan_statuses[0]:
                    status=loan_statuses[0]
                    if total_giving!=0:
                        ppaid=(total_paid/total_giving)*100
                else:
                    status="NEW CUSTOMER"
            except:
                status="NEW CUSTOMER"
                ppaid=0
            
            collected = 0
            
            
            if total_giving != 0:
                collected = (total_paid / total_giving) * 100
            
            loan_stats = [{'loan': loan, 'ppaid': (loan.amount_paid / loan.amount_collected) * 100} for loan in loans]
            
            customer_loans[customer] = {
                'given': total_giving,
                'paid': total_paid,
                'collected': collected,
                'loan_stats': loan_stats,
                'ppaid':ppaid,
                'status':status
            }
            total_collected_state += total_giving
            total_paid_state += total_paid
            total_customers_state += 1
    
    total_branches_state = branches.count()
    
    context = {
        'customer_loans': customer_loans,
        'total_collected_state': total_collected_state,
        'total_paid_state': total_paid_state,
        'total_customers_state': total_customers_state,
        'total_branches_state': total_branches_state,
    }
    
   
    
    return render(request, "generalmanagers/dashboard.html", context)

def state_customers(request):
    user = User.objects.get(username=request.user.username)
    general_manager = GeneralManager.objects.get(name=user.id)
    state = State.objects.get(general_manager=general_manager.id)
    branches = Branch.objects.filter(state=state.id)
    
    customer_loans = {}  # Dictionary to store customer loan statistics
    total_collected_state = 0
    total_paid_state = 0
    total_customers_state = 0
    


    for branch in branches:
        customers = Customers.objects.filter(branch=branch)
        
        for customer in customers:
            loans = Loan.objects.filter(loanee=customer)
            total_giving = loans.aggregate(total_collected=Sum('amount_collected'))['total_collected'] or 0
            total_paid = loans.aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0
            loan_statuses = [loan.status for loan in loans]
            dues=[loan.due_date for loan in loans]

            try:
                if loan_statuses[0]:
                    status=loan_statuses[0]
                    due=dues[0]
                    if total_giving!=0:
                        ppaid=(total_paid/total_giving)*100
                else:
                    status="NEW CUSTOMER"
            except:
                status="NEW CUSTOMER"
                ppaid=0
                due="No lOAN YET"
            
            collected = 0
            
            
            if total_giving != 0:
                collected = (total_paid / total_giving) * 100
            
            loan_stats = [{'loan': loan, 'ppaid': (loan.amount_paid / loan.amount_collected) * 100} for loan in loans]
            
            customer_loans[customer] = {
                'given': total_giving,
                'paid': total_paid,
                'collected': collected,
                'loan_stats': loan_stats,
                'ppaid':ppaid,
                'status':status,
                'due':due
            }
            total_collected_state += total_giving
            total_paid_state += total_paid
            total_customers_state += 1
    
    total_branches_state = branches.count()
    
    context = {
        'customer_loans': customer_loans,
        'total_collected_state': total_collected_state,
        'total_paid_state': total_paid_state,
        'total_customers_state': total_customers_state,
        'total_branches_state': total_branches_state,
    }

    return render(request, "generalmanagers/statecustomers.html", context)


def state_loans(request):
    user = User.objects.get(username=request.user.username)
    general_manager = GeneralManager.objects.get(name=user.id)
    state = State.objects.get(general_manager=general_manager.id)
    branches = Branch.objects.filter(state=state.id)
    
    customer_loans = {}  # Dictionary to store customer loan statistics
    total_collected_state = 0
    total_paid_state = 0
    total_customers_state = 0
    


    for branch in branches:
        customers = Customers.objects.filter(branch=branch)
        
        for customer in customers:
            loans = Loan.objects.filter(loanee=customer)
            total_giving = loans.aggregate(total_collected=Sum('amount_collected'))['total_collected'] or 0
            total_paid = loans.aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0
            loan_statuses = [loan.status for loan in loans]

            try:
                if loan_statuses[0]:
                    status=loan_statuses[0]
                    if total_giving!=0:
                        ppaid=(total_paid/total_giving)*100
                else:
                    status="NEW CUSTOMER"
            except:
                status="NEW CUSTOMER"
                ppaid=0
            

            
            collected = 0
            
            
            if total_giving != 0:
                collected = (total_paid / total_giving) * 100
            
            loan_stats = [{'loan': loan, 'ppaid': (loan.amount_paid / loan.amount_collected) * 100, 'status': loan.status} for loan in loans]
            
            customer_loans[customer] = {
                'given': total_giving,
                'paid': total_paid,
                'collected': collected,
                'loan_stats': loan_stats,
                'ppaid':ppaid,
                'status':status
            }
            total_collected_state += total_giving
            total_paid_state += total_paid
            total_customers_state += 1
    
    total_branches_state = branches.count()
    
    context = {
        'customer_loans': customer_loans,
        'total_collected_state': total_collected_state,
        'total_paid_state': total_paid_state,
        'total_customers_state': total_customers_state,
        'total_branches_state': total_branches_state,
    }
    

    return render(request, "generalmanagers/loans.html", context)



def customer_search(request):
    user = User.objects.get(username=request.user.username)
    general_manager = GeneralManager.objects.get(name=user.id)
    state = State.objects.get(general_manager=general_manager.id)
    branches = Branch.objects.filter(state=state.id)
    ppaid = 0
    branch_stats = []
    all_given=0
    all_returned=0
    for branch in branches:
        branch_loans_stats = []
        
        if request.method == 'GET':
            query = request.GET.get('q')
            if query:

                users = Customers.objects.filter(branch=branch, name__icontains=query)

                if users:
                    for i in users:            
                        customer_loans = Loan.objects.filter(loanee=i)   
                        total_giving = customer_loans.aggregate(total_collected=Sum('amount_collected'))['total_collected'] or 0
                        total_paid = customer_loans.aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0

                        all_given+=total_giving
                        all_returned+=total_paid
                        
                        for lo in customer_loans:
                            if lo.amount_collected == 0:
                                pass
                            else:
                                ppaid = (lo.amount_paid / lo.amount_collected) * 100
                            
                            branch_loans_stats.append({
                                'loan': lo,
                                'ppaid': int(ppaid),
                            })
                else:
                    customer_loans=None

            else:
                users = Customers.objects.filter()
            branch_stats.append({
            'branch': branch,
            'customers': users,
            'loans_stats': branch_loans_stats,
            "total":all_given,
            "rtotal":all_returned,
            'loans':customer_loans,
        })
         

            context = {
                "branch_stats":branch_stats,
                'customer_data': users,
                'query': query,
                
                "ppaid":ppaid,
            
                }
            
    return render(request,"generalmanagers/customersearch.html",context)


def loan_search(request):
    user = User.objects.get(username=request.user.username)
    general_manager = GeneralManager.objects.get(name=user.id)
    state = State.objects.get(general_manager=general_manager.id)
    branches = Branch.objects.filter(state=state.id)
    ppaid = 0
    branch_stats = []
    all_given=0
    all_returned=0
    for branch in branches:
        branch_loans_stats = []
        
        if request.method == 'GET':
            query = request.GET.get('q')
            if query:

                users = Customers.objects.filter(branch=branch, name__icontains=query)

                if users:
                    for i in users:            
                        customer_loans = Loan.objects.filter(loanee=i)   
                        total_giving = customer_loans.aggregate(total_collected=Sum('amount_collected'))['total_collected'] or 0
                        total_paid = customer_loans.aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0

                        all_given+=total_giving
                        all_returned+=total_paid
                        
                        for lo in customer_loans:
                            if lo.amount_collected == 0:
                                pass
                            else:
                                ppaid = (lo.amount_paid / lo.amount_collected) * 100
                            
                            branch_loans_stats.append({
                                'loan': lo,
                                'ppaid': int(ppaid),
                            })
                else:
                    customer_loans=None

            else:
                users = Customers.objects.filter()
            branch_stats.append({
            'branch': branch,
            'customers': users,
            'loans_stats': branch_loans_stats,
            "total":all_given,
            "rtotal":all_returned,
            'loans':customer_loans,
        })
         

            context = {
                "branch_stats":branch_stats,
                'customer_data': users,
                'query': query,
                
                "ppaid":ppaid,
            
                }



    return render(request,"generalmanagers/loansearch.html",context)

def branches(request):
    user = User.objects.get(username=request.user.username)
    general_manager = GeneralManager.objects.get(name=user.id)
    state = State.objects.get(general_manager=general_manager.id)
    branches = Branch.objects.filter(state=state.id)
    
    for branch in branches:
        branch.total_collected = Loan.objects.filter(loanee__branch=branch).aggregate(Sum('amount_collected'))['amount_collected__sum'] or 0
        branch.total_paid = Loan.objects.filter(loanee__branch=branch).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    


    return render(request,"generalmanagers/branches.html",context={ "branchs":branches})