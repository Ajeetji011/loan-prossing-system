from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import ast
import os
import re

# ----- Main Window Setup -----
root = Tk()
root.title('Login System')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.configure(bg="#fff")
root.resizable()

# ----- Authentication Functions -----
def load_users():
    users = {}
    try:
        if os.path.exists('datasheet.txt'):
            with open('datasheet.txt', 'r') as file:
                raw_data = ast.literal_eval(file.read())
                for user, details in raw_data.items():
                    if isinstance(details, dict):
                        users[user] = details
                    else:
                        users[user] = {'password': details, 'email': '', 'mobile': ''}
    except Exception as e:
        print(f"Error reading user data: {e}")
    return users

def save_users(users):
    with open('datasheet.txt', 'w') as file:
        file.write(str(users))

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def signin():
    identifier = identifier_entry.get()
    password = password_entry.get()
    users = load_users()

    for user, details in users.items():
        if (user == identifier or details.get('email') == identifier or details.get('mobile') == identifier) and details.get('password') == password:
            root.withdraw()
            open_loan_form()
            return

    messagebox.showerror('Invalid', 'Invalid username, email, or mobile number, or password.')

def signup_command():
    def signup():
        new_username = user_entry.get()
        new_password = pass_entry.get()
        confirm_password = confirm_entry.get()
        new_email = email_entry.get()
        new_mobile = mobile_entry.get()

        if new_username in ["", "Username"] or new_password in ["", "Password"] or new_email in ["", "Email"] or new_mobile in ["", "Mobile"]:
            messagebox.showerror('Error', 'Please fill all fields.')
            return
        if len(new_password) < 8:
            messagebox.showerror('Error', 'Password must be at least 8 characters long.')
            return
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
        if not re.match(pattern, new_password):
            messagebox.showerror('Error', 'Password must include uppercase, lowercase, digit, and special character.')
            return

        if not re.match(r"^\d{10}$", new_mobile):
            messagebox.showerror('Error', 'Please enter a valid mobile number (10 digits).')
            return

        if not is_valid_email(new_email):
            messagebox.showerror('Error', 'Please enter a valid email address.')
            return

        if new_password != confirm_password:
            messagebox.showerror('Error', 'Passwords do not match.')
            return

        users = load_users()
        if new_username in users:
            messagebox.showerror('Error', 'Username already exists.')
            return

        for user, details in users.items():
            if isinstance(details, dict):
                if details.get('email') == new_email:
                    messagebox.showerror('Error', 'Email already exists.')
                    return
                if details.get('mobile') == new_mobile:
                    messagebox.showerror('Error', 'Mobile number already exists.')
                    return

        users[new_username] = {
            'password': new_password,
            'email': new_email,
            'mobile': new_mobile
        }
        save_users(users)
        messagebox.showinfo('Success', 'Signed up successfully!')
        signup_window.destroy()

    signup_window = Toplevel(root)
    signup_window.title('Sign Up')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    signup_window.geometry(f"{screen_width}x{screen_height}+0+0")
    signup_window.configure(bg="#fff")
    signup_window.resizable()

    try:
        img = PhotoImage(file='login2.png')
        Label(signup_window, image=img, bg='white').place(x=150, y=190)
        signup_window.image = img
    except:
        pass

    frame = Frame(signup_window, width=600, height=550, bg="white")
    frame.place(x=580, y=50)

    Label(frame, text='Sign up', fg='#57a1f8', bg='white',
          font=('Microsoft YaHei UI Light', 28, 'bold')).place(x=260, y=5)

    def entry_box(y, placeholder, show=None):
        entry = Entry(frame, width=25, fg='black', border=0,
                      bg="white", font=('Microsoft YaHei UI Light', 11), show=show)
        entry.place(x=192, y=y)
        entry.insert(0, placeholder)

        def on_enter(e):
            if entry.get() == placeholder:
                entry.delete(0, END)
                if show:
                    entry.config(show='*')
        def on_leave(e):
            if entry.get() == '':
                entry.insert(0, placeholder)
                if show:
                    entry.config(show='')

        entry.bind('<FocusIn>', on_enter)
        entry.bind('<FocusOut>', on_leave)
        Frame(frame, width=295, height=2, bg="black").place(x=188, y=y+27)
        return entry

    user_entry = entry_box(80, 'Username')
    pass_entry = entry_box(150, 'Password', show='')
    confirm_entry = entry_box(220, 'Confirm Password', show='')
    email_entry = entry_box(290, 'Email')
    mobile_entry = entry_box(360, 'Mobile')

    Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white',
           border=0, command=signup).place(x=200, y=410)

    Label(frame, text="I have an account?", fg='black', bg='white',
          font=('Microsoft YaHei UI Light', 9)).place(x=250, y=450)

    Button(frame, width=6, text='Sign in', border=0, bg='white',
           cursor='hand2', fg='#57a1f8', command=signup_window.destroy).place(x=360, y=450)

    signup_window.mainloop()

