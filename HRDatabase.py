import mysql.connector
from tkinter import *
from tkinter import messagebox
import os


# Change accordingly
My_database = mysql.connector.connect(
    host = "localhost",
    user = "sj",
    passwd = "" 
    )

Mycursor = My_database.cursor()

Mycursor.execute("CREATE DATABASE IF NOT EXISTS hr_database") # Creates database if it doesn't exist

Mycursor.execute("USE hr_database") # Use database previously created to perform the following

# Create table: use first name, last name, username, password
Table_login_details = """
CREATE TABLE IF NOT EXISTS login_details (user_id INT(255) PRIMARY KEY AUTO_INCREMENT, first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL,
username VARCHAR(16) UNIQUE NOT NULL , password VARCHAR(255) NOT NULL )""" # Primary Key : user_id, Username: UNIQUE 
Mycursor.execute(Table_login_details)


View_login_details = """
SELECT *
FROM login_details"""
Mycursor.execute(View_login_details)
My_Login = Mycursor.fetchall() # Returned as[(Sandrine, Joseph,...),..]: list of tuples


# Dictionary storing log in details 
Dictionary_login = {} # Username and password
Dictionary_info = {} # Id and both names

for Each_User in range(len(My_Login)): # range(len returns each_line as an index 
    (User_ID, FirstName,LastName, Username,Pwd)= list(My_Login[Each_User]) # Returns each row as a list  
    Dictionary_login[Username] = Pwd # Id is the key, #Pwd is the key value
    Full_name = FirstName + " " + LastName
    Dictionary_info[Username] = Full_name
        


# Main Window

Main_Window = Tk() # Creates window
Main_Window.configure(background='lightblue3')
Main_Window.title("XYZ Company")


Label(Main_Window, text="", bg = "lightblue3").grid(row=0) # Creates space at row 0 [Empty Space]


Label(Main_Window, text="Username: ", bg = "lightblue3").grid(row = 1,sticky=W) # Position of text : W, position of grid (1,0) 


Label(Main_Window, text="", bg = "lightblue3").grid(row=2) # Creates space at row 2 [Empty Space]

Label(Main_Window, text="Password: ", bg = "lightblue3").grid(row=3, sticky=W) 

Verify_user = StringVar() # Define variable first as empty string
Verify_Pass = StringVar()

Entry(Main_Window,textvariable = Verify_user).grid(row=1, column=1) # Takes entry from user, textvariable : Used to refer to this input [Input Username]
Entry(Main_Window,textvariable = Verify_Pass, show = "*").grid(row=3, column=1) # [Input Password]

Empty_Line3 = Label(Main_Window, text="", bg = "lightblue3").grid(row=4) # [Empty Space]




# Function to verify log in details
def Verify_login():

    User = Verify_user.get() # get : retrieves corresponding input
    Pass = Verify_Pass.get()

    if len(User) != 0 and len(Pass)!=0: # Both fields are filled
        if User in Dictionary_login: # If User is a key in Dictionary_login
            if Pass == Dictionary_login[User]:
                Main_Window.withdraw() # Closes main window
                Login(User) # Proceed to open menu window
            else:
                Label(Main_Window, text="Incorrect Password.", fg = "red", bg = "lightblue3").grid(row=4) # Error Message [Incorrect Password]
        else:
                Label(Main_Window, text="Username does not exist.", fg = "red", bg = "lightblue3").grid(row=2) # Error Message [Incorrect username]
    elif len(User) == 0:
        Label(Main_Window, text="* Field should not be blank!", fg = "red", bg = "lightblue3").grid(row=2) # Error Message [Blank Username]
        
    else:
        Label(Main_Window, text="* Field should not be blank!", fg = "red", bg = "lightblue3").grid(row=4) # Error Message [Blank Password]

    
Button_Login = Button(Main_Window, text = "Log In", bg = "gray35", command = Verify_login).grid(row=5, column = 1) # Log in button




