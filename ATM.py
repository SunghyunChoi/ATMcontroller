from random import randint
from time import time
from collections import defaultdict
from typing import Any, Sequence

class Bank:

    #Account class
    class Account:
        def __init__(self, userName: Sequence, accountNumber: int, card=None):
            self.userName = userName
            self.accountNumber = accountNumber
            self.balance = 0
            if card:
                card.accountList.append(accountNumber)

    #Card class
    class Card:
        def __init__(self, userName: Sequence, cardNumber: int, password: int, accountNumber: int):
            self.cardNumber = cardNumber
            self.userName = userName
            self.password = password
            self.accountList = [accountNumber]

    #Bank initialize
    def __init__(self):
        # self.ATMList = defaultdict(bool)
        self.history = []
        self.key = 'ATMcontroller'
        self.accountList = defaultdict(bool)
        self.cardList = defaultdict(bool)

    #Register ATM
    # def registerATM(self, ATMNumber: int, key: Sequence):
    #     if key == self.key:
    #         self.ATMList[ATMNumber] = True
    #         return True
    #     else:
    #         return False

    def decryptPassword(self, encryptedPassword: Sequence):
        #self.key를 사용하여 decrypt한다.
        return encryptedPassword

    def createCard(self, userName: int, password: Sequence, accountNumber: int):
        cardNumber = randint(100000, 999999)
        if self.checkAccount(accountNumber):
            self.cardList[cardNumber] = self.Card(userName, cardNumber, password, accountNumber)
        else:
            return False, "Wrong Account Number"
        return cardNumber

    def createAccount(self, userName: Sequence):
        accountNumber = randint(10000000, 99999999)
        self.accountList[accountNumber] = self.Account(userName, accountNumber)

        return accountNumber

    def checkPassword(self, ATMNumber:int, cardNumber:int, encryptedPassword:Sequence):
        password = self.decryptPassword(encryptedPassword)

        if self.cardList[cardNumber]: #ATMNumber in self.ATMList 
            myCard = self.cardList[cardNumber]
            if myCard.password == password:
                return True, self.myCard.accountList
            else:
                return False, "Wrong Password"
        else:
            return False, "Invalid Card"

    def updateAccount(self, ATMnumber:int, requestType:Sequence, accountNumber:int, transferAccountNumber:int=None, amount:int=None):
        
        if requestType == 'seeBalance':
            balance = self.getBalance(accountNumber)
            return True, balance
        elif requestType == 'deposit':
            self.accountList[accountNumber].balance += amount
            balance = self.getBalance(accountNumber)
            return True, balance
        elif requestType == 'withdraw':
            if self.checkBalance(accountNumber, amount):
                self.accountList[accountNumber].balance -= amount
                balance = self.getBalance(accountNumber)
                return balance
            else:
                return False, "Not enough balance, Please check again."
        else: #Transfer
            if self.checkBalance(accountNumber, amount):
                if self.checkAccount(accountNumber):
                    self.transfer(accountNumber, transferAccountNumber, amount)
                    return True 
                else:
                    return False, "Invalid account number for transfer. Please check again"
            else:
                return False, "Not enough balance, Please check again."

    # Check if balance of the accountNumber is bigger or equal than required amount
    def checkBalance(self, accountNumber:int, amount:int):
        if self.getBalance() >= amount:
            return True
        else:
            return False

    def getBalance(self, accountNumber:int):
        return self.accountList[accountNumber].balance

    def deposit(self, accountNumber:int, amount:int):
        self.accountList[accountNumber].balance += amount
        return self.getBalance(accountNumber)

    def checkAccount(self, ATMNumber:int, accountNumber):
        if self.accountList[accountNumber]:
            return True
        else:
            return False

    def transfer(self, bankName:Sequence, accountNumber:int, transferAccountNumber:int, amount:int):
        return True
            
class ATM:
    class Display:
        def __init__(self):
            pass
        def displayImage(self, imageNumber:int, timeOut:int=None, text:int=None, textInput:Sequence=None):
            #Display Image Number == imageNumber
            #Wait For Timeout
            #get Input : testInput
            pass
        
    class CashBin:
        pass

    class CardReader:
        pass


bank = Bank()
accountNumber = bank.Account("sunghyunChoi")
print(accountNumber)