# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:00:14 2021

@author: alma_
"""

import requests
import json
import os  
import xlrd
import random
import uuid
import time
 
def generateOrders(totalOrders):
    validItems = getValidItems()
   
    omsSeg = '"oms": {'\
          '"ordr_id": 10,'\
          '"version": "1.100",'\
          '"workflow": "eFC 2.0",'\
          '"from_event": "ORDER_CHANGE_ITEM_REQUEST",'\
          '"event_end_time": "2021-01-14 22:48:38.491",'\
          '"order_reference": "'+str(uuid.uuid1()).replace("-", "")+'",'\
          '"requested_event": "ORDER_ENTRY_WMS",'\
          '"event_start_time": "2021-01-14 22:48:38.506",'\
          '"customer_order_reference": "5b14ae88-2e0f-4368-a1f8-cd47be6c209c1"'\
          '},'
    
    itemSeg = ''
    #generate item list
    for i in range(totalOrders):
        itemSeg += '{"name": "Molde Corazon Nyc Pop Cit",' 
        itemSeg += '"unit": "PZ",' 
        itemSeg +='"price": 0,' 
        itemSeg +='"comment": "",' 
        itemSeg +='"quantity": '+ str(random.randint(1,20))+',' 
        itemSeg +=' "attributes": {' 
        itemSeg +=' "ean": "7501044028850",'
        itemSeg += ' "sku": "' + str(round(validItems[random.randint(1,1600)]))+'",'
        itemSeg += '"weight_unit": "g",'
        itemSeg +='"weight_quantity": "0.100"}'
        if i + 1 < totalOrders:
            itemSeg += ', '
            
    destSeg = '"destination": {'\
        ' "schedule": {'\
        '"end": "2021-03-16T18:54:14.756Z",'\
        ' "start": "2020-12-28T17:10:54.203Z"}'\
            '},'
        
    print(omsSeg +'\n'+ itemSeg+'\n'+destSeg)


def getValidItems():
    # Give the location of the file
    loc = ("ListProd.xlsx")
     
    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
     
    # For row 0 and column 0
    print(sheet.cell_value(0, 0))
    
    arrayofvalues = sheet.col_values(0)
    
    return arrayofvalues


# vals_list = df['ARTICULO'].tolist()
# print(vals_list)

def readFiles():
    
    # specify your path of directory
    path = r"C:\alma\HEB\OMS\tests\20210121\JSON_ORDENES_21_22_CERT_y_PROD\Finales"
     
    # call listdir() method
    # path is a directory of which you want to list
    directories = os.listdir( path )
     
    # This would print all the files and directories
    for file in directories:
       if '.json' in file:
           sendOrder(file)
           # Wait for 5 seconds
           time.sleep(15)
       

def sendOrder(file_name):
    
    newHeaders = {'Content-type': 'application/json', 'Accept': '*/*','Accept-Encoding':'gzip, deflate, br', 'Connection':'keep-alive'}
    
    #file_name = 'ORDWMS20200121_TST002.json'
    # read file
    with open(file_name, 'rb') as myfile:
        data=myfile.read()
         
    
    response = requests.post('http://sdi201165:53403/oms/v1/sendOrderWms',
                             data=data,
                             headers=newHeaders)
    print (file_name)
    print("Status code: ", response.status_code)
    
    response_Json = response.json()
    print("Printing Post JSON data")
    print(response_Json)
    
    
    print('**********************************')
    
    #print("Content-Type is ", response_Json['headers']['Content-Type'])