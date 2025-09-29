from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from . import views
from .views import worker_list_create
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),


    path('', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),


    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('workers_list_create/', views.worker_list_create, name='workers_list_create'),

    path('stock_page/', views.stock_page, name='stock_page'),  # Serves the HTML

    # API endpoints for stock
    path('stock/', views.stock_list, name='stock_list'),  # GET stock items
    path('add/', views.add_item, name='add_item'),  # POST new item
    path('update/<int:item_id>/', views.update_item, name='update_item'),  # POST update
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),  # POST delete

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


