#!/usr/bin/python
# -*- coding: UTF-8 -*-
import fundProdma
import fundProdCenter
import os
import json
import threading
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def diff(rowM,rowC):
    dict = {}
    dict["productname"] = rowM[0] if rowM[0] == rowC[0] else rowM[0] + " | " + rowC[0]
    dict["seccode"]= rowM[1] if rowM[1] == rowC[1] else rowM[1] + " | " + rowC[1]
    dict["isETF"] = rowM[2] if rowM[2] == rowC[2] else rowM[2] + " | " + rowC[2]
    dict["isLOF"]= rowM[3] if rowM[3] == rowC[3] else rowM[3] + " | " + rowC[3]
    dict["isQDII"] = rowM[4] if rowM[4] == rowC[4] else rowM[4] + " | " + rowC[4]
    dict["isBreakeven"]=  rowM[5] if rowM[5] == rowC[5] else rowM[5] + " | " + rowC[5]
    dict["isLevel"] = rowM[6] if rowM[6] == rowC[6] else rowM[6] + " | " + rowC[6]
    dict["gradingMechanism"]= rowM[7] if rowM[7] == rowC[7] else (str(rowM[7]) or "no value") + " | " + (str(rowC[7]) or "no value")
    dict["investmentStrategy"] = rowM[8] if rowM[8] == rowC[8] else (str(rowM[8]) or "no value") + " | " + (str(rowC[8]) or "no value")
    dict["managerName"]= rowM[9] if rowM[9] == rowC[9] else (str(rowM[9]) or "no value") + " | " + (str(rowC[9]) or "no value")
    dict["moneyType"] = rowM[10] if rowM[10] == rowC[10] else (str(rowM[10]) or "no value") + " | " + (str(rowC[10]) or "no value")
    dict["investmentScope"]=  rowM[11] if rowM[11] == rowC[11] else (str(rowM[11]) or "no value") + " | " + (str(rowC[11]) or "no value")
    dict["performanceBenchmark"]= rowM[12] if rowM[12] == rowC[12] else (str(rowM[12]) or "no value") + " | " + (str(rowM[12]) or "no value")
    dict["manageFee"]= rowM[13] if rowM[13] == rowC[13] else (str(rowM[13]) or "no value") + " | " + (str(rowC[13]) or "no value")
    if rowM[13] == None or rowC[13] == None:
        dict["manageFee"]= str(rowM[13]) + " | " + str(rowC[13])
    else:
        if float(rowM[13]) == float(rowC[13]):
            dict["manageFee"] = rowM[13]
        else:
            dict["manageFee"]= str(rowM[13]) + " | " + str(rowC[13])
    if rowM[14] == None or rowC[14] == None:
        dict["trustFee"]= str(rowM[14]) + " | " + str(rowC[14])
    else:
        if float(rowM[14]) == float(rowC[14]):
            dict["trustFee"]= rowM[14]
        else:
            dict["trustFee"]= str(rowM[14]) + " | " + str(rowC[14])
    dict["custodian"]= rowM[15] if rowM[15] == rowC[15] else (str(rowM[15]) or "no value") + " | " + (str(rowC[15]) or "no value")
    dict["minSubscribeAmount"]= rowM[16] if rowM[16] == rowC[16] else (str(rowM[16]) or "no value") + " | " + (str(rowC[16]) or "no value")
    return dict

def queryFundData():
    t = threading.Thread(target=getFundProdmaData, name='thread1')
    t.start()
    resultFundProdCenter = fundProdCenter.getFundData()
    t.join()
    results = []
    for rowM in resultFundProdma:
        for rowC in resultFundProdCenter:
            if rowM[1] == rowC[1]:
                results.append(diff(rowM,rowC))
    return json.dumps(results)

def getFundProdmaData():
    global resultFundProdma
    resultFundProdma = fundProdma.getFundData()

def queryDiffFundRecords():
#if __name__=="__main__":
    t = threading.Thread(target=getFundProdmaData, name='thread1')
    t.start()
    resultFundProdCenter = fundProdCenter.getFundData()
    t.join()
    sameRecords = []
    results = []
    for rowM in resultFundProdma:
        for rowC in resultFundProdCenter:
            if rowM[1] == rowC[1]:
                sameRecords.append(rowM[1])

    for row in resultFundProdma:
        if not row[1] in sameRecords:
            results.append(diff(row,row))

    for row in resultFundProdCenter:
        if not row[1] in sameRecords:
            results.append(diff(row,row))
#    print( json.dumps(results))
    print("000000000000000")
    return json.dumps(results)
