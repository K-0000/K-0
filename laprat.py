import pandas as pd
import glob
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#Sale
Tk().withdraw()
path = r""+askopenfilename()
df = pd.read_csv(path)
TP= df.groupby(['Code']).agg({'Transport':'mean','Labour':'mean'})
Tr= TP.Transport.sum()
La= TP.Labour.sum()
group = df.groupby(['Date','Salesperson Name','Customer Name','Product Name','Saletype','Price','Transport']).agg({'Qty':'sum'})
group.to_csv('Byprice.csv')
df = pd.read_csv('Byprice.csv')
df['SoldTotal'] = (df['Price'] * df['Qty'])
print(df.head())
df2 = df.append(pd.DataFrame(df.SoldTotal.sum()+Tr+La, index = ["Total"], columns=[ "SoldTotal"]))
df2.to_csv('C:/Users/User-MDY-BT/Desktop/generated/Byprice.csv')
group = df.groupby(['Product Name']).agg({'Qty':'sum'})
group.to_csv('C:/Users/User-MDY-BT/Desktop/generated/Byproduct.csv')
sale = df.SoldTotal.sum()+Tr+La
#Cash
Tk().withdraw()
path = r""+askopenfilename()
df = pd.read_csv(path)
otr = df[df["Type"]== "Out"]
itr = df[df["Type"]== "In"]
outmon= otr.Ammount.sum()
otr = otr.append(pd.DataFrame(otr.Ammount.sum(), index = ["Total"], columns=[ "Ammount"]))
otr.to_csv('C:/Users/User-MDY-BT/Desktop/generated/OutCashreport.csv')
Inmon= itr.Ammount.sum()
itr = itr.append(pd.DataFrame(itr.Ammount.sum(), index = ["Total"], columns=[ "Ammount"]))
itr.to_csv('C:/Users/User-MDY-BT/Desktop/generated/InCashreport.csv')
ctr = df[df["Type"]== "Credit"]
creddit=ctr.Ammount.sum()
ctr = ctr.append(pd.DataFrame(ctr.Ammount.sum(), index = ["Total"], columns=[ "Ammount"]))
ctr.to_csv('C:/Users/User-MDY-BT/Desktop/generated/Creditreport.csv')

#Stockin
Tk().withdraw()
path = r""+askopenfilename()
df = pd.read_csv(path)
stockin = df[df["Type"]== "Stock In"]
mix = df[df["Type"]== "Mixed"]
mix= mix.groupby(['Date','Product','Type']).agg({'Quantity':'sum'})
divide = df[df["Type"]== "Divide"]
divide= divide.groupby(['Date','Product','Type']).agg({'Quantity':'sum'})
damage = df[df["Type"]== "Damaged"]
damage= damage.groupby(['Date','Product','Type']).agg({'Quantity':'sum'})
stockin.to_csv('C:/Users/User-MDY-BT/Desktop/generated/stockin.csv')
divide.to_csv('C:/Users/User-MDY-BT/Desktop/generated/divide.csv')
mix.to_csv('C:/Users/User-MDY-BT/Desktop/generated/mix.csv')
mix.to_csv('C:/Users/User-MDY-BT/Desktop/generated/damage.csv')


Inn = (sale+Inmon)
Outt = (outmon+creddit)
Calculated = Inn - Outt
Outcash = {"col":[sale,outmon,Inmon,creddit,Calculated]}
total=pd.DataFrame(Outcash, index=["Sale","Outcash","Incash","Credit", "Closing Money"])
print(total)
total.to_csv("C:/Users/User-MDY-BT/Desktop/generated/CashClose.csv")