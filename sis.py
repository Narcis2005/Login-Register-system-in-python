import hashlib
import mysql.connector

# MySQL connection
mydb = mysql.connector.connect(host="localhost", user="root", passwd="password123", database="testDB")
mycursor = mydb.cursor(buffered=True)
# Starting the program

YN = input("Do you have an account? (y/n) ")
while YN not in ["y", "n"]:
    YN = input("Not a valid answer. Choose again. (y/n) ")
# Register function
def register():
    global username
    username = ""
    Check = True
    while Check:
        username = input("Type your username: ")
        mycursor.execute('SELECT username FROM users WHERE username = %(username)s', {'username': username})
        result = mycursor.fetchall()
        if len(result) > 0:
            print("Username already taken")
            register()
        else:
            Check = False

    CreatePassword = input("Type your password: ")
    RepeatPassword = input("Repeat password: ")
    age = input("Type age: ")
    email = input("Type email: ")
    full_name = input("Type your full name: ")
    if CreatePassword == RepeatPassword:
        x = hashlib.sha256(CreatePassword.encode('utf-8'))
        Account = (username, x.hexdigest(), int(age), email, full_name)
        insert_command = "INSERT INTO users (username, password, age, email, full_name) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(insert_command, Account)
        mydb.commit()
    else:
        print("You typed something wrong. Try again")

# login function
def login():
    user_email = input("Type your email or your username: ")
    password = input("Type your password: ")
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    mycursor.execute("SELECT * FROM users WHERE username = %(username)s OR email= %(username)s AND password = %(password)s",
                     {'username': user_email, 'password': password})
    if mycursor.fetchall():
        print("You have connected")
    else:
        print("Username/email or password is wrong. Try again.")
        login()


if YN == "y":
    login()
else:
    register()
