# ATMcontroller
This is implementation of an ATM controller.
Simple Display, CashBin, CardReader, Bank module is added to test the ATM Controller.
ATM Controller reads user input from the Display Module's touchscreen and handles user's request by interacting with Bank module.

<p align=center>
<img width="589" alt="ATMController" src="https://user-images.githubusercontent.com/32299611/119831296-1bc68180-bf38-11eb-8a47-34b25b15acb0.png">
</p>  


## How to Clone
To clone the project, run the following in terminal:
```
git clone https://github.com/SunghyunChoi/ATMcontroller.git
```
<br/>

## How to Build
This project is written in Python3.9 and does not require any installation.

<br/>

## How to run Test
You can test by running the file 'testATM.py'
```
python testATM.py
or
python3 testATM.py
```

<br/>

Test will start with dummy user data.
Variable Name | Name | Account Number | Card Number | Password | Balance
--------- | -------- | ------- | ------------ | ----------- | ----------
user1 | Penny | 10000000 | 100000 | bear | 0
user2 | Servi | 10000001 | 100000 | bear | 0
<br/>

You can test the ATM with using either Unit Test Functions or Console.

<br/>

### 1. Using Functions

 You can use the test functions for the basic operations of an ATM.
 Test functions will return (True/False, result) and print it on console.
```
testDeposit(bearATM, user1.card, '1234', 5000)
testExit(bearATM)
testSeeBalance(bearATM, user1.card, '1234')
testExit(bearATM)
testWithdraw(bearATM, user1.card, '1234', 2000)
testExit(bearATM)
testTransfer(bearATM, user1.card, '1234', 10000001, 3000, user2.card, '1234')
testExit(bearATM)
```

```
<<Result For testDeposit>>

***********************************************
testDeposit : $ 5000
***********************************************


***********************************************
Username : Penny
AccountNumber : 10000000
Balance : $ 5000
***********************************************


***********************************************
Success
***********************************************
```


### 2. Using Console
You can run the ATM and test it using console.
If you run 'testATM.py', the last line of the code will start the Console Interaction.
```
bearATM.run(user1.card)
```
Card is automatically inserted by passing Card Object to the function.

```

***********************************************
Please insert your Card
***********************************************

***********************************************
Card Inserted
***********************************************

***********************************************
Please type your Password
***********************************************

1234(Your Input)

***********************************************
Hello Penny!
***********************************************

***********************************************
Please select an account
1. 10000000
***********************************************

1(Your Input)

***********************************************
What would you like to do?
1. See Balance
2. Deposit
3. Withdraw
4. Transfer
5. Exit
***********************************************

2(Your Input)

***********************************************
Input Cash
***********************************************

3000(Your Input)

***********************************************
Username : Penny
AccountNumber : 10000000
Balance : $ 3000
***********************************************

***********************************************
What would you like to do?
1. See Balance
2. Deposit
3. Withdraw
4. Transfer
5. Exit
***********************************************

5(Your Input)

***********************************************
Exit. Please take your card
***********************************************
```
