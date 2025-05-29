from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import auth_users, allowed_users
from user.forms import CreateUserForm
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Sum

# Create your views here.


@login_required(login_url='user-login')
def index(request):
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    staff = User.objects.filter(groups__name='Admin')
    staff_count = staff.count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'form': form,
        'order': order,
        'product': product,
        'product_count': product_count,
        'order_count': order_count,
        'staff_count': staff_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='user-login')
def products(request):
    product = Product.objects.all()
    product_count = product.count()
    staff = User.objects.filter(groups__name='Admin')
    staff_count = staff.count()
    order = Order.objects.all()
    order_count = order.count()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-products')
    else:
        form = ProductForm()
    context = {
        'product': product,
        'form': form,
        'staff_count': staff_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/products.html', context)


@login_required(login_url='user-login')
def product_detail(request, pk):
    context = {

    }
    return render(request, 'dashboard/products_detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def customers(request):
    staff = User.objects.filter(groups__name='Admin')
    staff_count = staff.count()
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Admin')
            user.groups.add(group)
            messages.success(request, f'Staff Account has been created for {username}')
            return redirect('dashboard-customers')
    else:
        form = CreateUserForm()

    context = {
        'staff': staff,
        'form': form,
        'staff_count': staff_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/customers.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def customer_detail(request, pk):
    staff = User.objects.filter(groups__name='Admin')
    staff_count = staff.count()
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customers = User.objects.get(id=pk)
    context = {
        'customers': customers,
        'staff_count': staff_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/customers_detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def product_edit(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-products')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/products_edit.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin'])
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-products')
    context = {
        'item': item
    }
    return render(request, 'dashboard/products_delete.html', context)


@login_required(login_url='user-login')
def order(request):
    order = Order.objects.all()
    order_count = order.count()
    staff = User.objects.filter(groups__name='Admin')
    staff_count = staff.count()
    product = Product.objects.all()
    product_count = product.count()

    context = {
        'order': order,
        'staff_count': staff_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/order.html', context)


@login_required(login_url='user-login')
def daily_stats(request):
    date_str = request.GET.get('date')
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Get orders for the selected date
        daily_orders = Order.objects.filter(
            created_at__date=date
        ).count()

        # Get active staff count (all staff members)
        active_staff = User.objects.filter(
            groups__name='Admin'
        ).count()

        # Get total products in stock
        products_in_stock = Product.objects.aggregate(
            total_stock=Sum('quantity')
        )['total_stock'] or 0

        return JsonResponse({
            'orders': daily_orders,
            'staff': active_staff,
            'products': products_in_stock
        })
    except (ValueError, TypeError):
        return JsonResponse({
            'orders': 0,
            'staff': 0,
            'products': 0
        })
