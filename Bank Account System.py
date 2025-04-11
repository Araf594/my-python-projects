#  Bank Account System
from datetime import date


class Loan:
    """Handles loan processing, repayment, and interest tracking."""
    max_loan_limit = 5000  # Prevents excessive loans
    interest_rate = 0.05

    def __init__(self, account, amount):
        self.account = account  # object account referred
        self.remaining_loan_due = amount + (1 + Loan.interest_rate)  # Applying initial interest of 5%
        self.payment_history = []

        account.balance += amount  # Granting user the loan to their main balance if eligible when loan object created.

    def __repr__(self):
        return f'{self.account}'

    def pay_installment(self, amount):
        """Process repayment and apply interest after each installment."""
        if amount <= 0:
            print("Invalid installment amount! Must be greater than zero.")
            return

        self.remaining_loan_due -= amount  # Deduct payment first
        self.payment_history.append(amount)

        # Check if loan is fully repaid
        if self.remaining_loan_due <= 0:
            self.remaining_loan_due = 0
            print("🎉 Loan fully paid!")
            print(f'Remaining Loan Due: {self.remaining_loan_due}')
            self.account.active_loan = None  # Can start a new loan as current loan has been paid in full
        else:
            self.remaining_loan_due *= (1 + Loan.interest_rate)  # Apply interest AFTER payment
            print(f'Remaining Loan Due: {self.remaining_loan_due:.2f} (Interest Applied)')  # 2 decimal places.

    def get_loan_summary(self):
        """Loan Summary"""
        print(f'Remaining Loan Due: ${self.remaining_loan_due:.2f} "Loan Payment history: {self.payment_history}')


