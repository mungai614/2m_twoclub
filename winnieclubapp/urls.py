from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import dashboard, worker_list_create

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),

    path('', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),

    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),

    path('workers_list_create/', worker_list_create, name='workers_list_create'),
    path('workers/', views.worker_list, name='worker_list'),

    path('money/', views.money_management, name='money_management'),
    path('sales/', views.record_sale, name='record_sale'),
    path('sales_list/', views.sales_list, name='sales_list'),

    path('stock_page/', views.stock_page, name='stock_page'),  # Serves the HTML

    # API endpoints for stock
    path('stock/', views.stock_list, name='stock_list'),
    path('add/', views.add_item, name='add_item'),
    path('update/<int:item_id>/', views.update_item, name='update_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
