# This file includes sample of Bank, Account, Card class for test.
from typing import Sequence
from random import randint
from collections import defaultdict
from datetime import datetime

#Card class
class Card:
    def __init__(self, userName: Sequence, cardNumber: int, password: int, accountNumber: int):
        self.cardNumber = cardNumber
        self.userName = userName
        self.password = password
        self.accountList = [accountNumber]

#Bank Class
class Bank:
    
    #Account class
    class Account:
        def __init__(self, userName: Sequence, accountNumber: int, password:Sequence, card=None):
            self.userName = userName
            self.accountNumber = accountNumber
            self.balance = 0
            self.password = password
            if card:
                card.accountList.append(accountNumber)

    #Bank initialize
    def __init__(self):
        # self.ATMList = defaultdict(bool)
        self.history = []
        self.key = 'ATMcontroller'
        self.cardCount = 0
        self.accountCount = 0
        self.accountList = defaultdict(bool)
        self.cardList = defaultdict(bool)

    # Create New Card
    def createCard(self, userName: int, password: Sequence, accountNumber: int):
        cardNumber = 100000 + self.cardCount
        self.cardCount += 1
        
        #validate transferAccountNumber
        checkAccountResult, result = self.checkAccountNumber(accountNumber)
        if checkAccountResult == False:
            return False, result

        self.cardList[cardNumber] = Card(userName, cardNumber, password, accountNumber)
        # print(f'Card Create Success.\nYour Card Number is {cardNumber}.')
        return True, self.cardList[cardNumber]

    # Decrypt password received from ATM
    def decryptPassword(self, encryptedPassword: Sequence):
        # Decrypt encryptedPassword using self.key
        return encryptedPassword

    # Check if password received from ATM is valid
    def checkPassword(self, ATMNumber:int, cardNumber:int, encryptedPassword:Sequence):
        password = self.decryptPassword(encryptedPassword)

        if self.cardList[cardNumber]: #ATMNumber in self.ATMList 
            myCard = self.cardList[cardNumber]
            if myCard.password == password:
                return True, myCard.accountList
            else:
                return False, "Error : Wrong Password"
        else:
            return False, "Error : Invalid Card"


    # Return account's balance
    def getBalance(self, accountNumber:int):
        return self.accountList[accountNumber].balance
    
    # Check if balance of the accountNumber is bigger or equal than required amount
    def checkBalance(self, accountNumber:int, amount:int):
        balance = self.getBalance(accountNumber)
        if balance >= amount:
            return True, balance 
        else:
            return False, "Error : Not enough balance"

    # Create New Account
    def createAccount(self, userName: Sequence, password:Sequence):
        accountNumber = 10000000 + self.accountCount
        self.accountCount += 1
        self.accountList[accountNumber] = self.Account(userName, accountNumber, password)
        # print(f'Account Create Success.\nYour Account Number is {accountNumber}.')

        return True, accountNumber
    
    # Return account
    def getAccountInfo(self, accountNumber:int):
        return self.accountList[accountNumber]

    # Validate accountNumber
    def checkAccountNumber(self, accountNumber):
        account = self.accountList[accountNumber]
        if self.accountList[accountNumber]:
            return True, account.userName
        else:
            return False, "Error : Invalid account number"

    # Deposit Money : add "amount" ofs money to account's balance
    def deposit(self, accountNumber:int, amount:int):
        self.accountList[accountNumber].balance += amount
        return True, self.getAccountInfo(accountNumber)

    # Withdraw Money : subtract "amount" of money to account's balance
    def withdraw(self, accountNumber:int, amount:int):
        enoughMoney, result = self.checkBalance(accountNumber, amount)
        if enoughMoney:
            self.accountList[accountNumber].balance -= amount
            return True, self.getAccountInfo(accountNumber)
        else:
            return False, result

    # Transfer "amount" of money from accountNumber to transferAccountNumber
    def transfer(self, accountNumber:int, transferAccountNumber:int, amount:int):
        
        # Validate transferAccountNumber
        checkAccountSuccess, result = self.checkAccountNumber(accountNumber)
        if checkAccountSuccess == False:
            return False, result

        # Withdraw money from sender's account
        withdrawSuccess, result = self.withdraw(accountNumber, amount)
        if withdrawSuccess == False:
            return False, result

        # Deposit money to transferAccountNumber
        _, _ = self.deposit(transferAccountNumber, amount)
    
        return True, result
            
    # Update account according to the request from ATM
    # [seeBalance, deposit, withdraw, transfer]
    def atmRequest(self, ATMnumber:int, requestType:Sequence, accountNumber:int, transferAccountNumber:int=None, amount:int=None):
        
        requestSuccess, result = '', ''
        if requestType == 'seeBalance':
            requestSuccess, result = True, self.getAccountInfo(accountNumber)
        elif requestType == 'deposit':
            requestSuccess, result = self.deposit(accountNumber, amount)
            self.history.append([datetime.now(), 'deposit', accountNumber, amount, self.getBalance(accountNumber)])
        elif requestType == 'withdraw':
            requestSuccess, result = self.withdraw(accountNumber, amount)
            self.history.append([datetime.now(), 'withdraw', accountNumber, amount, self.getBalance(accountNumber)])
        #Transfer
        else: 
            requestSuccess, result = self.transfer(accountNumber, transferAccountNumber, amount)
            self.history.append([datetime.now(), 'transfer', accountNumber, transferAccountNumber, amount, self.getBalance(accountNumber)])
        return requestSuccess, result