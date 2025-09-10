from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    role = getattr(request.user, 'role', 'customer')
    if role == 'admin':
        return render(request, 'catalog/dashboard_admin.html')
    elif role == 'manager':
        return render(request, 'catalog/dashboard_manager.html')
    elif role == 'staff':
        return render(request, 'catalog/dashboard_staff.html')
    else:
        return render(request, 'catalog/dashboard_customer.html')
