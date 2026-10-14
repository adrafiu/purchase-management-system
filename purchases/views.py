from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

from .models import Profile, Supplier, Purchase
from .forms import (
    RegisterForm,
    ProfileForm,
    SupplierForm,
    PurchaseForm
)


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        Profile.objects.create(
            user=user,
            full_name=user.username
        )

        messages.success(request, 'Registration successful.')
        return redirect('login')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('login')


@login_required(login_url='/login/')
def dashboard(request):
    purchases = Purchase.objects.all()

    total_purchase = purchases.count()

    total_amount = sum(
        (p.total_amount for p in purchases),
        Decimal('0.00')
    )

    paid_amount = sum(
        (p.paid_amount for p in purchases),
        Decimal('0.00')
    )

    due_amount = sum(
        (p.due_amount for p in purchases),
        Decimal('0.00')
    )

    recent_purchases = purchases.order_by('-purchase_date')[:5]

    context = {
        'total_purchase': total_purchase,
        'total_supplier': Supplier.objects.count(),
        'total_amount': total_amount,
        'paid_amount': paid_amount,
        'due_amount': due_amount,
        'recent_purchases': recent_purchases,
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='/login/')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.username}
    )

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'profile.html', {'form': form})


@login_required(login_url='/login/')
def supplier_list(request):
    query = request.GET.get('q', '')

    suppliers = Supplier.objects.all().order_by('supplier_name')

    if query:
        suppliers = suppliers.filter(
            Q(supplier_name__icontains=query)
            | Q(contact_number__icontains=query)
        )

    return render(request, 'suppliers.html', {
        'suppliers': suppliers,
        'query': query,
    })


@login_required(login_url='/login/')
def supplier_add(request):
    form = SupplierForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Supplier added successfully.')
        return redirect('suppliers')

    return render(request, 'supplier_form.html', {
        'form': form,
        'title': 'Add Supplier',
    })


@login_required(login_url='/login/')
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    form = SupplierForm(
        request.POST or None,
        instance=supplier
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Supplier updated successfully.')
        return redirect('suppliers')

    return render(request, 'supplier_form.html', {
        'form': form,
        'title': 'Edit Supplier',
    })


@login_required(login_url='/login/')
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully.')
        return redirect('suppliers')

    return render(request, 'confirm_delete.html', {
        'object': supplier,
        'cancel_url': 'suppliers',
    })


@login_required(login_url='/login/')
def purchase_list(request):
    query = request.GET.get('q', '')

    purchases = Purchase.objects.select_related(
        'supplier'
    ).order_by('-purchase_date')

    if query:
        purchases = purchases.filter(
            Q(product_name__icontains=query)
            | Q(supplier__supplier_name__icontains=query)
        )

    return render(request, 'purchases.html', {
        'purchases': purchases,
        'query': query,
    })


@login_required(login_url='/login/')
def purchase_add(request):
    form = PurchaseForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Purchase added successfully.')
        return redirect('purchases')

    return render(request, 'purchase_form.html', {
        'form': form,
        'title': 'Add Purchase',
    })


@login_required(login_url='/login/')
def purchase_edit(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)

    form = PurchaseForm(
        request.POST or None,
        instance=purchase
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Purchase updated successfully.')
        return redirect('purchases')

    return render(request, 'purchase_form.html', {
        'form': form,
        'title': 'Edit Purchase',
    })


@login_required(login_url='/login/')
def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == 'POST':
        purchase.delete()
        messages.success(request, 'Purchase deleted successfully.')
        return redirect('purchases')

    return render(request, 'confirm_delete.html', {
        'object': purchase,
        'cancel_url': 'purchases',
    })