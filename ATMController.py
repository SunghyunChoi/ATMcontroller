from time import thread_time_ns, time
from typing import Any, Sequence
from Bank import Bank, Card
from random import randint

class ATM:

    # Display Class : Displays image,texts and reads input from touchscreen
    class Display:
        def __init__(self):
            pass
        
        # Read Input from the Touchscreen
        def getInput(self, timeOut:int=None):
            userInput = input()
            return userInput
        
        # Displays received Data(Image Number, Text)
        def displayText(self, outputText:Sequence, imageNumber:int=None):
            print("\n***********************************************")
            if type(outputText)== Bank.Account:
                accountInfo = outputText
                print(f"Username : {accountInfo.userName}")
                print(f"AccountNumber : {accountInfo.accountNumber}")
                print(f"Balance : $ {accountInfo.balance}")
            elif type(outputText)==Card:
                cardInfo = outputText
                print(f"Hello {cardInfo.userName}!")
            else:
                print(outputText)
            print("***********************************************\n")
    
    # CashBin Class : Checks the amount of cash left in cash bin.
    class CashBin:
        # Initialize cash bin with initial cash
        def __init__(self, cash=1000000000):
            self.cash = cash

        # Returns current cash left in cash bin.
        def getCashBin(self):
            return self.cash

        # Check if there is enough cash in the CashBin
        def checkCashBin(self, amount:int):
            if self.getCashBin() < amount:
                return False, "Error : Not enough cash left in ATM. Please use another ATM."
            else:
                return True, self.getCashBin()

        # Put Money into the CashBin
        # Used when a user deposits money
        def inputCashBin(self, amount:int):
            self.cash += amount
            return True, self.getCashBin()
        
        # Get money from the cashbin
        # Used when a user withdraws money
        def outputCashBin(self, amount:int):
            self.cash -= amount
            return True, self.getCashBin()
            
    # CardReader Class, insert/read/return card.
    class CardReader:
        def __init__(self):
            self.card = None
        
        def insert(self, card:Card):
            self.card = card
            return True

        def read(self):
            return self.card.cardNumber

        def returnCard(self):
            self.card = None
            return True

    # ATM initialize
    def __init__(self, bank:Bank):
        self.bank = bank
        self.cardReader = self.CardReader()
        self.cashBin = self.CashBin()
        self.display = self.Display()
        self.key = 'ATMcontroller'
        self.selectAccountNumber = None
        self.ATMNumber = randint(1000, 9999)

    # Send display data to the Display Module
    def displayOutput(self, outputText:Sequence):
        returnInput = self.display.displayText(outputText)
    
    # Read input from the touchscreen
    # For simplicity, Assumes that user behaves as expected.
    # User cannot type in any unexpected characters for every cases.
    # ex)Typing characters.
    def displayInput(self):
        userInput = self.display.getInput()
        return userInput

    # Insert Card
    def insertCard(self, card:Card):
        self.cardReader.insert(card)
        return True

    # Read Card
    def readCard(self):
        cardNumber = self.cardReader.read()
        return cardNumber    
    
    # Return Card
    def returnCard(self):
        self.cardReader.returnCard()
        self.selectedAccountNumber = None
        return True

    # deposit cash to the cash bin
    def inputCash(self, amount):
        self.cashBin.inputCashBin(amount)
        return True
    
    # Check if there's enough cash in the cash bin
    def checkCash(self, amount):
        checkCashResult, result = self.cashBin.checkCashBin(amount)
        return checkCashResult, result

    # Withdraw cash from the cash bin
    def outputCash(self, amount):
        outputCashBinResult, result = self.cashBin.outputCashBin(amount)
        return outputCashBinResult, result

    # Read cash left in the cash bin
    def readCash(self):
        return self.cashBin.getCashBin()

    # Encrypt password
    def encrypt(self, password:Sequence):
        return password

    # Validate input password by sending the password to Bank Module.
    # If success, recieves a list of accounts that matches with the card.
    def validatePassword(self, password:Sequence):
        encryptedPassword = self.encrypt(password)
        validResult, result = self.bank.checkPassword(self.ATMNumber, self.readCard(), encryptedPassword)
        return validResult, result

    # Select account
    def selectAccount(self, accountNumber:int):
        self.selectedAccountNumber = accountNumber
        return True

    # See balance of the selected account
    # Success : (True, Account Information)
    # Fail :  (False, Error Message)
    def seeBalance(self):
        requestSuccess, result = self.bank.atmRequest(self.ATMNumber, 'seeBalance', self.selectedAccountNumber)
        return requestSuccess, result

    # Deposit money to the selected account
    # Success : (True, Account Information after deposit)
    # Fail :  (False, Error Message)
    def deposit(self, amount:int):
        self.inputCash(amount)
        depositSuccess, result = self.bank.atmRequest(self.ATMNumber, 'deposit', self.selectedAccountNumber, amount=amount)
        return depositSuccess, result

    # Deposit money to the selected account
    # Success : (True, Account Information after withdraw)
    # Fail :  (False, Error Message)
    def withdraw(self, amount:int):
        checkCashResult, result = self.checkCash(amount)
        if checkCashResult:
            withdrawSuccess, result = self.bank.atmRequest(self.ATMNumber, 'withdraw', self.selectedAccountNumber, amount=amount)
            return withdrawSuccess, result
        else:
            return checkCashResult, result

    # Transfer money from selected account to transferAccountNumber
    # For simplicity, transferring to another bank is not considered.
    # Success : (True, Account Information after transfer)
    # Fail :  (False, Error Message)
    def transfer(self, transferAccountNumber:int, amount:int):
        transferSuccess, result = self.bank.atmRequest(self.ATMNumber, 'transfer', self.selectedAccountNumber, transferAccountNumber=transferAccountNumber, amount=amount)
        return transferSuccess, result

    # Activate ATM
    # Sample Test Code for Console Debugging
    def run(self, card:Card, testList:Sequence=None):
        
        # Insert Card
        self.displayOutput("Please insert your Card")
        self.insertCard(card)
        self.displayOutput("Card Inserted")
        insertedCardNumber = self.readCard()

        # Input Password
        self.displayOutput("Please type your Password")
        password = self.displayInput()
        passwordMatch, result = self.validatePassword(password)
        passwordFailCount = 0

        # Validate Password
        while passwordMatch == False:
            passwordFailCount += 1
            if passwordFailCount>=3:
                self.displayOutput("Password Failure")
                return False
            self.displayOutput(f"Password Failed, please Try Again(Fail Count : {passwordFailCount}/3)")
            password = self.displayInput()
            passwordMatch, result = self.validatePassword(password)
        self.displayOutput(card)

        # Select Account
        accountList = result
        requestSuccess, result = True, ''
        outputText = "Please select an account"
        for idx, account in enumerate(accountList):
            outputText += f'\n{idx+1}. {account}'
        self.displayOutput(outputText)
        accountIdx = int(self.displayInput())
        if accountIdx > len(accountList):
            requestSuccess = False
            result = "Please select among the given accounts."
        else:
            self.selectAccount(accountList[accountIdx-1])

        # Keeps running until a request fails or user selects "5. Exit"
        while requestSuccess:
    
            # Receive User Input
            self.displayOutput("What would you like to do?\n1. See Balance\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Exit")
            userInput = self.displayInput()
            
            if userInput == '1':
                #See Balance
                requestSuccess, result = self.seeBalance()
            elif userInput == '2':
                #Deposit
                self.displayOutput("Input Cash")
                amount = int(self.displayInput())
                requestSuccess, result = self.deposit(amount)
            elif userInput == '3':
                #WithDraw
                self.displayOutput("How much would you like to withdraw?")
                amount = int(self.displayInput())
                requestSuccess, result = self.withdraw(amount)
            elif userInput == '4':
                #Transfer
                self.displayOutput("Input accountNumber to transfer")
                transferAccountNumber = int(self.displayInput())
                self.displayOutput("Input Cash")
                amount = int(self.displayInput())
                requestSuccess, result = self.transfer(transferAccountNumber, amount)
            else:
                #Exit
                self.displayOutput("Exit. Please take your card")
                self.returnCard()
                return

            self.displayOutput(result)
            if requestSuccess == False:
                self.displayOutput("Failed to complete task. Please take your card.")
                self.returnCard()