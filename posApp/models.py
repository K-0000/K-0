from django.db import models
from datetime import datetime
from unicodedata import category
from django.db import models
from django.utils import timezone

from .constants import StockTypeEnum as ST
from .constants import StockAvailabilityEnum as SA

# Create your models here.

class Employees(models.Model):
#     code = models.CharField(max_length=100,blank=True)
     name = models.TextField()
#     middlename = models.TextField(blank=True,null= True)
#     lastname = models.TextField()
#     gender = models.TextField(blank=True,null= True)
#     dob = models.DateField(blank=True,null= True)
     contact = models.TextField()
     address = models.TextField()
#     email = models.TextField()
#     department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
#     position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
     date_hired = models.DateField()
#     salary = models.FloatField(default=0)
#     status = models.IntegerField()
     date_added = models.DateTimeField(default=timezone.now)
     date_updated = models.DateTimeField(auto_now=True)

     def __str__(self):
         return self.name

class Customer(models.Model):
    name = models.TextField()
    phone = models.TextField(default="09")
    address = models.TextField()
    comment = models.TextField(default="Na")
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def count_pre(self):
        stocks = Pre_Stock.objects.filter(customer=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == 1:
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available  = stockIn - stockOut
        return available

    def count_credit(self):
        stocks = Cashbook.objects.filter(username=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.ct == 3:
                stockIn = int(stockIn) + int(stock.ammount)
            else:
                stockOut = int(stockOut) + int(stock.ammount)
        available  = stockIn - stockOut
        return available

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def lb_avali(self):
        stocks = Pounds.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == 1:
                stockIn = float(stockIn) + float(stock.lb)
            else:
                stockOut = float(stockOut) + float(stock.lb)
        available  = stockIn-stockOut
        return available

    def lb_in(self):
        stocks = Pounds.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == 1:
                stockIn = float(stockIn) + float(stock.lb)
        available  = stockIn
        return available

    def lb_out(self):
        stocks = Pounds.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == 1:
                stockIn = float(stockIn) + float(stock.lb)
            else:
                stockOut = float(stockOut) + float(stock.lb)
        available  = stockOut
        return available

    def __str__(self):
        return self.name

class Products(models.Model):
    code = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField()
    unitname = models.CharField(max_length=100, blank=True, null=True)
    unit = models.FloatField(default=0)
    description = models.TextField()
    price = models.FloatField(default=0)
    cost_price = models.FloatField(default=0)
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    product_image = models.ImageField(upload_to = f'./posApp/product_images/', default='./posApp/product_images/default.png')

    def count_inventory(self):
        stocks = Stock.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.stock_type == 1:
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available  = stockIn - stockOut
        return available

    def total_inventory(self):
        stocks = Stock.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.stock_type == 1:
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available  = stockIn
        return available

    def home_inventory(self):
        stocks = Stock.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.stock_type == 5:
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available  = stockIn
        return available

    def damage_inventory(self):
        stocks = Stock.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.stock_type == 6:
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available  = stockIn
        return available

    def sale_inventory(self):
        stocks = Stock.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.stock_type == 4:
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available  = stockIn
        return available

    def __str__(self):
        return self.code + " - " + self.name

    def lb_avali(self):
        stocks = Pounds.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == 1:
                stockIn = float(stockIn) + float(stock.lb)
            else:
                stockOut = float(stockOut) + float(stock.lb)
        available  = stockIn-stockOut
        return available

    def lb_in(self):
        stocks = Pounds.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == 1:
                stockIn = float(stockIn) + float(stock.lb)
        available  = stockIn
        return available

    def lb_out(self):
        stocks = Pounds.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == 1:
                stockIn = float(stockIn) + float(stock.lb)
            else:
                stockOut = float(stockOut) + float(stock.lb)
        available  = stockOut
        return available

    def costamm(self):
        stocks = Stock.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            stockIn = int(stockIn) + int(stock.quantity) *float(stock.cost)
        available  = stockIn
        return available

    def salecost(self):
        stocks = Stock.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        Count = 0
        Countout=0
        for stock in stocks:
            if stock.OS ==1:
                stockOut= int(stockOut) + int(stock.quantity)
                stockIn = int(stockIn) + float(stock.cost)
        available  = stockIn
        return available

    def Dailycost(self):
        stocks = Stock.objects.filter(product=self)
        stockIn = 0
        stockOut = 0
        Count = 0
        Countout=0
        for stock in stocks:
            if stock.stock_type ==4:
                stockIn = int(stockIn)+ float(stock.cost)*int(stock.quantity)
        available  = stockIn
        return available

    def onsale(self):
        stocks = Stock.objects.filter(product=self)
        salecounts= SaleCount.objects.filter(product_id=self)
        stockIn = 0
        stockOut = 0
        Count = 0
        Countout=0
        for stock in stocks:
            if stock.OS == 1:
                stockIn = int(stockIn) + int(stock.quantity)
        for salecount in salecounts:
            stockOut = int(stockOut) + int(salecount.qty)
        available  = stockIn - stockOut
        return available

    def daily_item_scount(self):
        now = datetime.now()
        current_year = now.strftime("%Y")
        current_month = now.strftime("%m")
        current_day = now.strftime("%d")
        stocks = Stock.objects.filter(date_created__year=current_year,date_created__month=current_month,date_created__day=current_day,product=self)
        stockIn = 0
        for stock in stocks:
            if stock.stock_type ==4:
                stockIn = int(stockIn) + int(stock.quantity)
        available  = stockIn
        return available

    def Month_item_scount(self):
        now = datetime.now()
        current_year = now.strftime("%Y")
        current_month = now.strftime("%m")
        current_day = now.strftime("%d")
        stocks = Stock.objects.filter(date_created__year=current_year,date_created__month=current_month,product=self)
        stockIn = 0
        for stock in stocks:
            if stock.stock_type ==4:
                stockIn = int(stockIn) + int(stock.quantity)
        available  = stockIn
        return available

    def __str__(self):
        return self.code + " - " + self.name


class Stock(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    stock_type = models.FloatField(default=1)
    OS = models.FloatField(default=2)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)


    def stockcostcount(self):
        costs_d = Stock.objects.filter(cost=self.cost)
        Count=0
        Countout=0
        for co in costs_d:
            if co.stock_type == 1:
                Count= int(Count) + int(self.quantity)
            if co.stock_type == 4:
                Countout= int(Countout) + int(self.quantity)
        available  = Count - Countout
        return available
    
    def test_stock_num(self):
        stockd = self.stock_type
        return str(stockd)
    
    def stock_type_verbose(self):
        type_verbose = ""

        stock_type = self.stock_type

        if stock_type == ST.STOCKIN.valInt():
            type_verbose = ST.STOCKIN

        elif stock_type == ST.RETURN.valInt():
            type_verbose = ST.RETURN

        elif stock_type == ST.MIXED.valInt():
            type_verbose = ST.MIXED

        elif stock_type == ST.SALES.valInt():
            type_verbose = ST.SALES

        elif stock_type == ST.HOME_USAGE.valInt():
            type_verbose = ST.HOME_USAGE

        elif stock_type == ST.DAMAGED.valInt():
            type_verbose = ST.DAMAGED

        elif stock_type == ST.UNKNOWN.valInt():
            type_verbose = ST.UNKNOWN

        elif stock_type == ST.DIVIDE.valInt():
            type_verbose = ST.DIVIDE

        elif stock_type == ST.SHWEBO.valInt():
            type_verbose = ST.SHWEBO
        else:
            type_verbose = ST.STOCKOUT

        return type_verbose
    
    
    
    #OS short form for "On Sale" AKA availability
    def stock_OS_verbose(self):
        
        OS_verbose = ""
        
        stock_OS = self.OS

        if stock_OS == SA.ON_SALE.valInt():
            OS_verbose = SA.ON_SALE

        elif stock_OS == SA.PASSIVE.valInt():
            OS_verbose = SA.PASSIVE
        
        else:
            OS_verbose = SA.SOLD_OUT

        return OS_verbose
            

class Sales(models.Model):
    customerID = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    empID = models.ForeignKey(Employees, on_delete=models.CASCADE, default=1)
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    Saletype =  models.IntegerField(default=1)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    transport = models.FloatField(default=0)
    labour = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def count_pre(self):
        stocks = Pre_Stock.objects.filter(code=self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == 1:
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available  = stockIn - stockOut
        return available

    def akos(self):
        totl = float(self.grand_total)
        Tros = self.grand_total
        return self.grand_total

    def __str__(self):
        return self.code

class Pre_Stock(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE,default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,default=1)
    quantity = models.FloatField(default=0)
    code = models.ForeignKey(Sales, on_delete=models.CASCADE,default=1)
    type = models.FloatField(default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

class salesItems(models.Model):
    sale_id = models.ForeignKey(Sales,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)

class Cashcats(models.Model):
    cashcatg = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

class Cashbook(models.Model):
    username = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    cashty  = models.ForeignKey(Cashcats, on_delete=models.CASCADE,default=1)
    payment = models.CharField(max_length=100) # Name in the HTML page
    descri = models.TextField() # Description in the Html Page
    ammount = models.FloatField(default=0) # Amount in the html page
    ct = models.IntegerField(default=1) # Cashflow in the html page
    tr = models.IntegerField(default=1) # Transaction in the html page
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

class Pounds(models.Model):
    product = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    lb = models.FloatField(default=0)
    type = models.FloatField(default=1)
    comment = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

class CostAmmount(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE,default=1)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE,default=1)
    cost = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

class SaleCount(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, default=1)
    qty = models.FloatField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)


class Vendors(models.Model):
    name = models.TextField()
    phone = models.TextField(default="09")
    address = models.TextField()
    comment = models.TextField(default="Na")
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Purchasebook(models.Model):
    username = models.ForeignKey(Vendors, on_delete=models.CASCADE, default=1)
    payment = models.CharField(max_length=100) # Name in the HTML page
    descri = models.TextField() # Description in the Html Page
    ammount = models.FloatField(default=0) # Amount in the html page
    ct = models.IntegerField(default=1) # Cashflow in the html page
    tr = models.IntegerField(default=1) # Transaction in the html page
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

class Purchase(models.Model):
    shopsID = models.ForeignKey(Vendors, on_delete=models.CASCADE, default=1)
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    Saletype =  models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

class PurchaseItems(models.Model):
    sale_id = models.ForeignKey(Purchase,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)

class Pre_Purchase(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE,default=1)
    vendors = models.ForeignKey(Vendors, on_delete=models.CASCADE,default=1)
    quantity = models.FloatField(default=0)
    code = models.ForeignKey(Sales, on_delete=models.CASCADE,default=1)
    type = models.FloatField(default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

