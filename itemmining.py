# -*- coding: utf-8 -*-

import orangecontrib.associate.fpgrowth as or3
import pandas as pd

def emptyList():
    return []

df_OnlineRetail = pd.read_excel('Online Retail.xlsx')

# Make Itemlist

dictItemToKey = {}
dictKeyToItem = {}
dictCounterItem = {}
dictItemToDescription = {}
firstIndex = df_OnlineRetail.iloc[1][0]
IdCounter = 0
ItemList = []

Basket = emptyList()
counter = 0

for index, row in df_OnlineRetail.iterrows():
    if dictItemToKey.get(row[1], None) == None:
        dictItemToKey[row[1]] = IdCounter
        dictItemToDescription[row[1]] = row[2]
        dictCounterItem[row[1]] = 0
        dictKeyToItem[IdCounter] = row[1]
        IdCounter += 1
    dictCounterItem[row[1]] += 1
    Basket.append(dictItemToKey[row[1]])
    if row[0] != firstIndex:
        ItemList.append(Basket)
        Basket = emptyList()
        firstIndex = row[0]    
    counter += 1
    if counter % 50000 == 0:
        print(str(counter) + "..")
        
# -- end of make ItemList

# search for frequent itemset
frequentItemSet = list(or3.frequent_itemsets(ItemList, 0.02))

print("FREQUENT PATTERN WITH MORE THAN 1 ITEM")
counter = 1
frequentItemSet.sort(key=lambda x: -x[1])
for itemSet in frequentItemSet:
    itemSet_list = list(itemSet[0])
    if len(itemSet_list) > 1:
        print ("[" + str(counter) + "]")
        for item in itemSet_list:
            print(dictItemToDescription[dictKeyToItem[item]])
        print("Minimal Support = " + str(itemSet[1]))
        counter += 1
        if counter > 15:
            break
            


# search for association Rule
associationRuleItemList = or3.association_rules(dict(or3.frequent_itemsets(ItemList, 0.02)), 
                                                0.001)
rules = list(associationRuleItemList)
rules.sort(key=lambda x: -x[3])

print("10 ASSOCIATION RULE WITH GREATER SUPPORT")
counter = 1

for rule in rules:
    rule_list = list(rule)
    print ("[" + str(counter) + "]")
    print (str(dictItemToDescription[dictKeyToItem[list(rule[0])[0]]]) + " => " + str(dictItemToDescription[dictKeyToItem[list(rule[1])[0]]]))
    print("Minimal Support = " + str(rule[2]))
    print("Confidence      = " + str(rule[3]))
    counter += 1
    if counter > 10:
        break
            