# ------- New Window for EMI Calculator -------
def open_emi_calculator():
    emi_win = Toplevel(root)
    emi_win.title("EMI Calculator")
    emi_win.geometry('400x400+500+250')
    emi_win.configure(bg="#fff")
    emi_win.resizable()

    Label(emi_win, text="EMI Calculator", font=('Microsoft YaHei UI Light', 20, 'bold'), fg='#57a1f8', bg='white').pack(pady=20)

    frame = Frame(emi_win, bg="white")
    frame.pack(padx=20, pady=10, fill=BOTH, expand=True)

    def form_entry(y, placeholder):
        entry = Entry(frame, width=25, fg='black', border=1,
                      bg="white", font=('Microsoft YaHei UI Light', 11))
        entry.pack(pady=5)
        entry.insert(0, placeholder)

        def on_enter(e):
            if entry.get() == placeholder:
                entry.delete(0, END)

        def on_leave(e):
            if entry.get() == '':
                entry.insert(0, placeholder)

        entry.bind('<FocusIn>', on_enter)
        entry.bind('<FocusOut>', on_leave)
        return entry

    principal_entry = form_entry(0, 'Loan Amount')
    interest_entry = form_entry(0, 'Annual Interest Rate (%)')
    tenure_entry = form_entry(0, 'Tenure (Months)')

    emi_result_var = StringVar()
    emi_result_var.set('')

    def calculate_emi():
        try:
            principal_text = principal_entry.get()
            interest_text = interest_entry.get()
            tenure_text = tenure_entry.get()
            # Prevent placeholder values calculation
            if principal_text in ('Loan Amount', '') or interest_text in ('Annual Interest Rate (%)', '') or tenure_text in ('Tenure (Months)', ''):
                raise ValueError("Fill all fields")

            principal = float(principal_text)
            annual_rate = float(interest_text)
            tenure = int(tenure_text)

            if principal <= 0 or annual_rate < 0 or tenure <= 0:
                raise ValueError("Invalid inputs")

            monthly_rate = annual_rate / (12 * 100)
            emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
            emi_result_var.set(f"EMI: ₹ {emi:,.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

    Button(frame, text="Calculate EMI", width=20, bg='#57a1f8', fg='white', command=calculate_emi).pack(pady=20)

    Label(frame, textvariable=emi_result_var, font=('Microsoft YaHei UI Light', 14, 'bold'), fg='black', bg='white').pack(pady=10)

# ----- Loan Form and Summary -----
def open_loan_form():
    form = Toplevel(root)
    form.title('Loan Application')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    form.geometry(f"{screen_width}x{screen_height}+0+0")
    form.configure(bg="#fff")
    form.resizable()

    try:
        img = PhotoImage(file='login.png')
        Label(form, image=img, bg='white').place(x=150, y=150)
        form.image = img
    except:
        pass

    frame = Frame(form, width=650, height=700, bg="white")
    frame.place(x=550, y=70)

    Label(frame, text='Loan Application Form', fg='#57a1f8', bg='white',
          font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=220, y=3)

    def form_entry(y, placeholder):
        entry = Entry(frame, width=25, fg='black', border=0,
                      bg="white", font=('Microsoft YaHei UI Light', 13))
        entry.place(x=250, y=y)
        entry.insert(0, placeholder)

        def on_enter(e):
            if entry.get() == placeholder:
                entry.delete(0, END)

        def on_leave(e):
            if entry.get() == '':
                entry.insert(0, placeholder)

        entry.bind('<FocusIn>', on_enter)
        entry.bind('<FocusOut>', on_leave)
        Frame(frame, width=295, height=2, bg="black").place(x=245, y=y+27)
        return entry

    name_entry = form_entry(80, 'Applicant Name')
    age_entry = form_entry(150, 'Age')
    income_entry = form_entry(220, 'Monthly Income')
    loan_amount_entry = form_entry(290, 'Loan Amount')

    loan_type_combo = Combobox(form, width=50, state="readonly")
    loan_type_combo['values'] = ("Home Loan", "Car Loan", "Personal Loan", "Education Loan")
    loan_type_combo.set("Loan type")
    loan_type_combo.place(x=790, y=420)
    

    Button(frame, width=39, pady=7, text='Open EMI Calculator', bg='#f39c12', fg='white', border=0,
           command=open_emi_calculator).place(x=255, y=390)

    def submit_application():
        name = name_entry.get()
        age = age_entry.get()
        income = income_entry.get()
        loan_amount = loan_amount_entry.get()
        loan_type = loan_type_combo.get()

        errors = []

        try:
            age_val = int(age)
            if not (18 <= age_val <= 65):
                errors.append("Age must be between 18 and 65.")
        except ValueError:
            errors.append("Invalid age.")

        try:
            income_val = float(income)
            if income_val <= 0:
                errors.append("Income must be positive.")
        except ValueError:
            errors.append("Invalid income.")

        try:
            loan_amount_val = float(loan_amount)
            if loan_amount_val <= 0:
                errors.append("Loan amount must be positive.")
        except ValueError:
            errors.append("Invalid loan amount.")

        if name in ["", "Applicant Name"]:
            errors.append("Enter applicant name.")
        if loan_type == "":
            errors.append("Select loan type.")

        if not errors:
            min_income = {
                "Home Loan": 3000,
                "Car Loan": 2000,
                "Personal Loan": 1500,
                "Education Loan": 1000
            }
            if income_val < min_income.get(loan_type, 0):
                errors.append(f"Minimum income for {loan_type} is ${min_income[loan_type]:.2f}.")
            if loan_amount_val > income_val * 20:
                errors.append(f"Loan exceeds maximum allowed (${income_val * 20:.2f}).")

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
        else:
            with open("loan_applications.txt", "a") as f:
                f.write(f"Name: {name}\nAge: {age_val}\nMonthly Income: ${income_val:.2f}\nLoan Amount: ${loan_amount_val:.2f}\nLoan Type: {loan_type}\n{'-'*40}\n")
            for entry in [name_entry, age_entry, income_entry, loan_amount_entry]:
                entry.delete(0, END)
            name_entry.insert(0, 'Applicant Name')
            age_entry.insert(0, 'Age')
            income_entry.insert(0, 'Monthly Income')
            loan_amount_entry.insert(0, 'Loan Amount')
            loan_type_combo.set('')
            messagebox.showinfo("Success", "Application Submitted Successfully!")

    Button(frame, width=39, pady=7, text='Submit', bg='#57a1f8', fg='white', border=0,
           command=submit_application).place(x=255, y=450)

    Button(frame, width=39, pady=7, text='View Applications', bg='#57a1f8', fg='white', border=0,
           command=open_summary_page).place(x=255, y=490)

def open_summary_page():
    summary = Toplevel(root)
    summary.title('Application Summary')
    summary.geometry('600x400+300+200')
    summary.configure(bg="#fff")
    summary.resizable()

    frame = Frame(summary, bg="white")
    frame.pack(pady=20, padx=10, fill=BOTH, expand=True)

    Label(frame, text='Loan Application Summary', fg='#57a1f8', bg='white',
          font=('Microsoft YaHei UI Light', 23, 'bold')).pack(pady=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    summary_text = Text(frame, wrap=WORD, bg="lightgrey", fg="black", font=('Microsoft YaHei UI Light', 11),
                        yscrollcommand=scrollbar.set)
    summary_text.pack(pady=10, fill=BOTH, expand=True)
    scrollbar.config(command=summary_text.yview)

    try:
        with open("loan_applications.txt", "r") as f:
            content = f.read()
            summary_text.insert(END, content if content.strip() else "No applications found.")
    except FileNotFoundError:
        summary_text.insert(END, "No applications found.")

    summary_text.config(state=DISABLED)

    Button(frame, text='Close', command=summary.destroy, bg='#57a1f8', fg='white').pack(pady=10)

# ----- UI Setup for Main Login Window -----
try:
    img = PhotoImage(file='login.png')
    Label(root, image=img, bg='white').place(x=230, y=170)
    root.image = img
except:
    pass

login_frame = Frame(root, width=750, height=550, bg="white")
login_frame.place(x=680, y=70)

Label(login_frame, text='Sign in', fg='#57a1f8', bg='white',
      font=('Microsoft YaHei UI Light', 28, 'bold')).place(x=150, y=110)

identifier_entry = Entry(login_frame, width=25, fg='black', border=0, bg="white",
                        font=('Microsoft YaHei UI Light', 13))
identifier_entry.place(x=80, y=210)
identifier_entry.insert(0, 'Username / Email / Mobile')
def on_enter_identifier(e):
    if identifier_entry.get() == 'Username / Email / Mobile':
        identifier_entry.delete(0, END)
def on_leave_identifier(e):
    if identifier_entry.get() == '':
        identifier_entry.insert(0, 'Username / Email / Mobile')
identifier_entry.bind('<FocusIn>', on_enter_identifier)
identifier_entry.bind('<FocusOut>', on_leave_identifier)
Frame(login_frame, width=300, height=2, bg="black").place(x=75, y=237)

password_entry = Entry(login_frame, width=25, fg='black', border=0, bg="white",
                       font=('Microsoft YaHei UI Light', 13), show='')
password_entry.place(x=80, y=280)
password_entry.insert(0, 'Password')
def on_enter_password(e):
    if password_entry.get() == 'Password':
        password_entry.delete(0, END)
        password_entry.config(show='*')
def on_leave_password(e):
    if password_entry.get() == '':
        password_entry.insert(0, 'Password')
        password_entry.config(show='')
password_entry.bind('<FocusIn>', on_enter_password)
password_entry.bind('<FocusOut>', on_leave_password)
Frame(login_frame, width=295, height=2, bg="black").place(x=75, y=307)

Button(login_frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white',
       border=0, command=signin).place(x=85, y=334)

Label(login_frame, text="Don't have an account?", fg='black', bg='white',
      font=('Microsoft YaHei UI Light', 9)).place(x=125, y=400)

Button(login_frame, width=6, text='Sign up', border=0, bg='white',
       cursor='hand2', fg='#57a1f8', command=signup_command).place(x=262, y=400)

Label(login_frame, text='Project by INDERJEET', fg='#57a1f8', bg='white',
      font=('Microsoft YaHei UI Light', 18, 'bold')).place(x=100, y=440)

root.mainloop()

