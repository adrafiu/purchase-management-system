from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_view, name='profile'),

    path('suppliers/', views.supplier_list, name='suppliers'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),
    path('suppliers/edit/<int:pk>/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),

    path('purchases/', views.purchase_list, name='purchases'),
    path('purchases/add/', views.purchase_add, name='purchase_add'),
    path('purchases/edit/<int:pk>/', views.purchase_edit, name='purchase_edit'),
    path('purchases/delete/<int:pk>/', views.purchase_delete, name='purchase_delete'),

]
