def sumAllIndex(authors):
    finalSum = 0
    for i in authors:
        finalSum += int(i["hindex"])
    return {"Сумма hIndex:": finalSum}
