from enum import Enum

STOCK_TYPE = {
    1: "Stockin",
    2: "Return",
    3: "Mixed",
    4: "Sales",
    5: "Home Usage",
    6: "Damaged",
    7: "Unknown",
    8: "Divide",
    9: "Shwebo return",
    0: "Stockout"
}

class StockTypeEnum(Enum):
    STOCKIN = 1
    RETURN = 2
    MIXED = 3
    SALES = 4
    HOME_USAGE = 5
    DAMAGED = 6
    UNKNOWN = 7
    DIVIDE = 8 
    SHWEBO = 9
    STOCKOUT = 0

    def __str__(self):
        return STOCK_TYPE[self.value]
    
    def valInt(self):
        return self.value
    
    def cases():
        return STOCK_TYPE
    

STOCK_AVAILABILITY = {
    1: "On Sale",
    2: "Passive",
    0: "Sold Out"
}

class StockAvailabilityEnum(Enum):
    ON_SALE = 1
    PASSIVE = 2
    SOLD_OUT = 0

    def __str__(self):
        return STOCK_AVAILABILITY[self.value]
    
    def valInt(self):
        return self.value

CASHBOOK_CASHFLOW = {
    1: "Cash In",
    2: "Cash Out",
    3: "Credit",
    0: "Damaged"
}

class Cashbook_CashflowEnum(Enum):
    CASH_IN = 1
    CASH_OUT = 2
    CREDIT = 3
    DAMAGeD = 0

    def __str__(self):
        return CASHBOOK_CASHFLOW[self.value]
    
    def valInt(self):
        return self.value

CASHBOOK_TRANSACTION = {
    1: "Cash Payment",
    2: "Bank Transfer",
    0: "Damaged"
}

class Cashbook_TransactionEnum(Enum):
    CASH_PAYMENT = 1
    BANK_TRANSFER = 2
    DAMAGED = 0
    def __str__(self):
        return CASHBOOK_TRANSACTION[self.value]
    
    def valInt(self):
        return self.value
