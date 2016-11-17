#!/usr/bin/python
# -*- coding: UTF-8 -*-
import fundProdma
import fundProdCenter
import os
import json
import threading
#import sqlite3

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def diff(rowM,rowC):
    dict = {}
    for x,y in rowM.items():
        if x == "manageFee" or x == "trustFee":
            if rowM[x] == None or rowC[x] == None:
                dict[x]= str(rowM[x]) + " | " + str(rowC[x])
            else:
                if float(rowM[x]) == float(rowC[x]):
                    dict[x] = rowM[x]
                else:
                    dict[x]= str(rowM[x]) + " | " + str(rowC[x])
        elif x ==  "productname":
            dict[x] =  rowM[x]
        elif x == "moneyType":
            if rowM[x] and rowM[x] in rowC[x]:
                dict[x] =  rowM[x]
            else:
                dict[x] = rowM[x] if rowM[x] == rowC[x] else (str(rowM[x]) + " | " + str(rowC[x]))
        else:
            dict[x] = rowM[x] if rowM[x] == rowC[x] else (str(rowM[x]) + " | " + str(rowC[x]))
    return dict

def model(row):
    dict = {}
    dict["productname"] = row[0]
    dict["seccode"]= row[1]
    dict["isETF"] = row[2]
    dict["isLOF"]= row[3]
    dict["isQDII"] = row[4]
    dict["isBreakeven"]=  row[5]
    dict["isLevel"] = row[6]
    dict["gradingMechanism"] = row[7]
    dict["investmentStrategy"] = row[8]
    #dict["managerName"]= row[9]
    dict["moneyType"] = row[10]
    #dict["investmentScope"]=  row[11]
    dict["performanceBenchmark"]= row[12]
    dict["manageFee"] = row[13]
    dict["trustFee"]= row[14]
    dict["custodian"]= row[15]
    dict["minSubscribeAmount"]= row[16]
    dict["FeeCount"]= row[17]
    dict["managerCount"]= row[18]
    return dict

# get the fund data that record can be found in fundcenter or in fundprodma but not both
def queryOnleProdmaFundData():
    records = getAllFundRecords()
    results = []
    for x,y in records.items():
        if len(y) == 1 and y[0]["comefrom"] == '1':
            results.append(y[0])
    return json.dumps({'rows':results,'total':'50000'})

def queryOnleProdCenterFundData():
    records = getAllFundRecords()
    results = []
    for x,y in records.items():
        if len(y) == 1 and y[0]["comefrom"] == '2':
            results.append(y[0])
    return json.dumps({'rows':results,'total':'50000'})

# thread that get fundprodma data
def getFundProdmaData():
    global resultFundProdma
    resultFundProdma = fundProdma.getFundData()

# get the fund data that record can be found in both fundcenter and fundprodma
def queryDiffFundRecords():
    results = []
    records = getAllFundRecords()
    for x,y in records.items():
        if len(y) == 2:
            results.append(diff(y[0],y[1]))
    return json.dumps({'rows':results,'total':'50000'})

def queryFundProdmaOriginalData():
    results=[]
    funds = fundProdma.getFundData()
    for row in funds:
        m = model(row)
        results.append(m)
    return json.dumps({'rows':results,'total':'50000'})

def queryFundProdCenterOriginalData():
    results=[]
    funds = fundProdCenter.getFundData()
    for row in funds:
        m = model(row)
        results.append(m)
    return json.dumps({'rows':results,'total':'50000'})

def getAllFundRecords():
#if __name__=="__main__":
    t = threading.Thread(target=getFundProdmaData, name='thread1')
    t.start()
    resultFundProdCenter = fundProdCenter.getFundData()
    t.join()
    print("resultFundProdCenter:" + str(len(resultFundProdCenter)))
    print("resultFundProdma:" + str(len(resultFundProdma)))
    #conn = create_table('/home/vagrant/lixc/tutorial/tutorial/db.sqlite')
    #for row in resultFundProdCenter:
    #    conn.execute('replace into fund values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16],"1",datetime.datetime.now().date()))

    results = {}

    for row in resultFundProdma:
        #if not results.get(row[1]):
        m = model(row)
        m['comefrom'] = '1'
        results[row[1]] =  [m]

    for row in resultFundProdCenter:
        m = model(row)
        m['comefrom'] = '2'
        if not row[1] in results:
            results[row[1]] =  [m]
        else:
            results.get(row[1]).append(m)
    return results
#    print( json.dumps(results))

#def create_table(filename):
#    conn = sqlite3.connect(filename)
#    conn.execute("""create table if not exists fund
#                (productname text,
#                seccode text,
#                isETF text,
#                isLOF text,
#                isQDII text,
#                isBreakeven text,
#                isLevel text,
#                gradingMechanism text,
#                investmentStrategy text,
#                managerName text,
#                moneyType text,
#                investmentScope text,
#                performanceBenchmark text,
#                manageFee text,
#                trustFee text,
#                custodian text,
#                minSubscribeAmount text,
#                comeFrom int not null,
#                updateDate text,
#                primary key(seccode,comeFrom)
#                )""")
#    conn.commit()
#    return conn

#def queryDiffFundRecords():
##if __name__=="__main__":
#    t = threading.Thread(target=getFundProdmaData, name='thread1')
#    t.start()
#    resultFundProdCenter = fundProdCenter.getFundData()
#    t.join()
#    sameRecords = []
#    results = []
#    for rowM in resultFundProdma:
#        for rowC in resultFundProdCenter:
#            if rowM[1] == rowC[1]:
#                sameRecords.append(rowM[1])
#
#    for row in resultFundProdma:
#        if not row[1] in sameRecords:
#            results.append(diff(row,row))
#
#    for row in resultFundProdCenter:
#        if not row[1] in sameRecords:
#            results.append(diff(row,row))
##    print( json.dumps(results))
#    return json.dumps(results)
