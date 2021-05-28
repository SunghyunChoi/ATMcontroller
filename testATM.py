import ATMController
from Bank import Bank, Card
class User:
    def __init__(self, name, card=None):
        self.name = name
        self.card = card

def testInsertCard(ATM, card):
    ATM.displayOutput("testInsertCard")
    ATM.insertCard(card)
    if ATM.readCard() == card.cardNumber:
        return True
    else:
        return False

#For simplicity, only one account is made for each card.
def testSeeBalance(ATM, card, password):
    ATM.displayOutput("testseeBalance")
    ATM.insertCard(card)
    validResult, accountList = ATM.validatePassword(password)
    ATM.selectAccount(accountList[0])
    requestSuccess, result = ATM.seeBalance()
    ATM.displayOutput(result)
    
    if requestSuccess:
        ATM.displayOutput("Success")
    else:
        ATM.displayOutput("Fail")
    
    return requestSuccess, result

def testDeposit(ATM, card, password, amount):
    ATM.displayOutput(f"testDeposit : $ {amount}")
    ATM.insertCard(card)
    validResult, accountList = ATM.validatePassword(password)
    ATM.selectAccount(accountList[0])
    requestSuccess, result = ATM.deposit(amount)
    ATM.displayOutput(result)


    if requestSuccess:
        ATM.displayOutput("Success")
    else:
        ATM.displayOutput("Fail")
        
    return requestSuccess, result

def testWithdraw(ATM, card, password, amount):
    ATM.displayOutput(f"testWithdraw : ${amount}")
    ATM.insertCard(card)
    validResult, accountList = ATM.validatePassword(password)
    ATM.selectAccount(accountList[0])
    requestSuccess, result = ATM.withdraw(amount)

    ATM.displayOutput(result)
    if requestSuccess:
        ATM.displayOutput("Success")
    else:
        ATM.displayOutput("Fail")

    return requestSuccess, result

def testTransfer(ATM, senderCard, senderPassword, receiverAccountNumber, amount, receiverCard, receiverPassword):
    ATM.displayOutput("testTransfer")
    #Check Receiver's initial balance
    ATM.insertCard(receiverCard)
    validResult, accountList = ATM.validatePassword(senderPassword)
    ATM.selectAccount(accountList[0])
    _, receiverOldAccount = ATM.seeBalance()
    ATM.returnCard()

    #Check Sender's initial balance
    ATM.insertCard(senderCard)
    validResult, accountList = ATM.validatePassword(senderPassword)
    ATM.selectAccount(accountList[0])
    _, senderOldAccount = ATM.seeBalance()
    
    ATM.displayOutput(senderOldAccount)
    ATM.displayOutput(receiverOldAccount)
    ATM.displayOutput(f"Transfer $ {amount}")
    
    #Transfer
    requestSuccess, result = ATM.transfer(receiverAccountNumber, amount)
    _, senderNewAccount = ATM.seeBalance()
    ATM.returnCard()

    #Check Receiver's balance after transfer
    ATM.insertCard(receiverCard)
    validResult, accountList = ATM.validatePassword(senderPassword)
    ATM.selectAccount(accountList[0])
    _, receiverNewAccount = ATM.seeBalance()
    ATM.returnCard()
    
    ATM.displayOutput(senderNewAccount)
    ATM.displayOutput(receiverNewAccount)

    
    if senderOldAccount.balance - senderNewAccount.balance == receiverNewAccount.balance - receiverOldAccount.balance:
        ATM.displayOutput("Success")
        return True
    else:
        ATM.displayOutput("Fail")
        return False

def testExit(ATM):
    return ATM.returnCard()

if __name__=='__main__':
    bearBank = Bank()
    bearATM = ATMController.ATM(bearBank)

    # Create User1 : Penny
    # Account Number : 10000000
    # Card number : 100000
    user1 = User("Penny")
    createResult, accountNumber1 = bearBank.createAccount("Penny", "1234")
    createResult, card1 = bearBank.createCard(user1.name, "1234", accountNumber1)
    user1.card = card1

    # Create User2 : Servi
    # Account Number : 10000001
    # Card number : 100001
    user2 = User("Servi")
    createResult, accountNumber2 = bearBank.createAccount("Servi", "1234")
    createResult, card2 = bearBank.createCard(user2.name, "1234", accountNumber2)
    user2.card = card2

    # Test functions
    testDeposit(bearATM, user1.card, '1234', 5000)
    testExit(bearATM)
    testSeeBalance(bearATM, user1.card, '1234')
    testExit(bearATM)
    testWithdraw(bearATM, user1.card, '1234', 2000)
    testExit(bearATM)
    testTransfer(bearATM, user1.card, '1234', 10000001, 3000, user2.card, '1234')
    testExit(bearATM)

    # Start Console : Test is started by inserting card into the ATM
    # Insert Penny's card into the ATM
    print("%%%%%%%Test Console Start%%%%%%%")
    bearATM.run(user1.card)
