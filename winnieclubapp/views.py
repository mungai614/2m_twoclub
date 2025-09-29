from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm

from .models import StockItem
from .models import Member

def home(request):
    return render(request, 'home.html')

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Save email manually if UserCreationForm doesn't collect it
            user.email = request.POST.get('email')  # assuming you add email field in the template
            user.save()

            login(request, user)

            # Check if it's an admin email
            admin_emails = ['admin@example.com', 'superuser@example.com']  # customize this
            if user.email in admin_emails:
                return redirect('dashboard')  # admin dashboard URL name
            else:
                return redirect('home')  # regular user home URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    return render(request, 'profile.html')




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StockItem
import json

def stock_page(request):
    return render(request, 'stock_page.html')

def stock_list(request):
    if request.method == 'GET':
        items = list(StockItem.objects.values())
        return JsonResponse({'items': items})

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            quantity = data.get('quantity', 0)

            if not name or not isinstance(quantity, int) or quantity < 0:
                return JsonResponse({'status': 'error', 'message': 'Invalid input'}, status=400)

            item = StockItem.objects.create(name=name, quantity=quantity)
            return JsonResponse({'id': item.id, 'name': item.name, 'quantity': item.quantity})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def update_item(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = data.get('quantity')
        try:
            item = StockItem.objects.get(id=item_id)
            item.quantity = quantity
            item.save()
            return JsonResponse({'status': 'success'})
        except StockItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)

@csrf_exempt
def delete_item(request, item_id):
    if request.method == 'POST':
        try:
            item = StockItem.objects.get(id=item_id)
            item.delete()
            return JsonResponse({'status': 'deleted'})
        except StockItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)



from .models import Worker
from .forms import WorkerForm

def worker_list_create(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('worker-list-create.')
    else:
        form = WorkerForm()

    workers = Worker.objects.all()
    return render(request, 'worker_list_create.html', {
        'form': form,
        'workers': workers
    })



def dashboard(request):
    return render(request, 'dashboard.html')

