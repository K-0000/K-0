from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView
import requests

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.home, name="home-page"),
    
    path('test', views.test, name="test-page"),    
    
    #Credentials
    path('login', auth_views.LoginView.as_view(template_name = 'posApp/login.html',redirect_authenticated_user=True), name="login"),
    path('userlogin', views.login_user, name="login-user"),
    path('logout', views.logoutuser, name="logout"),
    
    #Category
    path('category', views.category, name="category-page"),
    path('manage_category', views.manage_category, name="manage_category-page"),
    path('save_category', views.save_category, name="save-category-page"),
    path('delete_category', views.delete_category, name="delete-category"),
    
    #Product
    path('products', views.products, name="product-page"),
    path('manage_products', views.manage_products, name="manage_products-page"),
    path('save_product', views.save_product, name="save-product-page"),
    path('delete_product', views.delete_product, name="delete-product"),    

    #Stock
    path('stock', views.Stock_page, name="stock"),
    path('manage_stock', views.manage_stock, name="manage_stock-page"),
    path('delete_stock', views.delete_stock, name="delete-stock"),
    path('save_stock', views.save_stock, name="save-stock-page"),

    path('prestock', views.Prestock_page, name="prestock"),
    
    #Mixed
    path('mixed', views.mix_stock, name="mixed"),
    path('mixed2', views.mix_stock2, name="mixed2"),
    path('mixeditems', views.mixed_item, name="mixeditems"),
    path('Poundmanagement', views.lb_manage, name="pound"),
    path('Divide', views.divide_manage, name="divide"),

    #Customer
    path('customer', views.customer, name="customer-page"),
    path('manage_customer', views.manage_customer, name="manage_customer-page"),
    path('save_customer', views.save_customer, name="save-customer-page"),
    path('delete_customer', views.delete_customer, name="delete-customer"),

    #Vendors
    path('vendor', views.vendor, name="vendor-page"),
    path('manage_vendor', views.manage_vendor, name="manage_vendor-page"),
    path('save_vendor', views.save_vendor, name="save-vendor-page"),
    path('delete_vendor', views.delete_vendor, name="delete-vendor"),
    
    #Pos
    path('pos', views.pos, name="pos-page"),
    path('save-pos', views.save_pos, name="save-pos"),

    #Purchase
    path('purchase', views.purchase, name='purchase-page'),
    path('save-purchase', views.save_purchase, name='save-purchase'),

    #sales
    path('sales', views.salesList, name="sales-page"),
    path('sales/<str:filter_id>', views.salesList, name="sales-page-filtered"),
    path('receipt', views.receipt, name="receipt-modal"),
    path('delete_sale', views.delete_sale, name="delete-sale"),
    
    #Cashbook
    path('Cashbook', views.cashbook, name="cashbk"),
    path('Cashbook/<int:receipt_redirect>', views.cashbook, name="cashbkred"),
    path('manage_cashbook', views.manage_cashbook, name="manage_cashbook-page"),
    path('save_cashbook', views.Save_cashbook, name="save-cashbook-page"),
    path('delete_cashbook', views.delete_cashbook,name="delete-cashbook"),

    #Purchasebook
    path('Purchasebook', views.purchasebook, name="purchasebk"),
    path('manage_purchasebook', views.manage_purchasebook, name="manage_purchasebook-page"),
    path('save_purchasebook', views.Save_purchasebook, name="save_purchasebook"),
    path('delete_purchasebook', views.delete_purchasebook,name="delete-purchasebook"),


    path('Mixing', views.mix_stock, name="mix_stock-page"),
    path('checkout-modal', views.checkout_modal, name="checkout-modal"),

    #Sales Report
    path('SP', views.data_sale, name="sale_report"),
    path('SP/<str:date_from>', views.data_sale, name="sale_report_date_from"),
    path('SP/<str:date_from>/<str:date_to>', views.data_sale, name="sale_report_date_from_date_to"),

    #Stock Report
    path('ST', views.data_stock, name="stock_report"),
    path('ST/<str:date_from>', views.data_stock, name="stock_report_date_from"),
    path('ST/<str:date_from>/<str:date_to>', views.data_stock, name="stock_report_date_from_date_to"),

    #Pound Report
    path('LB', views.data_lb, name="pound_report"),
    path('LB/<str:date_from>', views.data_lb, name="pound_report_date_from"),
    path('LB/<str:date_from>/<str:date_to>', views.data_lb, name="pound_report_date_from_date_to"),

    # Cashbook Report
    path('CR', views.data_cash, name="cash_report"),
    path('CR/<str:date_from>', views.data_cash, name="cash_report_date_from"),
    path('CR/<str:date_from>/<str:date_to>', views.data_cash, name="cash_report_date_from_date_to"),

    # Prepaid Report
    path('PR', views.data_prepaid, name="prepaid_report"),
    path('PR/<str:date_from>', views.data_prepaid, name="prepaid_report_date_from"),
    path('PR/<str:date_from>/<str:date_to>', views.data_prepaid, name="prepaid_report_date_from_date_to"),
    # path('employees', views.employees, name="employee-page"),
    # path('manage_employees', views.manage_employees, name="manage_employees-page"),
    # path('save_employee', views.save_employee, name="save-employee-page"),
    # path('delete_employee', views.delete_employee, name="delete-employee"),
    # path('view_employee', views.view_employee, name="view-employee-page"),
]