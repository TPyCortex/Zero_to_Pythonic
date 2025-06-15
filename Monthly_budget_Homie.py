# 💬 Ask for user's name and greet them
name = input("Hi! What is your name: ")
print("Hi " + name + " nice to meet you!")

# 🎯 Ask the user's savings goal
question1 = input ("Your monthly savings goal (£):")
print ('Cool! So your monthly savings goal is £'+ question1 + '. We can do it!')

# 💰 Ask for annual salary and calculate monthly salary
Salary= float(input("What is your annual salary (£): "))
Monthly_Salary = Salary / 12
# 🧾 Determine tax rate based on UK income tax brackets
if Salary <= 12570:
    tax_rate = 0.0
elif Salary <= 50270:
    tax_rate = 0.20
elif Salary <= 125140:
    tax_rate = 0.40
else:
    tax_rate = 0.45

# 🧮 Calculate monthly tax and after-tax monthly income
Total_Tax = Salary * tax_rate
Monthly_Tax = Total_Tax / 12
After_tax = Monthly_Salary - Monthly_Tax
print("Great! So your monthly income after tax is £" + str(round(After_tax,2)))

# 💸 Ask if the user has loan repayment — conditional input
loan = input("Do you have any monthly loan payment? (Yes or No):")
if loan == "Yes":
    Loan_Amount = float(input("What is your monthly loan repayment amount (£): "))
else:
    Loan_Amount = 0.0
# 🏠 Ask for regular expenses
rent = float(input("Enter your rent (£): "))
bills = float(input("Enter your bills (£): "))
fun = float(input("Enter your other/entertainment/fun expenses (£): "))

# 🧾 Sum total monthly expenses (loan + rent + bills + fun)
total_expenses = float( Loan_Amount+ rent + bills + fun)
# 💰 Calculate remaining income after all expenses
result = After_tax - total_expenses

# 📊 Show user's savings for the month
print("Your monthly savings is £" +str(round(result,2)))

# ✅ Compare savings to the user's goal and give feedback
if result < float(question1):
    print("Sorry, you don't have enough money! LMAO.. Try to eat out less and eat more homecooked food.")
else:
    print("You are doing great! Keep it up!")



