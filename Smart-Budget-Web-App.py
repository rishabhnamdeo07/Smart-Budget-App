import streamlit as st
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt

#--------- PAGE SETTINGS ---------#

st.set_page_config(page_title="SmartBudget Lite", page_icon="💰", layout="wide")

st.markdown(""" 
<style>
            
/* ===== SECTION BOX ===== */
.section-box {
    max-width: 600px;
    margin: auto;
    padding: 8px;
    border-radius: 10px;
    border: 1px solid #E6E6E6;
    background-color: #FFFFFF;
    margin-bottom: 15px;
}
            
/* ===== TITLE CENTER ===== */
.title-center {
    text-align: center;
}
            
/* ===== SMALL TEXT ===== */
.small-text {
    color: gray;
    font-size: 14px;
    text-align: center;
}
       
/* ===== CARD DESIGN ONLY ===== */
.card {
    background-color: #1E222A;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 3px 8px
rgba(0,0,0,0.25);
}
            
/* Card Title */
.card h3 {
    color: #AAAAAA;
    font-size: 16px;
    margin-bottom: 5px;
}
            
/* Card Value */
.card h1 {
    color: #FFFFFF;
    font-size: 26px;
    margin: 0;
}
            
/* ===== DIVIDER ===== */
.divider {
    height: 1px;
    background: #E6E6E6;
    margin: 15px 0;
}
            
</style>
""", unsafe_allow_html=True)

#--------- USER LOGIN ---------#

if "username" not in st.session_state:
    st.session_state.username = ""

if "username1" not in st.session_state:
    st.session_state.username1 = ""

if st.session_state.username == "":
    st.markdown('<div class="title-center"><h1>💰 SmartBudget Lite</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="small-text">Track Smart. Save Better.</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-text">👨‍💻 Developed By Rynex Labs</div>', unsafe_allow_html=True)

    name1 = st.text_input("Enter your Name :")
    name = st.text_input("Enter your Username :(Please enter a username that ensures no one else can access your data)")
    if st.button("Start"):
        if name.strip() != "":
            st.session_state.username = name
            st.session_state.username1 = name1

            st.rerun()

    st.stop()

username = st.session_state.username
username1 = st.session_state.username1

st.title("💰 SmartBudget Lite")
st.write(f"Welcome **{username1}** 👋")

if st.button("Logout"):
    st.session_state.username = ""
    st.rerun()

#---------- LOAD MORE DATA ---------#

filename = f"{username}_expenses.csv"

if os.path.exists(filename):
    df = pd.read_csv(filename)
else:
    df = pd.DataFrame(columns=["Type", "Category", "Amount", "Data"])

#--------- SIDEBAR INPUT ---------#

st.sidebar.header("Add Transaction")

t_type = st.sidebar.selectbox("Type", ["Income", "Expense"])

category = st.sidebar.text_input("Category")

amount = st.sidebar.number_input("Amount", min_value=0)

date = st.sidebar.date_input("Date", datetime.date.today())

if st.sidebar.button("Add Transaction"):
    new_data = pd.DataFrame({"Type":[t_type], "Category":[category], "Amount":[amount], "Date":[str(date)]})

    df = pd.concat([df,new_data],ignore_index=True)

    df.to_csv(filename,index=False)

    st.sidebar.success("Transaction Saved!")

#--------- STREAK SYSTEM ---------#

st.markdown('<div class="section-box">', unsafe_allow_html=True)
streak_file = "streak.txt"
today = datetime.date.today()

if os.path.exists(streak_file):
    with open(streak_file, "r") as f:
        data = f.read().split(",")

        last_date = datetime.datetime.strptime(data[0],"%Y-%m-%d").date()
        streak = int(data[1])
else:
    last_date = today
    streak = 0

if today == last_date:
    pass
elif today == last_date + datetime.timedelta(days=1):
    streak += 1
else:
    streak = 1

with open(streak_file, "w") as f:
    f.write(f"{today},{streak}")

st.subheader("🔥 Daily Streak")
st.write(f"you are on a **{streak} day streak!**")

st.markdown('</div>',unsafe_allow_html=True)

# --------- DASHBOARD SUMMARY ---------#