class GeneralAccount:
    """Creates a General Account"""
    __last_account_number = 1000  # Private class variable to store the last assigned account number
    __max_daily_limit = 2000
    __withdrawal_today = {}  # format E.g {date : 24-03-2025, user1: '2000', user2: '200'}

    @classmethod
    def get_max_daily_withdrawal_limit(cls):
        """Getter for daily maximum withdrawal limit if user wants to check it"""
        return cls.__max_daily_limit

    @classmethod
    def get_withdrawals_of_today(cls):
        """Provides read-only access to withdrawal data history of users of a specific day"""
        return cls.__withdrawal_today.copy()  # Returns a copy of dictionary to prevent modification

    @classmethod
    def check_daily_limit(cls, amount, account_number):
        """Checks if a user exceeds the daily maximum withdrawal limit"""
        date_today = str(date.today())
        if cls.__withdrawal_today.get('date') != date_today:  # get function to avoid program from crashing.
            cls.__withdrawal_today = {'date': date_today}  # The withdrawal data resets on a new day

        withdrawal_so_far = cls.__withdrawal_today.get(account_number, 0)  # $0 if no withdrawal made my user in a day.
        if withdrawal_so_far + amount <= cls.__max_daily_limit:
            cls.__withdrawal_today[account_number] = withdrawal_so_far + amount  # Appends/Update withdrawal amount.
            return True
        else:
            print(f'⚠️Warning! Daily withdrawal limit of ${cls.__max_daily_limit} exceeded.')
            return False

    @classmethod
    def update_withdrawal_limit(cls, new_limit, admin_pass):
        """Allows only the admin to update the withdrawal limit if it's greater than $2000."""
        if admin_pass == 'secure_admin_pass':  # ✅ Admin authentication
            if isinstance(new_limit, (int, float)) and new_limit > 2000:  # ✅ Ensure new limit is valid
                cls.__max_daily_limit = new_limit
                print(f"New withdrawal limit set to ${cls.__max_daily_limit}")
            else:
                print('New value for daily maximum withdrawal limit should be greater than $2000')
        else:
            print("Access Denied (Incorrect Password)! Only the bank admin can update the limit.")

    @classmethod
    def get_account_number(cls):
        """Getter method to access the last account number."""
        account_number = cls.__last_account_number
        cls.__last_account_number += 1
        return account_number

    @classmethod
    def set_account_number(cls, new_value):
        """Setter method to modify the last account number (if needed)."""
        if new_value > cls.__last_account_number:  # To maintain uniqueness, new value should be greater.
            cls.__last_account_number = new_value
        else:
            raise ValueError('Setting a value for the last Account number must be greater than the current value.')

    def freeze_account(self):
        """Allows freezing the account"""
        self.__is_freeze = True
        print('The account is frozen')

    def unfreeze_account(self):
        """Allows unfreezing the account"""
        if self.__is_freeze:
            self.__is_freeze = False
            print('The account is unfrozen')
        else:
            print('The account is already unfrozen!')

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.__account_number = GeneralAccount.get_account_number()
        self.transaction_history = []
        self.__is_freeze = False  # By default, account should be active when created.
        self.active_loan = None  # Initially no active loan when user creates the account

    def apply_for_loan(self, amount):
        """Allow customers to request a loan if they are eligible."""
        if amount > Loan.max_loan_limit:
            print(f'Loan Denied! Your amount of loan request exceeded maximum loan limit: ${Loan.max_loan_limit}')
            return

        if self.active_loan:
            print('You already have 1 active loan, pay the remaining amount for that loan before starting another one.')
            return

        self.active_loan = Loan(self, amount)  # Loan object created (linked) # Composition
        print(f"✅ Loan approved! ${amount} added to your account balance.")

    def repay_loan(self, installment):
        """Make a loan payment if the account has an active loan."""
        if not self.active_loan:
            print('No active loan to repay!')
            return

        self.active_loan.pay_installment(installment)

    def loan_summary(self):
        """Displays Loan Summary if there is an active loan"""
        if not self.active_loan:
            print('You current do not have any active loan!')
        else:
            self.active_loan.get_loan_summary()

    @property
    def is_freeze(self):
        """Read-only property"""
        return self.__is_freeze

    @property
    def account_number(self):  # Can access this method like an attribute due to property decorator
        """getter for account number"""
        return self.__account_number

    def __repr__(self):
        return f'Name: {self.name} Account No: {self.account_number} Balance: {self.balance}, Account_Type: General'

    def deposit_money(self, amount):
        """Deposits money into the account"""
        if self.is_freeze:
            print('Transaction denied! Your account is frozen.')
            return
        if amount > 0:
            self.balance += amount
            current_date = str(date.today())
            transaction = {'Amount': amount, 'Date': current_date, 'Type': 'Deposit'}
            self.transaction_history.append(transaction)
            print(f'${amount} has been successfully deposited in your account')
        else:
            print('Transaction not possible! The amount of deposit must be more than $0')

    def check_amount(self, amount):
        """Helper method to check if withdrawal is possible"""
        if amount > self.balance:
            return False
        return True

    def verify_user(self):
        """Helper method to verify the user (Needed for all types of account)"""
        try:
            account_num = int(input(f'Please enter the account number of {self.name}: '))
            if account_num == self.account_number:
                return True
            else:
                print('Account Number does not match! You have to enter the correct account number to proceed.')
                return False
        except ValueError:
            print("❌ Invalid input. Please enter a valid account number.")

    def validate_withdraw(self, amount):
        """Helper method to confirm withdraw (Needed for all types of account)"""
        while True:
            authenticate = input(f'Do you wish to proceed and and withdraw from this account? ("Yes"/"No"): ').strip()
            if authenticate.lower() == 'yes':
                self.balance -= amount
                current_date = str(date.today())
                self.transaction_history.append({'Amount': amount, 'Date': current_date, 'Type': 'Withdrawal'})
                print(f'Transaction Successful! Current Balance: {self.balance}')
                return True
            elif authenticate.lower() == 'no':
                print('Transaction cancelled!')
                return False
            else:
                print('Invalid Response. Answer either "Yes" or "No"')

    def withdraw_money(self, amount):
        """Generic withdrawal method (can be overridden)"""
        if self.is_freeze:
            print('Transaction denied! Your account is frozen.')
            return

        if GeneralAccount.check_daily_limit(amount, self.account_number):
            if self.check_amount(amount):
                if self.verify_user():
                    self.validate_withdraw(amount)
                    return
            else:
                print('You do not have sufficient funds in your account balance for this withdrawal.')
                return

    def check_balance(self):
        """Displays the current balance"""
        print(f'Your current account balance is: {self.balance}')

    def view_transaction_history(self):
        """Displays the transaction history"""
        if not self.transaction_history:
            print('This user did not make any transaction yet!')
        else:
            print('----------TRANSACTION HISTORY-------------')
            for index, item in enumerate(self.transaction_history, start=1):
                print(f'{index}. Amount: {item["Amount"]}, Date: {item["Date"]}, Type: {item["Type"]}')


