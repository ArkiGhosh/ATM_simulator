from os import close, name
from constants import CREATE_ACCOUNT, DEPOSIT_MONEY, DISPLAY_BALANCE, EXIT, SEND_MONEY, WITHDRAW_MONEY
import csv
import random


#All the information related to a particular user stored in a csv file
#as the bank's database


def welcome_screen():
    print("Welcome to BestBank")
    print("*" * 50)
    print()
    print("Press the keys to perform the following operations: ")
    print("Press 1 to send money") # use constants for output string
    print("Press 2 to create a new account")
    print("Press 3 to display your balance")
    print("Press 4 to deposit money")
    print("Press 5 to withdraw money")
    print("Press 6 to exit")

def func():
    print("Please enter your choice: ", end = "")
    choice = int(input())

    if (choice == SEND_MONEY):
        send_money()
        print("*" * 50)

    elif (choice == CREATE_ACCOUNT):
        create_account()
        print("*" * 50)

    elif (choice == DISPLAY_BALANCE):
        acc_pin = general()
        disp_obj = Account(account_number = acc_pin[0], pin = acc_pin[1])
        disp_obj.display()
        print("*" * 50)
        
    elif (choice == DEPOSIT_MONEY):
        acc_pin = general()
        dep_obj = Account(account_number = acc_pin[0], pin = acc_pin[1])
        if (dep_obj.deposit_money()):
            print("Amount depositted successfully!")
            print()
        print("*" * 50)
        pass

    elif (choice == WITHDRAW_MONEY):
        acc_pin = general()
        with_obj = Account(account_number = acc_pin[0], pin = acc_pin[1])
        if (with_obj.withdraw_money()):
            print("Amount withdrawn successfully!")
            print()
        print("*" * 50)
        pass

    elif (choice == EXIT):
        print("Thank you for choosing BestBank")
        print("Have a good day")
        print("*" * 50)
        exit()



#ALL MAIN FUNCTIONS
def send_money():
    print()
    print("*" * 50)
    print("Please enter your account number: ", end = "")
    sender = input()

    print("Please enter your pin: ", end = "")
    send_pin = input()
    print()

    send_obj = Account(account_number = sender, pin = send_pin)

    print("Please enter the name of the recipient: ", end = "")
    recip = input()

    print("Please enter recipient's account number: ", end = "")
    r_acc = input()

    print("Please enter IFSC code: ", end = "")
    ifsc = input()

    print("Please enter the branch code: ", end = "")
    branch_cd = input()

    print("Enter the amount to be transferred")
    amt = int(input())

    #checking whether the sender has sufficient balance
    with open('account_info.csv', 'r') as file:
        reader = csv.DictReader(file)
        for i in reader:
            if (i["account_no"] == sender) and (i["pins"] == send_pin):
                if int(i["current_b"]) >= amt:
                    t = int(i["current_b"]) - amt
                    l = [recip, r_acc, ifsc, branch_cd]
                    # passing arguments like this instead of separately introduces chances of invalid number/sequence of arguments
                    #main body for money transfer
                    if (send_obj.transfer_info(l)):
                        print("Please enter the 6 - digit OTP sent to your registered mobile number: ", end = "")
                        t_otp = input()

                        #updating sender's and receiver's balance 
                        r = csv.reader(open('account_info.csv'))
                        lines = list(r)
                        for j in lines:
                            if (j[1] == sender) and (j[2] == send_pin):
                                j[3] = t
                            if (j[1] == r_acc) and (j[0] == recip):
                                j[3] = int(j[3]) + amt
                        
                        # duplicate code, make a function writerows() which handles the open, write and close.
                        tru = open('account_info.csv', 'w', newline = "")
                        writer = csv.writer(tru)
                        writer.writerows(lines)
                        tru.close()

                        if len(t_otp) == 6 and t_otp[0] != '0':

                            print("Money successfully transferred!")
                            print("*" * 50)
                        else:
                            print("wrong OTP, please restart the process")
                            send_money() # don't recurse without a base case

                    #money transfer body ends here
                else:
                    print("Insufficient balance")
    


def create_account():

    print("*" * 50)
    print()
    #name, type_ac, mobile_no, email, nominee
    print("Please enter the name under which this account is to be registered: ", end = "")
    nname = input()

    print("Choose the type of account: SAVINGS(1) or CURRENT(2): ", end = "")
    type_a = "savings" if int(input()) == 1 else "current"

    print("Please enter your mobile number: ", end = "")
    mobile_no = input()

    print("Please enter your email address: ", end = "")
    emailid = input()

    print("Please enter the Nominee name: ", end = "")
    Nomname = input()

    print()
    
    # use named constants for column names, or in this case, use a constant list called HEADINGS
    headings = ['Name:', 'Account Number:', 'PIN:', 'Current balance:', 'IFSC code:', 'Branch Code:', 'Type of account:', 'Mobile number:', 'Email address:', 'Nominee:']
    main_info = Account(name = nname, atype = type_a, mb_num = mobile_no, emailID = emailid, nomin = Nomname)
    main_info_lis = main_info.new_acc_info()
    print(main_info_lis)
    print("Account created successfully, please note the details of your account: ")
    print("-" * 50)
    for i in range(len(headings)):
        print(headings[i], main_info_lis[i], end = " ")
        print()
    print("-" * 50)
    print()
    print("*" * 50)
    
