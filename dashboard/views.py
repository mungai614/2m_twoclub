from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def admin_dashboard(request):
    # You can pass any context here for dashboard stats, etc.
    context = {}
    return render(request, 'dashboard/admin_dashboard.html', context)