class SavingAccount(GeneralAccount):
    """Creates a Savings Account"""
    months_since_last_interest = 0
    withdrawal = 0  # User will be allowed to withdraw 6 times per month
    last_interest_applied_month = 0
    min_balance = 25
    interest = 1.01

    def __init__(self, name, balance):
        if balance < SavingAccount.min_balance:
            raise ValueError(f"Initial balance must be at least ${SavingAccount.min_balance}.")
        else:
            super().__init__(name, balance)

    def __repr__(self):
        return f'Name: {self.name} Account No: {self.account_number} Balance: {self.balance} Account_Type: Savings'

    def apply_interest(self):
        """Applies a monthly interest"""
        current_month = date.today().month
        if current_month != SavingAccount.months_since_last_interest:
            self.balance = self.balance * self.interest
            SavingAccount.months_since_last_interest = current_month

    def withdraw_money(self, amount):
        """Overridden, this method functions differently than other withdraw methods"""
        if self.is_freeze:
            print('Transaction denied! Your account is frozen.')
            return
        if not SavingAccount.check_daily_limit(amount, self.account_number):
            return  # exceeded daily withdrawal limit
        balance_after_withdrawal = self.balance - amount
        if balance_after_withdrawal < self.min_balance:
            print(f'Transaction Denied!')
            print(f'After this transaction, your account balance will be lower than the minimum balance needed')
            print(f'Balance (After withdrawal): ${balance_after_withdrawal}')
            print(f'Minimum balance needed to keep the account active: ${self.min_balance}')
            return
        current_month = date.today().month
        if SavingAccount.last_interest_applied_month != current_month:
            SavingAccount.last_interest_applied_month += 1
            SavingAccount.withdrawal = 0
        if SavingAccount.last_interest_applied_month == current_month and SavingAccount.withdrawal == 6:
            print('Transaction Denied! You can not withdraw money more than 6 times in a month!')
            return
        if self.check_amount(amount):
            if self.verify_user():
                if self.validate_withdraw(amount):
                    SavingAccount.withdrawal += 1
                    return
            else:
                print('Account Number does not match! Please enter the correct account number in order to proceed')
                return
        else:
            print('You do not have sufficient funds in your account balance for this withdrawal.')
            return


class CheckingAccount(GeneralAccount):
    """Creates a Checking Account"""

    def __init__(self, name, balance):
        if balance <= -3000:
            raise ValueError("The initial balance should be more than the overdraft limit which is (-)$3,000")
        else:
            super().__init__(name, balance)

    def __repr__(self):
        return f'Name: {self.name} Account No: {self.account_number} Balance: {self.balance} Account_Type: Checking'

    def withdraw_money(self, amount):  # Overdraft Protection
        """Overridden, this method functions differently than other withdraw methods"""
        charge_fee = 50  # Charges $50 if user wants to withdraw and if their balance is negative or will be negative.
        limit = -3000  # Overdraft Limit
        # Case 1 - No fee charged if balance after withdrawal is positive (more than $0)
        # Case 2 - Fee charged if : Balance after withdrawal is negative (below $0)
        # Whatever the user withdraws must never exceed the withdrawal limit which is $3,000
        # Before transaction, verify account number and double check whether they actually want to withdraw.

        if self.is_freeze:
            print('Transaction denied! Your account is frozen.')
            return

        if not CheckingAccount.check_daily_limit(amount, self.account_number):
            return  # exceeded daily withdrawal limit

        # Case when balance is negative after withdrawal (Fee will be charged)
        balance_after_withdrawal = self.balance - amount
        if balance_after_withdrawal < 0:
            balance_after_charge = balance_after_withdrawal - charge_fee
            if balance_after_charge < limit:
                print('Transaction Denied! You will exceed the overdraft limit ($3,000) after this transaction')
                print('For overdrawing an additional fee of $50 is charged as well')
                print(f'Your balance after this transaction would be ${balance_after_charge}')
                print('Exceeds overdraft limit of $3,000')
                return
            else:
                print(f'Current balance: ${self.balance} and after withdrawal: ${balance_after_charge}')
                print('For the negative balance, you have to pay an additional fee charge of $50 with this withdrawal')
                print(f'Withdraw amount: ${amount} and Charge for negative balance: $50')
                if self.verify_user():
                    self.validate_withdraw(amount + charge_fee)
                    return

        # Case when balance is positive after withdrawal (No Fee will be charged)
        if balance_after_withdrawal > 0:
            if self.verify_user():
                self.validate_withdraw(amount)
            else:
                print('Account Number does not match! You need to enter the correct account number in order to proceed')
                return


























