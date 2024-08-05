from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse
from flask import jsonify
from posApp.models import Category, Products, Sales, salesItems, Stock, Pre_Stock, Cashbook, CostAmmount, Cashcats, Vendors, Purchasebook
from posApp.models import Customer as custo
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json, sys
from datetime import date, datetime
import pandas as pd
from io import BytesIO
from sqlalchemy import create_engine
import pymysql
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *

from .constants import StockTypeEnum as ST
from .constants import StockAvailabilityEnum as SA
from .constants import Cashbook_CashflowEnum as CB_CF
from .constants import Cashbook_TransactionEnum as CB_T

from Postest.project_constants import Credentials as CR
from dateutil import parser

def test(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'posApp/test.html', context)

# Login
def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


# Logout
def logoutuser(request):
    logout(request)
    return redirect('/')


# Create your views here.
@login_required
def home(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    categories = len(Category.objects.all())
    products = len(Products.objects.all())
    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month=current_month,
        date_added__day=current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month=current_month,
        date_added__day=current_day
    ).all()
    total_sales = sum(today_sales.values_list('grand_total', flat=True))
    context = {
        'page_title': 'Home',
        'categories': categories,
        'products': products,
        'transaction': transaction,
        'total_sales': total_sales,
    }
    return render(request, 'posApp/home.html', context)


def about(request):
    context = {
        'page_title': 'About',
    }
    return render(request, 'posApp/about.html', context)


# Category Section
@login_required
def category(request):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=' % request.path)
    category_list = Category.objects.all()
    # category_list = {}
    context = {
        'page_title': 'Category List',
        'category': category_list,
    }
    return render(request, 'posApp/category.html', context)

@login_required
def manage_category(request):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=%s' % request.path)
    category = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()

    context = {
        'category': category
    }
    return render(request, 'posApp/manage_category.html', context)


