from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, Income
from .forms import ExpenseForm, CustomSignUpForm, IncomeForm
from collections import defaultdict
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.conf import settings
import requests
from django.contrib.auth.models import User
from .models import  Profile
from urllib.parse import urlencode
from django.contrib.auth import login

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        expenses = expenses.filter(category=category)
    
    # Calculate monthly totals
    monthly_totals = expenses.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('-month')

    # Calculate yearly totals
    yearly_totals = expenses.annotate(
        year=TruncYear('date')
    ).values('year').annotate(
        total=Sum('amount')
    ).order_by('-year')
    
    # Regular grouping by date
    grouped_expenses = {}
    date_totals = {}
    
    for expense in expenses:
        date = expense.date
        if date not in grouped_expenses:
            grouped_expenses[date] = []
        grouped_expenses[date].append(expense)
        
        if date not in date_totals:
            date_totals[date] = 0
        date_totals[date] += float(expense.amount)
    
    context = {
        'grouped_expenses': grouped_expenses,
        'totals': date_totals,
        'monthly_totals': monthly_totals,
        'yearly_totals': yearly_totals,
        'expense_categories': Expense.CATEGORY_CHOICES,
        'income_categories': Income.CATEGORY_CHOICES,
        'selected_category': category,
    }
    return render(request, 'trackense/expense_list.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('trackense:expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'trackense/expense_form.html', {'form': form})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('trackense:expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'trackense/expense_form.html', {'form': form, 'edit_mode': True})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')
    return redirect('trackense:expense_list')

@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        incomes = incomes.filter(category=category)
    
    monthly_totals = incomes.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('-month')

    yearly_totals = incomes.annotate(
        year=TruncYear('date')
    ).values('year').annotate(
        total=Sum('amount')
    ).order_by('-year')
    
    grouped_incomes = {}
    date_totals = {}
    
    for income in incomes:
        date = income.date
        if date not in grouped_incomes:
            grouped_incomes[date] = []
        grouped_incomes[date].append(income)
        
        if date not in date_totals:
            date_totals[date] = 0
        date_totals[date] += float(income.amount)
    
    context = {
        'grouped_incomes': grouped_incomes,
        'totals': date_totals,
        'monthly_totals': monthly_totals,
        'yearly_totals': yearly_totals,
        'expense_categories': Expense.CATEGORY_CHOICES,
        'income_categories': Income.CATEGORY_CHOICES,
        'selected_category': category,
    }
    return render(request, 'trackense/income_list.html', context)

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Income added successfully!')
            return redirect('trackense:income_list')
    else:
        form = IncomeForm()
    return render(request, 'trackense/income_form.html', {'form': form})

@login_required
def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully!')
            return redirect('trackense:income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'trackense/income_form.html', {'form': form, 'edit_mode': True})

@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    income.delete()
    messages.success(request, 'Income deleted successfully!')
    return redirect('trackense:income_list')

@login_required
def dashboard(request):
    # Get expense data by category
    expense_by_category = Expense.objects.filter(user=request.user).values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Get recent expenses and incomes with category info
    recent_expenses = list(Expense.objects.filter(user=request.user).values(
        'title', 'amount', 'date', 'category', 'created_at'
    ).order_by('-date', '-created_at'))
    recent_incomes = list(Income.objects.filter(user=request.user).values(
        'title', 'amount', 'date', 'category', 'created_at'
    ).order_by('-date', '-created_at'))
    
    # Add type and get category details
    for expense in recent_expenses:
        expense['type'] = 'expense'
        category_name = expense['category']  # Store the category name
        expense['category'] = {
            'name': category_name,
            'icon': Expense.CATEGORY_ICONS[category_name]  # Get icon directly from CATEGORY_ICONS
        }
    
    for income in recent_incomes:
        income['type'] = 'income'
        category_name = income['category']  # Store the category name
        income['category'] = {
            'name': category_name,
            'icon': Income.CATEGORY_ICONS[category_name]  # Get icon directly from CATEGORY_ICONS
        }
    
    # Calculate totals
    total_expenses = Expense.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_income = Income.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    remaining_balance = float(total_income) - float(total_expenses)
    
    # Combine and sort recent transactions
    recent_transactions = sorted(
        recent_expenses + recent_incomes,
        key=lambda x: (x['date'], x['created_at']),
        reverse=True
    )[:5]
    
    categories = [item['category'] for item in expense_by_category]
    amounts = [float(item['total']) for item in expense_by_category]
    
    context = {
        'expense_categories': [(cat[0], cat[1], Expense.CATEGORY_ICONS[cat[0]]) for cat in Expense.CATEGORY_CHOICES],
        'income_categories': [(cat[0], cat[1], Income.CATEGORY_ICONS[cat[0]]) for cat in Income.CATEGORY_CHOICES],
        'chart_categories': categories,
        'chart_amounts': amounts,
        'recent_transactions': recent_transactions,
        'total_income': float(total_income),
        'total_expenses': float(total_expenses),
        'remaining_balance': remaining_balance,
    }
    return render(request, 'trackense/dashboard.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to Expense Tracker!')
            return redirect('trackense:expense_list')
    else:
        form = CustomSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def google_login(request):
    """Redirect users to Google's OAuth consent screen."""
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'select_account',
    }
    auth_url = f"{settings.GOOGLE_AUTH_URL}?{urlencode(params)}"
    return redirect(auth_url)

def google_callback(request):
    """Handle the callback from Google OAuth."""
    code = request.GET.get('code')
    if not code:
        return redirect('login')  # Redirect to login if no code is provided

    # Exchange the authorization code for an access token
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    response = requests.post(settings.GOOGLE_TOKEN_URL, data=token_data)
    if response.status_code != 200:
        return redirect('login')  # Handle error

    access_token = response.json().get('access_token')

    # Fetch user info using the access token
    user_info_response = requests.get(settings.GOOGLE_USER_INFO_URL, headers={
        'Authorization': f'Bearer {access_token}'
    })
    if user_info_response.status_code != 200:
        return redirect('login')  # Handle error

    user_info = user_info_response.json()
    email = user_info.get('email')
    first_name = user_info.get('given_name', '')
    last_name = user_info.get('family_name', '')
    google_profile_picture = user_info.get('picture', '')  # Get the Google profile picture URL

    # Create or get the user
    user, created = User.objects.get_or_create(
        username=email,
        defaults={'email': email, 'first_name': first_name, 'last_name': last_name}
    )

    # Update or create the user's profile with the Google profile picture
    profile, profile_created = Profile.objects.get_or_create(user=user)
    profile.google_profile_picture = google_profile_picture
    profile.save()

    # Log the user in with the specified backend
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('trackense:dashboard') 
