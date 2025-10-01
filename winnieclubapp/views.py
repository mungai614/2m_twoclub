from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Sum, F, FloatField, ExpressionWrapper

from .models import StockItem, Sale, Worker
from .forms import SaleForm, WorkerForm
from .serializers import StockItemSerializer


# --- Basic Pages ---

def home(request):
    return render(request, 'home.html')


def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def profile_view(request):
    return render(request, 'profile.html')


def register(request):
    """
    User registration view with email capture and redirect based on admin status.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email')  # make sure your registration form has an email field
            user.save()

            login(request, user)

            admin_emails = ['admin@example.com', 'superuser@example.com']  # customize this list
            if user.email in admin_emails:
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# --- Stock Item API Views ---

@api_view(['GET'])
def stock_list(request):
    items = StockItem.objects.all()
    serializer = StockItemSerializer(items, many=True)
    return Response({'items': serializer.data})


@api_view(['POST'])
def add_item(request):
    serializer = StockItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_item(request, item_id):
    try:
        item = StockItem.objects.get(id=item_id)
        item.quantity = request.data.get('quantity', item.quantity)
        item.save()
        return Response({'status': 'updated'})
    except StockItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=404)


@api_view(['POST'])
def delete_item(request, item_id):
    try:
        item = StockItem.objects.get(id=item_id)
        item.delete()
        return Response({'status': 'deleted'})
    except StockItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=404)


# --- Worker Views ---

def worker_list_create(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('worker-list-create')  # Make sure this URL name is correct
    else:
        form = WorkerForm()

    workers = Worker.objects.all()
    return render(request, 'worker_list_create.html', {'form': form, 'workers': workers})


def worker_list(request):
    workers = Worker.objects.all()
    return render(request, 'worker_list.html', {'workers': workers})


# --- Money Management ---

def money_management(request):
    total_spent = StockItem.objects.aggregate(
        total=Sum(ExpressionWrapper(F('buying_price') * F('quantity'), output_field=FloatField()))
    )['total'] or 0

    total_revenue = Sale.objects.aggregate(
        total=Sum(ExpressionWrapper(F('quantity_sold') * F('selling_price'), output_field=FloatField()))
    )['total'] or 0

    total_cost_sold = Sale.objects.aggregate(
        total=Sum(ExpressionWrapper(F('quantity_sold') * F('buying_price'), output_field=FloatField()))
    )['total'] or 0

    total_profit = total_revenue - total_cost_sold

    context = {
        'total_spent': total_spent,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
    }
    return render(request, 'money_management.html', context)


# --- Sale Views ---

from django.shortcuts import render, redirect
from .forms import SaleForm

def record_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save()  # saves Sale and sets FK correctly
            return redirect('sales_list')  # redirect to your sales list page
    else:
        form = SaleForm()

    return render(request, 'record_sale.html', {'form': form})


def sales_list(request):
    sales = Sale.objects.all().order_by('-date_sold')
    context = {'sales': sales}
    return render(request, 'sales_list.html', context)


# --- Other Pages ---

def stock_page(request):
    return render(request, 'stock_page.html')