# Registration Window
def Register():
    Main_Window.withdraw()
    global Window_registration 
    Window_registration = Toplevel(Main_Window) # Appears over main, neccessary step for inner function
    
    Window_registration.title("Registration Form")
    Label(Window_registration, text="").grid(row=0) # [Empty Space]
    Label(Window_registration, text="Enter your first name: ").grid(row=1)
    Label(Window_registration, text="").grid(row=2) # [Empty Space]
    Label(Window_registration, text="Enter your last name: ").grid(row=3)
    Label(Window_registration, text="").grid(row=4) # [Empty Space]
    Label(Window_registration, text="Create a new username: ").grid(row=5)
    Label(Window_registration, text="").grid(row=6) # [Empty Space]
    Label(Window_registration, text="Create a new password: ").grid(row=7)
    Label(Window_registration, text="Retype the password: ").grid(row=9)

    
    FirstName = StringVar()
    LastName = StringVar()
    New_Username = StringVar()
    New_Password = StringVar()
    Valid_Password = StringVar()
    
    FirstName = Entry(Window_registration,textvariable = FirstName) # [Input First Name]
    FirstName.grid(row=1, column=1)
    LastName = Entry(Window_registration,textvariable = LastName) # [Input Last Name]
    LastName.grid(row=3, column=1)
    New_User = Entry(Window_registration,textvariable = New_Username) # [Input New Username]
    New_User.grid(row=5, column=1)
    New_Pass = Entry(Window_registration,textvariable = New_Password, show = "*") # [Input New Password]
    New_Pass.grid(row=7, column=1)
    Valid_Pass = Entry(Window_registration,textvariable = Valid_Password, show = "*") # [Input New Password]
    Valid_Pass.grid(row=9, column=1) 

    # Registration completed
    def Complete_Register():
        global Username_info
        Username_info = New_Username.get()
        Password_info = New_Password.get()
        ValidPassword_info = Valid_Password.get()
        FirstName_info = FirstName.get()
        LastName_info = LastName.get()

        
        if Username_info in Dictionary_login:
            Label(Window_registration, text = "Username already taken.",fg = "red").grid(row=6)
            
        elif len(Username_info) == 0 or len(Password_info) == 0:
            # message box display
            messagebox.showerror("Error", "No fields should be left blank.")
        elif ValidPassword_info != Password_info:
            Label(Window_registration, text = "Passwords do not match.",fg = "red").grid(row=10)
        else:
            Dictionary_login[Username_info] = Password_info
            Dictionary_info[Username_info] = FirstName_info.capitalize() + " " + LastName_info.capitalize()

            # Insert the rows

            Insert_NewUser_details = """
                INSERT IGNORE INTO login_details (first_name,last_name,username,password)
                VALUES (%s, %s, %s, %s)""" # Insert ignore: ignores records where [any variable] username (unique) triggers warnings. Used to by pass duplicate error when re-running script
            NewUser_details = (FirstName_info.capitalize(), LastName_info.capitalize(), Username_info, Password_info)

            Mycursor.execute(Insert_NewUser_details,NewUser_details)
            My_database.commit() # Necessary for new rows to be added
            

            Window_registration.destroy() # Closes Toplevel window
            Login(Username_info)

    # Register button on registration window
    Label(Window_registration, text="").grid(row=11) # [Empty Space]
    Button_CompleteRegister =  Button(Window_registration, text = "Register", bg = "gray35", command = Complete_Register).grid(row=12, column = 1)

    # Insert a column space near edge
    for each_row in range(12):
        Label(Window_registration, text="").grid(row=each_row,column = 3) # Add empty column before window ends
        
    
    Window_registration.mainloop()

Button_Register = Button(Main_Window, text = "New User", bg = "gray35", command = Register).grid(row=5, column = 2) # Register button on Main Window



def Login(User_logged):
    WelcomePage = Tk()

    # Welcome
    (Logged_First, Logged_Last) = Dictionary_info[User_logged].split()
    Label(WelcomePage, text = "Welcome" + " " + Logged_First + "!").grid(row = 0)
 
    WelcomePage.grid(row = 0,column = 1)


    Window_menu.mainloop()
    
    
Main_Window.mainloop() # Ensures main menu stays open until close button pressed