#general template for display, withdraw and deposit
def general(): #doing validation here would have been nice
    print()
    print("*" * 50)
    print("Please enter your account number: ", end = "")
    acc_disp = input()

    print("Please enter your PIN: ", end = " ")
    pin_disp = input()
    return [acc_disp, pin_disp]
#function ends here
    

class Account():
    #name, account_no, pins, current_b, ifsc_codes, branchcode, type, mobile_no, email, nominee
    def __init__(self, name = 0, account_number = 0, pin = 0, ifsc_cd = 0, branch_cd = 0, atype = 0, mb_num = 0, emailID = 0, nomin = 0):
    # would have been better do it line by line
        self.name, self.account_number, self.pin, self.ifsc_cd, self.branch_cd, self.atype, self.mb_num, self.emailID, self.nomin = [name, account_number, pin, ifsc_cd, branch_cd, atype, mb_num, emailID, nomin]


    #Function to store all the information in the csv file
    #The name should make clear the purpose of the function, try to start function names with verbs
    def new_acc_info(self):
        acc_num, pin, ifsc_c, branch_c = [random.randint(10000, 99999), random.randint(1000, 9999), random.randint(1000, 9999), random.randint(1000, 9999)]
        
        with open('account_info.csv', 'a', newline = "") as file:
            write = csv.writer(file)
            write.writerow([self.name, acc_num, pin, 0, ifsc_c, branch_c, self.atype, self.mb_num, self.emailID, self.nomin])
        return [self.name, acc_num, pin, 0, ifsc_c, branch_c, self.atype, self.mb_num, self.emailID, self.nomin]
        #returns a list that contains all the info 
    #function ends here


    #all details of the recipient
    def transfer_info(self, lis):
        recip_name, recip_acc_no, ifsc, branch = lis

        with open('account_info.csv', 'r') as file:
            reader = csv.DictReader(file)
            t = 0
            for i in reader:
                if (i['account_no'] == recip_acc_no) and (i['name'] == recip_name):
                    t = 1
                    temp_ifsc = i['ifsc_codes']
                    temp_branch = i['branchcode']                    

        if t == 1:
            if (temp_ifsc == ifsc) and (temp_branch == branch):
                print("Account found successfully")
                return True
            else:
                print("Details do not match, please try again")
                send_money()
        else:
            print("Account not found, please try again")
            send_money()
    #transfer info ends here

    #display function
    def display(self):
        with open('account_info.csv', 'r') as file:
            reader = csv.DictReader(file)
            t = 0
            for i in reader:
                if (i['account_no'] == self.account_number) and (i["pins"] == self.pin):
                    print("Your current balance is: ", i['current_b'], end = "")
                    print()
                    print("*" * 50)
                    t = 1
        if t == 0:
            print("Sorry, account not found, please check your details and try again.")

    #withdraw function
    def withdraw_money(self):
        print()
        print("Enter the amount you want to withdraw: ", end = "")
        amt = int(input())
        # amount not validated
        
        # duplicate code, better to make an update function which will change amount of account by passed in parameters
        r = csv.reader(open('account_info.csv'))
        lines = list(r)
        t = 0

        for i in lines:
            if (i[1] == self.account_number) and (i[2] == self.pin):
                if int(i[3]) - amt < 0:
                    t = 2
                else:
                    t = 1
                    i[3] = int(i[3]) - amt
    
        rdfile = open('account_info.csv', 'w', newline = "")
        writer = csv.writer(rdfile)
        writer.writerows(lines)
        rdfile.close()

        if t == 0:
            print("Account not found")
        elif t == 2:
            print("Insufficient balance")
        else:
            return True
    
    #deposit function
    def deposit_money(self):
        print()
        print("Enter the amount you want to deposit: ", end = "")
        amt = int(input())

        r = csv.reader(open('account_info.csv'))
        lines = list(r)
        t = 0

        for i in lines:
            if (i[1] == self.account_number) and (i[2] == self.pin):
                i[3] = int(i[3]) + amt
                t = 1

        rdfile = open('account_info.csv', 'w', newline = "")
        writer = csv.writer(rdfile)
        writer.writerows(lines)
        rdfile.close()

        if t == 0:
            print("Account not found")
        else:
            return True

    
                