@login_required
def save_category(request):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_category = Category.objects.filter(id=data['id']).update(name=data['name'],
                                                                          description=data['description'],
                                                                          status=data['status'])
        else:
            save_category = Category(name=data['name'], description=data['description'], status=data['status'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_category(request):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    data = request.POST
    resp = {'status': ''}
    try:
        Category.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
#End Category Section


# Customer Section
@login_required
def customer(request):
    custo_list = custo.objects.all()
    # category_list = {}
    context = {
        'page_title': 'Customer List',
        'customers': custo_list,
    }
    return render(request, 'posApp/customer.html', context)

@login_required
def manage_customer(request):
    customer = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            customer = Customer.objects.filter(id=id).first()

    context = {
        'customer': customer 
    }
    return render(request, 'posApp/manage_customer.html', context)

@login_required
def save_customer(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_customer = Customer.objects.filter(id=data['id']).update(name=data['name'],
                                                                          address=data['address'])
        else:
            save_customer = Customer(name=data['name'], phone=data['phone'],address=data['address'], comment=data['comment'] )
            save_customer.save()
        resp['status'] = 'success'
        messages.success(request, 'Customer Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_customer(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Customer.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

#### End Customer Section

# Vendor Section
@login_required
def vendor(request):
    vendor_list = Vendors.objects.all()
    # category_list = {}
    context = {
        'page_title': 'Vendor List',
        'vendors': vendor_list,
    }
    return render(request, 'posApp/vendor.html', context)

@login_required
def manage_vendor(request):
    vendor = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            vendor = Vendors.objects.filter(id=id).first()

    context = {
        'vendor': vendor 
    }
    return render(request, 'posApp/manage_vendor.html', context)

@login_required
def save_vendor(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_vendor = Vendors.objects.filter(id=data['id']).update(name=data['name'],
                                                                          address=data['address'])
        else:
            save_vendor = Vendors(name=data['name'], phone=data['phone'],address=data['address'], comment=data['comment'] )
            save_vendor.save()
        resp['status'] = 'success'
        messages.success(request, 'Vendor Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_vendor(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Vendors.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Vendor Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
#### End Vendor Section


### Products Section; Product Section
@login_required
def products(request):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    product_list = Products.objects.all()
    context = {
        'page_title': 'Product List',
        'products': product_list,
    }
    return render(request, 'posApp/products.html', context)


@login_required
def manage_products(request):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    product = {}
    categories = Category.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()

    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'posApp/manage_product.html', context)

@login_required
def save_product(request):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0:
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id=data['category_id']).first()
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0:
                save_product = Products.objects.filter(id=data['id']).update(code=data['code'], category_id=category,
                                                                             name=data['name'],
                                                                             description=data['description'],
                                                                             price=float(data['price']),
                                                                             status=data['status'])
            else:
                save_product = Products(code=data['code'], category_id=category, name=data['name'],
                                        description=data['description'], price=float(data['price']),
                                        status=data['status'])
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_product(request):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    data = request.POST
    resp = {'status': ''}
    try:
        Products.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
###End Product Section

#Pos; Point of Sale
@login_required
def pos(request):
    products = Products.objects.filter(status=1)
    data = request.POST
    Customers = custo.objects.all()
    costprice = Stock.objects.all()
    Employeeos = Employees.objects.all()
    M1 = poscost(request.POST)
    product_json = []
    print(M1)
    for product in products:
        product_json.append({'id': product.id, 'name': product.name, 'price': float(product.price)})
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'product_json': json.dumps(product_json),
        'Customers': Customers,
        'Employees': Employeeos,
        'Costprices':costprice,
        'cost':M1,
    }
    # return HttpResponse('')
    return render(request, 'posApp/pos.html', context)


@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total': grand_total,
    }
    return render(request, 'posApp/checkout.html', context)


@login_required
def save_pos(request):
    resp = {'status': 'failed', 'msg': ''}
    data = request.POST
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code=str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        """
        Stcost= Stock.objects.filter(OS=1).values('cost')
        Dtcost= Stock.objects.filter().values('cost')
        CAcost= CostAmmount.objects.values('cost')
        CAqty= CostAmmount.objects.values('qty')
        Stjson= list(Stcost)
        Dtcost= list(Dtcost)
        CAcost= list(CAcost)
        CAqty= list(CAqty)
        print("Cost :", CAcost)
        #df= pd.DataFrame(Stjson)
        df= pd.DataFrame(CAcost)
        CAqty= pd.DataFrame(CAqty)
        print(df)
        df2= pd.DataFrame(Dtcost)
        df2= df["cost"].mean
        #print(df2)
        qf=df["cost"].mean()
        qf= qf.astype(float)
        #print(qf)
        df= df.values[0]
        df= df.astype(float)
        caqty= CAqty.qty[0]
        
        caqty = caqty.astype(float)
        print(caqty)
        """
        emp = Employees.objects.filter(id=int(data['employee_id'])).first()
        customer = custo.objects.filter(id=int(data['customer_id'])).first()
        grandtotal= float(data['grand_total'])+float(data['transport'])+float(data['labour'])
        sales = Sales(customerID= customer,empID=emp,code=code, sub_total=data['sub_total'], tax=data['tax'], tax_amount=data['tax_amount'],
                      grand_total=grandtotal, tendered_amount=data['tendered_amount'],
                      amount_change=data['amount_change'], Saletype=data['sale_type'], transport=data['transport'], labour=data['labour']).save()
        print("Pass!!")
        sale_id = Sales.objects.last().pk
        i = 0
        #print(onstock)
        salety = data['sale_type']
        cashto = custo.objects.first()
        if salety == '2':
            Cashbook(username=customer,payment=code,descri ="Credit Sale", ammount=data['grand_total'], ct=3 ).save()
        #print(request.POST['cost'])
        for prod in data.getlist('product_id[]'):
            product_id = prod
            sale = Sales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            #cost = float(request.POST['cost'])
            #cost = df
            qty = data.getlist('qty[]')[i]
            price = data.getlist('price[]')[i]
            total = float(qty) * float(price)
            #cAqq = caqty - float(qty)
            print({'sale_id': sale, 'product_id': product, 'qty': qty, 'price': price, 'total': total})
            #CostAmmount.objects.filter().update(qty=cAqq)
            customerid = custo.objects.filter(id=int(data['customer_id'])).first()
            salesItems(sale_id=sale, product_id=product, qty=qty, price=price, total=total).save()
            SaleCount(product_id=product,qty=qty).save()
            print("pass!")
            if salety == '3':
                Pre_Stock(product=product,customer=customerid ,quantity=qty, code=sale,type='1').save()
            else:
                Stock(product=product, quantity=qty, stock_type='4').save()
            i += int(1)
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Sale Record has been saved.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def salesList(request,filter_id=""):
    sales = Sales.objects.all()
    bad_request_message = False

    if filter_id != "":
        sales = Sales.objects.filter(code=filter_id)
        if not sales:
            sales = Sales.objects.all()
            bad_request_message = True

    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        data['items'] = salesItems.objects.filter(sale_id=sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']), '.2f')
        # print(data)
        sale_data.append(data)
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month=current_month,
        date_added__day=current_day
    ).all()
    total_sales = sum(today_sales.values_list('grand_total', flat=True))
    today_cashin = Cashbook.objects.filter(
        date_created__year=current_year,
        date_created__month=current_month,
        date_created__day=current_day,
        ct=1
    ).all()
    total_cashin = sum(today_cashin.values_list('ammount', flat=True))
    today_cashout = Cashbook.objects.filter(
        date_created__year=current_year,
        date_created__month=current_month,
        date_created__day=current_day,
        ct=2
    ).all()
    total_cashout = sum(today_cashout.values_list('ammount', flat=True))
    today_credit = Cashbook.objects.filter(
        date_created__year=current_year,
        date_created__month=current_month,
        date_created__day=current_day,
        ct=3
    ).all()
    total_credit = sum(today_credit.values_list('ammount', flat=True))

    #Monthly
    M_credit = Cashbook.objects.filter(date_created__year=current_year,date_created__month=current_month,ct=3).all()
    M_cashout = Cashbook.objects.filter(date_created__year=current_year,date_created__month=current_month,ct=2).all()
    M_cashin = Cashbook.objects.filter(date_created__year=current_year,date_created__month=current_month,ct=1).all()
    M_sales = Sales.objects.filter(date_added__year=current_year,date_added__month=current_month,).all()
    M_cashin = sum(M_cashin.values_list('ammount', flat=True))
    M_cashout = sum(M_cashout.values_list('ammount', flat=True))
    M_credit = sum(M_credit.values_list('ammount', flat=True))
    M_sales = sum(M_sales.values_list('grand_total', flat=True))

    product_list = Products.objects.all()
    context = {
        'bad_request_message': bad_request_message,
        'filter_id': filter_id,
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
        'total_sales':total_sales,
        'total_cashin':total_cashin,
        'total_cashout':total_cashout,
        'total_credit':total_credit,
        'M_cashin':M_cashin,
        'M_cashout':M_cashout,
        'M_credit':M_credit,
        'M_sales':M_sales,
        'Products':product_list,
    }
    # return HttpResponse('')
    return render(request, 'posApp/sales.html', context)


@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id=id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales, field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id=sales).all()
    context = {
        "transaction": transaction,
        "salesItems": ItemList

    }

    return render(request, 'posApp/receipt.html', context)
    # return HttpResponse('')
#End Pos Section


@login_required
def delete_sale(request):
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id=id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')


# Stock Section
@login_required
def Stock_page(request):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    stock_list = Stock.objects.all()
    product_list = Products.objects.all()
    if request.POST:
        SaleCount.objects.all().delete()
    context = {
        'page_title': 'Stock List',
        'stocks': stock_list,
        'products': product_list,
    }
    return render(request, 'posApp/inventory.html', context)

@login_required
def delete_stock(request):
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        delete = Stock.objects.filter(id=id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')

@login_required
def manage_stock(request):

    type_cases = {type_case.valInt() : str(type_case) for type_case in ST}
    ava_cases = {ava_case.valInt(): str(ava_case) for ava_case in SA }

    product_list = {}
    product_list = Products.objects.all()

    stock_list = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            stock_list = Stock.objects.filter(id=id).first()
    
    M1 = addstock(request.POST)
    if request.POST:
        M1 = addstock(request.POST)
        stockid = Stock.objects.filter().last()
        print(stockid)
        product = Products.objects.filter(id=int(request.POST['product'])).first()
        if M1.is_valid():
            M1.save()
            stockid = Stock.objects.filter().last()
            print(stockid)
            CostAmmount(product_id=product,stock_id=stockid, cost=float(request.POST['cost']), qty=float(request.POST['quantity']) ).save()
            return HttpResponseRedirect('http://127.0.0.1:90/stock')
        
    context = {
        'stocks': stock_list,
        'product': M1,
        'product_list': product_list,
        'current_time': timezone.now,
        'type_cases': type_cases,
        'ava_cases': ava_cases

    }
    return render(request, 'posApp/manage_stock.html', context)

def save_stock(request):
    data = request.POST
    print(data)
    resp = {'status': 'failed'}
    product = Products.objects.filter(id=data['product']).first()
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_stock = Stock.objects.filter(id=data['id']).update(product=data['product'],
                                                                          quantity=data['quantity'],
                                                                          cost=data['cost'],
                                                                          stock_type=data['stock_type'],
                                                                          OS=data['OS']
                                                                          )
        else:
            save_stock = Stock(product=product,
                                        quantity=data['quantity'],
                                        cost=data['cost'],
                                        stock_type=data['stock_type'],
                                        OS=data['OS'])
            save_stock.save()

        resp['status'] = 'success'
        messages.success(request, 'Stock Entry Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

#End Stock Section


@login_required
def Prestock_page(request):
    stock_list = Pre_Stock.objects.all()
    product_list = Products.objects.all()
    customer_list= Sales.objects.all()
    form = preout(request.POST)
    """
    sqlEngine = create_engine(CR.DB_ENGINE, pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    FR = pd.read_sql(
            "select  posapp_customer.name, posapp_products.name,posapp_pre_stock.code,quantity,type from posapp_pre_stock, posapp_customer, posapp_products "
            "where posapp_pre_stock.customer_id = posapp_customer.id and posapp_pre_stock.product_id = posapp_products.id;", dbConnection);
    FR = FR.replace({'type': {1: 'In', 2: 'Out'}})
    OUT = FR[FR['type']=='Out']
    IN = FR[FR['type']=='In']
    print(OUT)
    print(FR.head())
    FR_columns = [s.replace("_", " ").title() for s in FR.columns.values]
    # There has to be a way to automate this

    FR.columns = FR_columns

    FR.to_csv('posApp/files/Payment.csv')

    FRS = FR.style \
        .format(precision=3, thousands=",", decimal=".") \
        .set_table_attributes(
        'class="table table-striped table-bordered" id="sales_report_table" name="sales_report_table"') \
        .to_html()

    print(FRS)
    """
    if request.POST:
        form = preout(request.POST)
        print(form)
        print(request.POST["quantity"])
        print(request.POST['product'])
        product = Products.objects.filter(id=int(request.POST['product'])).first()
        if form.is_valid():
            form.save()
            Stock(product=product, quantity=request.POST["quantity"], stock_type='4').save()
    context = {
        'page_title': 'Pre_Stock List',
        'stocks': stock_list,
        'products': product_list,
        'customers': customer_list,
        'form':form,
        #'itemlist':FRS,
    }
    return render(request, 'posApp/inventory_pre.html', context)


### Cashbook section

@login_required
def cashbook(request, receipt_redirect = 0):
    cash_list = Cashbook.objects.all()
    cc = Customer.objects.all()
    context = {
        'receipt_redirect' : receipt_redirect,
        'page_title': 'Cash_Book',
        'cashs': cash_list,
        'customers':cc
    }
    return render(request, 'posApp/cashbook.html', context)

@login_required
def manage_cashbook(request):

    cashflow_cases = {cashflow_case.valInt() : str(cashflow_case) for cashflow_case in CB_CF}
    transaction_cases = {transaction_case.valInt(): str(transaction_case) for transaction_case in CB_T}
    print(transaction_cases)

    ussrs = Customer.objects.all()
    casg = Cashcats.objects.all()
    cash_list = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            cash_list = Cashbook.objects.filter(id=id).first()

    #print(cashflow_cases)
    #print(transaction_cases)
     
    context = {
        'current_time': timezone.now,
        'cashbook': cash_list,
        'cashflow_cases': cashflow_cases,
        'transaction_cases': transaction_cases,
        'users':ussrs,
        'Cashcats':casg
    }
    return render(request, 'posApp/manage_cashbook.html', context)

@login_required
def Save_cashbook(request):
    data = request.POST
    print(data)
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            uuu = Customer.objects.filter(id=data['customer_id']).first()
            ccc = Cashcats.objects.filter(id=data['cass_id']).first()
            save_cashbook = Cashbook.objects.filter(id=data['id']).update(username=uuu,cashty=ccc,payment=data['name-payment'],
                                                                        ammount=data['amount'],
                                                                        descri=data['description'],
                                                                        ct=data['cashflow'],
                                                                        tr=data['transaction']
                                                                        )
        else:
            uuu = Customer.objects.filter(id=data['customer_id']).first()
            ccc = Cashcats.objects.filter(id=data['cass_id']).first()
            save_cashbook = Cashbook(username=uuu,cashty=ccc,payment=data['name-payment'],
                                            ammount=data['amount'],
                                            descri=data['description'],
                                            ct=data['cashflow'],
                                            tr=data['transaction']
                                            )
            save_cashbook.save()

        resp['status'] = 'success'
        messages.success(request, 'Stock Entry Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_cashbook(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Cashbook.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

#### End Cashbook Section

### Purchasebook Section

@login_required
def purchasebook(request):
    pb_list = Purchasebook.objects.all()
    vv = Vendors.objects.all()
    context = {
        'page_title': 'Purchasebook',
        'pbs': pb_list,
        'vendors':vv
    }
    return render(request, 'posApp/purchasebook.html', context)

@login_required
def manage_purchasebook(request):

    cashflow_cases = {cashflow_case.valInt() : str(cashflow_case) for cashflow_case in CB_CF}
    transaction_cases = {transaction_case.valInt(): str(transaction_case) for transaction_case in CB_T}

    ussrs = Vendors.objects.all()
    casg = Cashcats.objects.all()
    cash_list = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            cash_list = Purchasebook.objects.filter(id=id).first()

    #print(cashflow_cases)
    #print(transaction_cases)
     
    context = {
        'current_time': timezone.now,
        'purchasebook': cash_list,
        'cashflow_cases': cashflow_cases,
        'transaction_cases': transaction_cases,
        'users':ussrs,
        'Cashcats':casg
    }
    return render(request, 'posApp/manage_purchasebook.html', context)

@login_required
def Save_purchasebook(request):
    data = request.POST
    print(data)
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            uuu = Vendors.objects.filter(id=data['vendor_id']).first()
            ccc = Cashcats.objects.filter(id=data['cass_id']).first()
            save_purchasebook = Purchasebook.objects.filter(id=data['id']).update(username=uuu,cashty=ccc,payment=data['name-payment'],
                                                                        ammount=data['amount'],
                                                                        descri=data['description'],
                                                                        ct=data['cashflow'],
                                                                        tr=data['transaction']
                                                                        )
        else:
            uuu = Vendors.objects.filter(id=data['vendor_id']).first()
            ccc = Cashcats.objects.filter(id=data['cass_id']).first()
            save_purchasebook = Purchasebook(username=uuu,cashty=ccc,payment=data['name-payment'],
                                            ammount=data['amount'],
                                            descri=data['description'],
                                            ct=data['cashflow'],
                                            tr=data['transaction']
                                            )
            save_purchasebook.save()

        resp['status'] = 'success'
        messages.success(request, 'Stock Entry Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_purchasebook(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Purchasebook.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Purchasebook Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

### End Purchasebook Section


@login_required
#Sales Report page; Sales_report page; sale_report page; sale report page ##I need this for ctrl-f
def data_sale(request, date_from="", date_to=""):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    DTF = ""
    DTT = ""
    date_to_temp = date_to


    CURR_TIME = timezone.now().strftime("%Y%m%d")
    SALES_DATE = "posApp_sales.date_added"

    
    #Logic to Parse date from and date to such that it's a valid SQL query to add on to the main query
    date_range_query = ""

    date_from_queried = date_from.replace("-","")
    date_to_queried = date_to.replace("-","")

    if date_from != "" and date_to != "":
        DTF = parser.parse(date_from)
        DTT = parser.parse(date_to)
        if DTF != "" and DTT != "" and DTF > DTT:
            date_from,date_to = date_to,date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{date_to_queried}'"
    
    elif date_from != "" and date_to == "":
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"

    elif date_from == "" and date_to != "":
        date_from,date_to = date_to,date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"
        

    #sqlEngine       = create_engine(f'mysql+pymysql://{CR.DB_USER}:{CR.DB_PASSWORD}@127.0.0.1/{CR.DB_NAME}', pool_recycle=3600)
    #sqlEngine       = create_engine('user:password@domain/dbname', pool_recycle=3600)
    sqlEngine       = create_engine(CR.DB_ENGINE, pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    FR= pd.read_sql("select   DATE_FORMAT(posApp_sales.date_added,'%%d %%M %%Y') as Date,posApp_products.name as product_name, transport,labour, posApp_salesitems.price,posApp_sales.grand_total , posApp_salesitems.qty , posApp_sales.code,posApp_sales.Saletype ,posApp_customer.name as customer_name,posApp_employees.name as Salesperson_name"
                        " from posApp_products,  posApp_salesitems, posApp_sales,posApp_customer, posApp_employees "
                        "where  posApp_sales.id =  posApp_salesitems.sale_id_id and posApp_salesitems.product_id_id = posApp_products.id and posApp_sales.customerID_id = posApp_customer.id"
                        " and posApp_sales.empID_id = posApp_employees.id "+date_range_query, dbConnection);
    FR = FR.replace({'Saletype': {1: 'Debit', 2: 'Credit', 3: 'Prepaid'}})
    FR = FR.sort_values(by=['code'])
    print(FR)

    
    FR_columns = [s.replace("_"," ").title() for s in FR.columns.values]
    #There has to be a way to automate this

    FR.columns = FR_columns

    FR.to_csv('posApp/files/Payment.csv')
    
    FRS = FR.style\
        .format(precision=3, thousands=",", decimal=".")\
        .set_table_attributes('class="table table-striped table-bordered" id="sales_report_table" name="sales_report_table"')\
        .to_html()
    
    print(FRS)
        
    #SL = pd.DataFrame(item3)
    #SL = SL.replace({'type': {1: 'Stockin', 2: 'Return', 3: 'Mixed',4: 'Sale', 6: 'Homeusage'}})
    #SI = pd.DataFrame(item2)
    #SL.to_csv('posApp/files/Stocklist.csv')

    mydict = {
        #"itemlist": FR.to_html(),
        "itemlist": FRS,
        "current_date_time": timezone.now,
        "date_from": date_from,
        "date_to": date_to
        
    }
    dbConnection.close()
    return render(request, 'posApp/LOL.html', context=mydict)

@login_required
def mix_stock(request):
    product_list = Products.objects.all()
    M1 = Mixed1(request.POST)
    if request.POST:
        M1 = Mixed1(request.POST)
        product = Products.objects.filter(id=int(request.POST['product'])).first()
        if M1.is_valid():
            Stock(product=product, quantity=request.POST["quantity"], stock_type='3').save()
            return HttpResponseRedirect('http://127.0.0.1:90/mixed2')

    context = {
        'page_title': 'Mixing 1',
        'products': product_list,
        'Mixed1':M1,
    }
    return render(request, 'posApp/mix_stock.html', context)

@login_required
def mix_stock2(request):
    product_list = Products.objects.all()
    M1 = Mixed1(request.POST)
    if request.POST:
        M1 = Mixed1(request.POST)
        product = Products.objects.filter(id=int(request.POST['product'])).first()
        if M1.is_valid():
            Stock(product=product, quantity=request.POST["quantity"], stock_type='3').save()
            return HttpResponseRedirect('http://127.0.0.1:90/mixeditems')

    context = {
        'page_title': 'Mixing 2',
        'products': product_list,
        'Mixed1':M1,
    }
    return render(request, 'posApp/mix_stock2.html', context)

@login_required
def mixed_item(request):
    product_list = Products.objects.all()
    M1 = Mixed1(request.POST)
    if request.POST:
        M1 = Mixed1(request.POST)
        product = Products.objects.filter(id=int(request.POST['product'])).first()
        if M1.is_valid():
            Stock(product=product, quantity=request.POST["quantity"], stock_type='1').save()
            return HttpResponseRedirect('http://127.0.0.1:90/stock')

    context = {
        'page_title': 'Mixed Items',
        'products': product_list,
        'Mixed1':M1,
    }
    return render(request, 'posApp/mix_item.html', context)

@login_required
def lb_manage(request):
    product_list = Category.objects.all()
    lb_list = Pounds.objects.all()
    M1 = lbmatrix(request.POST)
    if request.POST:
        M1 = lbmatrix(request.POST)
        print(M1)
        print(M1)
        product = Products.objects.filter(id=int(request.POST['cat'])).first()
        if M1.is_valid():
            if request.POST["type"]== "1":
                M1.save()
            elif request.POST["type"]== "2":
                M1.save()
                Stock(product=product, quantity=1, stock_type='1').save()
    context = {
        'page_title': 'Excess Management',
        'products':product_list,
        'stocks': lb_list,
        'Mixed1':M1,
    }
    return render(request, 'posApp/lb_management.html', context)

@login_required
def divide_manage(request):
    product_list = Products.objects.all()
    M1 = divide(request.POST)
    if request.POST:
        M1 = divide(request.POST)
        print(M1)
        product = Products.objects.filter(id=int(request.POST['product'])).first()
        product2 = Products.objects.filter(id=int(request.POST['dividedproduct'])).first()
        qty = request.POST['quantity']
        qty2 = request.POST['quantity2']
        if M1.is_valid():
            Stock(product=product, quantity=qty, stock_type='8').save()
            Stock(product=product2, quantity=qty2 , stock_type='1').save()
    context = {
        'page_title': 'Excess Management',
        'products':product_list,
        'Mixed1':M1,
    }
    return render(request, 'posApp/divide_management.html', context)
# Create your views here.
#select posApp_products.name,  posApp_salesitems.price,posApp_sales.grand_total , posApp_salesitems.qty , posApp_sales.code,  posApp_sales.date_added from posApp_products,  posApp_salesitems, posApp_sales where  posApp_sales.id =  posApp_salesitems.sale_id_id and posApp_salesitems.product_id_id = posApp_products.id

@login_required

def data_stock(request, date_from="", date_to=""):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    DTF = ""
    DTT = ""
    date_to_temp = date_to

    CURR_TIME = timezone.now().strftime("%Y%m%d")
    SALES_DATE = "posApp_stock.date_created"

    # Logic to Parse date from and date to such that it's a valid SQL query to add on to the main query
    date_range_query = ""

    date_from_queried = date_from.replace("-", "")
    date_to_queried = date_to.replace("-", "")

    if date_from != "" and date_to != "":
        DTF = parser.parse(date_from)
        DTT = parser.parse(date_to)
        if DTF != "" and DTT != "" and DTF > DTT:
            date_from, date_to = date_to, date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{date_to_queried}'"

    elif date_from != "" and date_to == "":
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"

    elif date_from == "" and date_to != "":
        date_from, date_to = date_to, date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"

    # sqlEngine = create_engine(f'mysql+pymysql://root:ChaoSlk1!#$!EEW@127.0.0.1/bt', pool_recycle=3600)
    # sqlEngine       = create_engine('user:password@domain/dbname', pool_recycle=3600)
    sqlEngine = create_engine(CR.DB_ENGINE, pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    FR = pd.read_sql(
        "select DATE_FORMAT(posApp_stock.date_created,'%%d %%M %%Y') as Date, posApp_products.name as product, posApp_stock.quantity,  "
        "posApp_stock.stock_type as type,  posApp_stock.cost from posApp_stock, posApp_products where posApp_stock.product_id=posApp_products.id " + date_range_query, dbConnection);
    FR = FR.replace({'type': {1: 'Stock In', 2: 'Return', 3:'Mix',4: 'Sale', 5:'HomeUsage', 6:'Damaged', 7:'General', 8:'Divide' , 9:'ShweBo Return'}})
    FR = FR.sort_values(by=['Date'])
    print(FR)

    FR_columns = [s.replace("_", " ").title() for s in FR.columns.values]
    # There has to be a way to automate this

    FR.columns = FR_columns

    FR.to_csv('posApp/files/Payment.csv')

    FRS = FR.style \
        .format(precision=3, thousands=",", decimal=".") \
        .set_table_attributes(
        'class="table table-striped table-bordered" id="stock_report_table" name="stock_report_table"') \
        .to_html()

    print(FRS)

    # SL = pd.DataFrame(item3)
    # SL = SL.replace({'type': {1: 'Stockin', 2: 'Return', 3: 'Mixed',4: 'Sale', 6: 'Homeusage'}})
    # SI = pd.DataFrame(item2)
    # SL.to_csv('posApp/files/Stocklist.csv')

    mydict = {
        # "itemlist": FR.to_html(),
        "itemlist": FRS,
        "current_date_time": timezone.now,
        "date_from": date_from,
        "date_to": date_to

    }
    dbConnection.close()
    return render(request, 'posApp/stock_report.html', context=mydict)

@login_required

def data_lb(request, date_from="", date_to=""):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    DTF = ""
    DTT = ""
    date_to_temp = date_to

    CURR_TIME = timezone.now().strftime("%Y%m%d")
    SALES_DATE = "posApp_pounds.date_created"

    # Logic to Parse date from and date to such that it's a valid SQL query to add on to the main query
    date_range_query = ""

    date_from_queried = date_from.replace("-", "")
    date_to_queried = date_to.replace("-", "")

    if date_from != "" and date_to != "":
        DTF = parser.parse(date_from)
        DTT = parser.parse(date_to)
        if DTF != "" and DTT != "" and DTF > DTT:
            date_from, date_to = date_to, date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{date_to_queried}'"

    elif date_from != "" and date_to == "":
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"

    elif date_from == "" and date_to != "":
        date_from, date_to = date_to, date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"

    # sqlEngine = create_engine(f'mysql+pymysql://root:ChaoSlk1!#$!EEW@127.0.0.1/bt', pool_recycle=3600)
    # sqlEngine       = create_engine('user:password@domain/dbname', pool_recycle=3600)
    sqlEngine = create_engine(CR.DB_ENGINE, pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    FR = pd.read_sql(
        "SELECT DATE_FORMAT(posApp_pounds.date_created,'%%d %%M %%Y') as Date, posApp_category.name, posApp_pounds.lb,posApp_pounds.type, posApp_pounds.comment from posApp_pounds,"
        " posApp_category where posApp_pounds.product_id = posApp_category.id " + date_range_query, dbConnection);
    FR = FR.replace({'type': {1: 'In', 2: 'Out'}})
    FR = FR.sort_values(by=['Date'])
    print(FR)

    FR_columns = [s.replace("_", " ").title() for s in FR.columns.values]
    # There has to be a way to automate this

    FR.columns = FR_columns

    FR.to_csv('posApp/files/Payment.csv')

    FRS = FR.style \
        .format(precision=3, thousands=",", decimal=".") \
        .set_table_attributes(
        'class="table table-striped table-bordered" id="pound_report_table" name="pound_report_table"') \
        .to_html()

    print(FRS)

    mydict = {
        "itemlist": FRS,
        "current_date_time": timezone.now,
        "date_from": date_from,
        "date_to": date_to

    }
    dbConnection.close()
    return render(request, 'posApp/pound_report.html', context=mydict)

@login_required
def data_cash(request, date_from="", date_to=""):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    DTF = ""
    DTT = ""
    date_to_temp = date_to

    CURR_TIME = timezone.now().strftime("%Y%m%d")
    SALES_DATE = "posApp_cashbook.date_created"

    # Logic to Parse date from and date to such that it's a valid SQL query to add on to the main query
    date_range_query = ""

    date_from_queried = date_from.replace("-", "")
    date_to_queried = date_to.replace("-", "")

    if date_from != "" and date_to != "":
        DTF = parser.parse(date_from)
        DTT = parser.parse(date_to)
        if DTF != "" and DTT != "" and DTF > DTT:
            date_from, date_to = date_to, date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{date_to_queried}'"

    elif date_from != "" and date_to == "":
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"

    elif date_from == "" and date_to != "":
        date_from, date_to = date_to, date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"

    # sqlEngine = create_engine(f'mysql+pymysql://root:ChaoSlk1!#$!EEW@127.0.0.1/bt', pool_recycle=3600)
    # sqlEngine       = create_engine('user:password@domain/dbname', pool_recycle=3600)
    sqlEngine       = create_engine(CR.DB_ENGINE, pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    FR = pd.read_sql(
        "select DATE_FORMAT(posApp_cashbook.date_created,'%%d %%M %%Y') as Date, posApp_customer.name ,posapp_cashcats.cashcatg,posApp_cashbook.payment as name,ammount, posApp_cashbook.descri as Description, posApp_cashbook.ct as type, posApp_cashbook.tr as transfer_method from posApp_cashbook, posapp_customer, posapp_cashcats where posApp_cashbook.id = posApp_cashbook.id and posApp_cashbook.username_id = posapp_customer.id and  posApp_cashbook.cashty_id = posapp_cashcats.id "+ date_range_query, dbConnection);
    FR = FR.replace({'type': {1: 'In', 2: 'Out', 3:"Credit"}, 'transfer_method':{1: 'Cash Payment', 2: 'Bank Transfer'}})
    FR = FR.sort_values(by=['Date'])
    print(FR)

    FR_columns = [s.replace("_", " ").title() for s in FR.columns.values]
    # There has to be a way to automate this

    FR.columns = FR_columns

    FR.to_csv('posApp/files/Payment.csv')

    FRS = FR.style \
        .format(precision=3, thousands=",", decimal=".") \
        .set_table_attributes(
        'class="table table-striped table-bordered" id="cash_report_table" name="cash_report_table"') \
        .to_html()

    print(FRS)

    mydict = {
        "itemlist": FRS,
        "current_date_time": timezone.now,
        "date_from": date_from,
        "date_to": date_to

    }
    dbConnection.close()
    return render(request, 'posApp/cash_report.html', context=mydict)

@login_required
def data_prepaid(request, date_from="", date_to=""):
    if not request.user.email.endswith('@admin.com'):
        return redirect('/login?next=/' % request.path)
    DTF = ""
    DTT = ""
    date_to_temp = date_to

    CURR_TIME = timezone.now().strftime("%Y%m%d")
    SALES_DATE = "posApp_pre_stock.date_created"

    # Logic to Parse date from and date to such that it's a valid SQL query to add on to the main query
    date_range_query = ""

    date_from_queried = date_from.replace("-", "")
    date_to_queried = date_to.replace("-", "")

    if date_from != "" and date_to != "":
        DTF = parser.parse(date_from)
        DTT = parser.parse(date_to)
        if DTF != "" and DTT != "" and DTF > DTT:
            date_from, date_to = date_to, date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{date_to_queried}'"

    elif date_from != "" and date_to == "":
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"

    elif date_from == "" and date_to != "":
        date_from, date_to = date_to, date_from
        date_range_query += f"and {SALES_DATE} >= '{date_from_queried}' and {SALES_DATE} <= '{CURR_TIME}'"

    # sqlEngine = create_engine(f'mysql+pymysql://root:ChaoSlk1!#$!EEW@127.0.0.1/bt', pool_recycle=3600)
    # sqlEngine       = create_engine('user:password@domain/dbname', pool_recycle=3600)
    sqlEngine       = create_engine(CR.DB_ENGINE, pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    FR = pd.read_sql(
            "select  DATE_FORMAT(posApp_pre_stock.date_created,'%%d %%M %%Y') as Date, posapp_customer.name, posapp_products.name,posapp_sales.code,quantity,type from posapp_pre_stock, posapp_customer, posapp_products, "
            "posapp_sales where posapp_pre_stock.customer_id = posapp_customer.id and posapp_pre_stock.product_id = posapp_products.id and posapp_pre_stock.code_id = posapp_sales.id "+ date_range_query, dbConnection);
    FR = FR.replace({'type': {1: 'In', 2: 'Out'}})
    FR = FR.sort_values(by=['Date'])
    print(FR)

    FR_columns = [s.replace("_", " ").title() for s in FR.columns.values]
    # There has to be a way to automate this

    FR.columns = FR_columns

    FR.to_csv('posApp/files/Payment.csv')

    FRS = FR.style \
        .format(precision=3, thousands=",", decimal=".") \
        .set_table_attributes(
        'class="table table-striped table-bordered" id="cash_report_table" name="cash_report_table"') \
        .to_html()

    print(FRS)

    mydict = {
        "itemlist": FRS,
        "current_date_time": timezone.now,
        "date_from": date_from,
        "date_to": date_to

    }
    dbConnection.close()
    return render(request, 'posApp/prepaid_report.html', context=mydict)

@login_required
def purchase(request):
    products = Products.objects.filter(status=1)
    data = request.POST
    Customers = Vendors.objects.all()
    costprice = Stock.objects.all()
    M1 = poscost(request.POST)
    product_json = []
    print(M1)
    for product in products:
        product_json.append({'id': product.id, 'name': product.name, 'price': float(product.price)})
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'product_json': json.dumps(product_json),
        'Customers': Customers,
        'Costprices':costprice,
        'cost':M1,
    }
    # return HttpResponse('')
    return render(request, 'posApp/Purchase.html', context)


@login_required
def save_purchase(request):
    resp = {'status': 'failed', 'msg': ''}
    data = request.POST
    pref = "5000"
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Purchase.objects.filter(code=str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        customer = Vendors.objects.filter(id=int(data['customer_id'])).first()
        grandtotal = float(data['grand_total'])
        sales = Purchase(shopsID=customer, code=code, sub_total=data['sub_total'],grand_total=grandtotal,Saletype=data['sale_type']).save()
        sale_id = Purchase.objects.last().pk
        salety = data['sale_type']
        if salety == '2':
            Cashbook(username=customer, payment=code, descri="Credit Sale", ammount=data['grand_total'], ct=3).save()
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod
            sale = Purchase.objects.filter(id=sale_id).first()

            product = Products.objects.filter(id=product_id).first()
            print("pass!!!!!")
            qty = data.getlist('qty[]')[i]
            price = data.getlist('price[]')[i]
            total = float(qty) * float(price)
            print({'sale_id': sale, 'product_id': product, 'qty': qty, 'price': price, 'total': total})
            customerid = Vendors.objects.filter(id=int(data['customer_id'])).first()
            PurchaseItems(sale_id=sale, product_id=product, qty=qty, price=price, total=total).save()
            SaleCount(product_id=product, qty=qty).save()
            print("pass!")
            if salety == '3':
                Pre_Purchase(product=product, customer=customerid, quantity=qty, code=sale, type='1').save()
            else:
                Stock(product=product, quantity=qty, stock_type='1').save()
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Sale Record has been saved.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type="application/json")