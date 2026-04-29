"""
URL configuration for luxehairs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('luxehairs-admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('chat/', views.chat, name='chat'),
    # Custom Admin Routes
    path('admin-dashboard/', views.custom_admin, name='custom_admin'),
    path('admin-dashboard/customers/', views.admin_customers, name='admin_customers'),
    path('admin-dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('admin-dashboard/inventory/', views.admin_inventory, name='admin_inventory'),
    path('admin-dashboard/add/', views.admin_product_add, name='admin_product_add'),
    path('admin-dashboard/edit/<int:product_id>/', views.admin_product_edit, name='admin_product_edit'),
    path('admin-dashboard/delete/<int:product_id>/', views.admin_product_delete, name='admin_product_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
