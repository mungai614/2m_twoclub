from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages

from django.db.models import Sum, F, FloatField, ExpressionWrapper

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import StockItem, Sale, Worker, Event
from .forms import SaleForm, WorkerForm
from .serializers import StockItemSerializer


# --- Custom Login View ---

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return '/dashboard/'
        return '/'


# --- Basic Pages ---

def home(request):
    events = Event.objects.order_by('event_date')
    return render(request, 'home.html', {'events': events})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')


# --- Registration View ---

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email')
            user.save()
            authenticated_user = authenticate(username=user.username, password=request.POST['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)
            if user.is_staff or user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# --- Stock API Views ---

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
            return redirect('workers_list_create')
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

def record_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_list')
    else:
        form = SaleForm()
    return render(request, 'record_sale.html', {'form': form})

def sales_list(request):
    sales = Sale.objects.all().order_by('-date_sold')
    return render(request, 'sales_list.html', {'sales': sales})


# --- Stock Page View ---

def stock_page(request):
    return render(request, 'stock_page.html')
