#
# Jason H. Wells - wellsjason543@gmail.com
# v4 - 03/30/2025
# 
# "Dues Tracker" is the first 3 columns of Dues Tracker google sheet copied and pasted into a .txt
# "Cashnet Record" is a pdf obtained from SLICE and all text copied into a .txt
#
# After parsing Cashnet Record - if extra words are appended to people's names, or dues appearing in non dues payments,
# add those words to Tokens.tokens
#

import string
import copy
from os.path import isfile
from cmu_cpcs_utils import prettyPrint

class Tokens:
    tokens = ['symphony','chamber','orchestra','member','due','annual','flute','auo']

class Person:
    def __init__(self, name: str, 
                       paymentMethod: str, # 'cashnet', 'cashnet(record only)', 'cashnet(duplicate)', 'cash', 'NONE'
                       cashnetReceiptNumber: str,
                       cashnetConfirmation: tuple[str, str] | None): # (date, amount)
        
        self.name = name
        self.paymentMethod = paymentMethod
        self.cashnetReceiptNumber = cashnetReceiptNumber
        self.cashnetConfirmation = cashnetConfirmation

    def personToList(self):
        return [self.name, self.paymentMethod, self.cashnetReceiptNumber, self.cashnetConfirmation]
    
    def __str__(self):
        return f'{self.name}, {self.paymentMethod}, {self.cashnetReceiptNumber}, {self.cashnetConfirmation}'
    
    def __repr__(self):
        return self.__str__()

    def __hash__(self): # unused
        return hash(self.__str__())

def getDuesTrackerLines():
    while True:
        duesTrackerFilename = input('Dues Tracker: ')
        if not duesTrackerFilename.endswith('.txt'): duesTrackerFilename += '.txt'
        if isfile(duesTrackerFilename):
            print()
            with open(duesTrackerFilename) as file:
                return file.readlines()
        else:
            print('Invalid file name\n')

def getCashnetRecordLines():
    while True:
        cashnetRecordFilename = input('Cashnet Record: ')
        if not cashnetRecordFilename.endswith('.txt'): cashnetRecordFilename += '.txt'
        if isfile(cashnetRecordFilename):
            print()
            with open(cashnetRecordFilename) as file:
                return file.readlines()
        else:
            print('Invalid file name\n') 

# mutates people, returns None
def processDuesTracker(people: list[Person], duesTrackerLines: list[str]):
    doubleContinue = False
    for line in duesTrackerLines:
        # no checkbox means un-useful line or person dropped
        if 'FALSE' not in line and 'TRUE' not in line: 
            continue
        
        boolStartIndex = max(line.find('TRUE'), line.find('FALSE'))
        
        # name
        name = line[:boolStartIndex-1]
        
        # payment method
        lineWithoutName = line[boolStartIndex:]
        receiptNumberStartIndex = lineWithoutName.index('\t')+1
        receiptNumber = lineWithoutName[receiptNumberStartIndex:-1]
        
        if line[boolStartIndex] == 'T':
            if receiptNumber == '':
                paymentMethod = 'cash'
            else: paymentMethod = 'cashnet'
        else: paymentMethod = 'NONE'

        people.append(Person(name, paymentMethod, receiptNumber, None))

# get index of the last char of a name by finding the word that comes after it
# return None if no index found
def getLineNameEnd(line: str, tokens: list):
    lowestIndex = None
    for token in tokens:
        tokenIndex = line.lower().find(token)
        if tokenIndex != -1 and (lowestIndex is None or (tokenIndex < lowestIndex)):
            lowestIndex = tokenIndex
    if lowestIndex is None: 
        return None
    return lowestIndex-2

# returns (people, list of non-dues payments)
def processCashnetRecord(people: list[Person], cashnetRecordLines: list[str]):
    newPeople = copy.copy(people)

    dataLines = []
    highestYear = 0
    for line in cashnetRecordLines:
        try: LineHasTransaction = line[2] == '/' # look for date stamp
        except IndexError: continue
        
        if LineHasTransaction:
            year = int(line.split('/')[2][:4])
            if highestYear < year: highestYear = year
            dataLines.append(line)
    
    # remove transactions not from the highest year (don't include fall semester transactions during spring semester)
    lineNumber = len(dataLines)-1
    while 0 <= lineNumber:
        if int(dataLines[lineNumber].split('/')[2][:4]) != highestYear:
            del dataLines[lineNumber]
        lineNumber -= 1


    nonDuesPayments: list = []

    for line in dataLines:
        nameEndIndex = getLineNameEnd(line, Tokens.tokens)
        if nameEndIndex is None:
            nonDuesPayments.append(line[:-1]) # omit new line char
            continue

        # name
        name = line[11:nameEndIndex+1] # date stamp is 11 chars long
    
        # date
        date = line[:11]

        # amount
        amountStartIndex = max(line.find('.com'), line.find('edu'))+4
        amount = line[amountStartIndex:].strip()
    
        index = -1
        found = False
        for person in people: # linear search through old people to find name match
            index += 1
            if person.name.lower() == name.lower(): # name match -> update Person object
                if people[index].cashnetConfirmation is None:
                    newPeople[index].cashnetConfirmation = (date, amount)
                    if people[index].paymentMethod == 'NONE':
                        newPeople[index].paymentMethod = 'cashnet(record only)'
                else: # duplicate cashnet confirmation
                    newPeople.append(Person(name, 'cashnet(duplicate)', '', (date, amount)))
                found = True
                break
        if not found: # searched all old people and no match -> create new Person
            newPeople.append(Person(name, 'cashnet(record only)', '', (date, amount)))

    return newPeople, nonDuesPayments

# run in place
def insertIndexesTo2dList(L: list[list]):
    for rowIndex in range(len(L)):
        L[rowIndex].insert(0,rowIndex)

def printPeople(people: list[Person]):
    peopleList = [person.personToList() for person in people] 
    peopleList.sort()
    peopleList.insert(0,['Name','Payment Method','Cashnet Receipt No.','Cashnet Confirmation'])
    
    insertIndexesTo2dList(peopleList)
    prettyPrint(peopleList)

def printPeopleWithPaymentMethod(people: list[Person], paymentMethod: str):
    peopleList = [person.personToList() for person in people if person.paymentMethod == paymentMethod]
    peopleList.sort()
    peopleList.insert(0,['Name','Payment Method','Cashnet Receipt No.','Cashnet Confirmation'])
    
    insertIndexesTo2dList(peopleList)

    print(f'---Payment Method: {paymentMethod}---')
    prettyPrint(peopleList)

def main():
    people: list[Person] = []
    print()

    # dues tracker
    duesTrackerLines = getDuesTrackerLines()
    processDuesTracker(people, duesTrackerLines)
    
    print('---dues tracker data---')
    printPeople(people)
    
    printPeopleWithPaymentMethod(people, 'NONE')

    # cashnet record
    cashnetRecordLines = getCashnetRecordLines()
    people, nonDuesPayments = processCashnetRecord(people, cashnetRecordLines)
    
    print('---data merged w/ cashnet record ---')
    printPeople(people)

    printPeopleWithPaymentMethod(people, 'cashnet(duplicate)')
    printPeopleWithPaymentMethod(people, 'cashnet(record only)')
    printPeopleWithPaymentMethod(people, 'NONE')
    

    print('---non dues payments---')
    for item in nonDuesPayments:
        print(item)
    
    print()

if __name__ == '__main__':
    main()