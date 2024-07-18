import streamlit as st
import pandas as pd

# Function to calculate compound interest
def calculate_compound_interest(principal, rate, years):
    return principal * ((1 + rate / 100) ** years)

# Function to calculate monthly mortgage payments
def calculate_mortgage(principal, rate, years):
    monthly_rate = rate / 100 / 12
    payments = years * 12
    return principal * monthly_rate / (1 - (1 + monthly_rate) ** -payments)

# Function to calculate retirement savings
def calculate_retirement_savings(initial_amount, monthly_contribution, rate, years):
    total = initial_amount
    for _ in range(years * 12):
        total = total * (1 + rate / 100 / 12) + monthly_contribution
    return total

# Function to calculate daily expenses
def calculate_daily_expenses(expenses, days):
    return sum(expenses) * days

# Streamlit app
def main():
    st.title("Financial Calculator")

    st.sidebar.header("Choose Calculator")
    calculator_type = st.sidebar.selectbox("Select a calculator", ("Compound Interest", "Mortgage", "Retirement Savings", "Daily Expenses"))

    if calculator_type == "Compound Interest":
        st.header("Compound Interest Calculator")
        principal = st.number_input("Principal Amount", min_value=0.0, value=1000.0)
        rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0)
        years = st.number_input("Number of Years", min_value=0, value=10)
        
        if st.button("Calculate"):
            total = calculate_compound_interest(principal, rate, years)
            st.write(f"Total Amount after {years} years: ${total:.2f}")

    elif calculator_type == "Mortgage":
        st.header("Mortgage Calculator")
        principal = st.number_input("Principal Amount", min_value=0.0, value=200000.0)
        rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=3.5)
        years = st.number_input("Mortgage Term (Years)", min_value=0, value=30)
        
        if st.button("Calculate"):
            monthly_payment = calculate_mortgage(principal, rate, years)
            st.write(f"Monthly Mortgage Payment: ${monthly_payment:.2f}")

    elif calculator_type == "Retirement Savings":
        st.header("Retirement Savings Calculator")
        initial_amount = st.number_input("Initial Amount", min_value=0.0, value=10000.0)
        monthly_contribution = st.number_input("Monthly Contribution", min_value=0.0, value=500.0)
        rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0)
        years = st.number_input("Number of Years", min_value=0, value=30)
        
        if st.button("Calculate"):
            total = calculate_retirement_savings(initial_amount, monthly_contribution, rate, years)
            st.write(f"Total Retirement Savings after {years} years: ${total:.2f}")

    elif calculator_type == "Daily Expenses":
        st.header("Daily Expenses Calculator")
        days = st.number_input("Number of Days", min_value=1, value=1)
        expense_items = st.text_area("Enter your daily expenses separated by commas (e.g., 10,20,30)").split(',')
        expenses = [float(expense) for expense in expense_items if expense.strip().isdigit()]

        if st.button("Calculate"):
            total_expenses = calculate_daily_expenses(expenses, days)
            st.write(f"Total Expenses over {days} days: ${total_expenses:.2f}")

if __name__ == "__main__":
    main()