st.markdown('<div class="section-box">', unsafe_allow_html=True)
if not df.empty:
    income = df[df["Type"]=="Income"]["Amount"].sum()
    expense = df[df["Type"]=="Expense"]["Amount"].sum()
    balance = income - expense

    st.subheader("📊 Financial Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="card"><h3>💰 Income</h3><h1>₹{income}</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="card"><h3>💸 Expense</h3><h1>₹{expense}</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="card"><h3>🏛 Balance</h3><h1>₹{balance}</h1></div>', unsafe_allow_html=True)

st.markdown('</div>',unsafe_allow_html=True)
#--------- TRANSACTIONS ---------#

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("📜 Transactions")

st.dataframe(df,use_container_width=True)


#--------- DELETE TRANSACTION ---------#

st.subheader("🗑 Delete Transaction")

if not df.empty:
    delete_index = st.number_input("Enter transaction index", min_value=0, max_value=len(df)-1, step=1)

    if st.button("Delete"):
        df = df.drop(delete_index).reset_index(drop=True)
        df.to_csv(filename,index=False)

        st.success("Transaction Deleted")
        st.rerun()

st.markdown('</div>',unsafe_allow_html=True)

#------- -- EXPENSE BY CATEGORY ---------#

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("📈 Expense by Category")
expense_df = df[df["Type"]=="Expense"]
if not expense_df.empty:
    chart_data = expense_df.groupby("Category")["Amount"].sum()
    st.bar_chart(chart_data)

st.markdown('</div>',unsafe_allow_html=True)

#--------- REMAINING DAILY BUDGET ---------#

st.markdown('<div class="section-box">', unsafe_allow_html=True)

st.subheader("📋 Remaining Budget Per Day")
budget = st.number_input("Enter Monthly Budget (₹)", min_value=0)
if budget > 0:
    today = datetime.date.today()
    import calendar

    total_days = calendar.monthrange(today.year, today.month)[1]
    remaining_days = total_days - today.day + 1

    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    remaining_budget = budget - expense

    if remaining_days > 0:
        per_day = remaining_budget / remaining_days
    else:
        per_day = 0

    st.write(F"📅 You can spend ₹{per_day:.2f} per day")

#--------- WEEKLY ALERT ---------#

st.subheader("🚨 Weekly Alert")
if not df.empty:
    expense_df = df[df["Type"]=="Expense"]

    expense_df["Date"] = pd.to_datetime(expense_df["Date"])
    last_week = datetime.datetime.now()-datetime.timedelta(days=7)

    weekly_spending = expense_df[expense_df["Date"] >= last_week]["Amount"].sum()
    st.info(f"Your spending over the last 7 days is: ₹{weekly_spending}")

st.markdown('</div>',unsafe_allow_html=True)

#--------- SMART INSIGHT ---------#

st.markdown('<div class="section-box">', unsafe_allow_html=True)

st.subheader("💡 Smart Insight")
if not df.empty:

    income1 = df[df["Type"] == "Income"]["Amount"].sum()
    expense1 = df[df["Type"] == "Expense"]["Amount"].sum()
    expense_df1 = df[df["Type"] == "Expense"]

    if expense1 > income1:
        st.error("⚠ You are spending more than you earn! Try reducing unnecessary expenses.\nSpend less,save more.")

    elif expense1 > income1 * 0.8:
        st.warning("⚠ You are close to your income limit and Spend a little less now.")

    else:
        st.success("✅ Your spending is under control. You're managing your money well.")

    if not expense_df1.empty:
        category_spending = expense_df.groupby("Category")["Amount"].sum()

        top_category = category_spending.idxmax()
        top_amount = category_spending.max()

        st.write(f"Most of your Spending is on **{top_category}** (₹{top_amount})")

    if income1 > 0:
        percent = (expense/income) * 100
        st.write(f"📊 You spent {percent:.1f}% of your income")

    
    if income1 > 0:
        savings = income1 - expense1
        rate = (savings / income) * 100

    st.write(f"💰 Your Savings Rate is: {rate:.1f}%")
    
    st.subheader("📊 Financial Health Score")
    score = 100

    savings = income1 - expense1
    if savings > 0:
        st.success(f"You saved ₹{savings} this period.")

    else:
        st.error("❌ No savings this period. Focus on reducing expenses to start saving.")

    
    if income1 > 0:
        ratio = expense/income
        if ratio > 1:
            score -= 40
        elif ratio > 0.8:
            score -= 20
        elif ratio > 0.6:
            score -= 10
    if savings <= 0:
        score -= 30
    elif savings < income * 0.2:
        score -= 10

    score = max(score, 0)
    st.metric("Your Score", f"{score}/100")

    st.progress(score / 100)

    if score >= 80:
        st.success("🔥 Excellent Financial Health!")
    elif score >= 60:
        st.info("👍 Good, but can improve savings") 
    elif score >= 40:
        st.warning("⚠ Moderate, control your spending")
    else:
        st.error("🚨 Poor financial health, take action now!")
st.markdown('</div>',unsafe_allow_html=True)

#--------- BADGES SYSTEM ---------#

st.subheader("🏆 Achievements")
badges = []

if not df.empty:
    income1 = df[df["Type"] == "Income"]["Amount"].sum()
    expense1 = df[df["Type"] == "Expense"]["Amount"].sum()
    savings = income - expense

    if savings > 0:
        badges.append("💰 Saver Badge")
    if savings > income * 0.2:
        badges.append("🏛 Smart Saver")
    if expense < income:
        badges.append("📉 Budget Master")
    
    if streak >= 3:
        badges.append("🔥 3-Day Streak")
    
    if streak >= 7:
        badges.append("🚀 7-Day Streak")
    
    if streak >= 30:
        badges.append("👑 Discipline King")

if badges:
    for b in badges:
        st.success(b)
else:
    st.info("No Badges yet. Start tracking to earn acievements!")


#---------FEEDBACK---------#

r = st.slider("Rate",1,5)
if st.button("Submit Feedback"):
    st.success("Thank you for your Feedback")
