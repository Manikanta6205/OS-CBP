from tkinter import Button, Entry, Label

from Libs.pyImage.Image import Image

__author__ = 'TheBigEye'
__version__ = '2.0'

# Specific Colors
Login_background_color = "#477afb"
Login_entry_color = "#5A7EFC"

def Login(master):  # Display the login window

    global Login_GUI, Login_Button_icon, Shutdown_Button_icon

    master.configure(background = Login_background_color)  # Sets the background to Blue

    Login_GUI = Image.setImage("Assets/Shell/Boot/Login/Login.png")
    Login = Label(master, image = Login_GUI, borderwidth="0.1")
    Login.place(x=0, y=0)

    # Login entry (Password)
    Login_Password_Entry = Entry(
        Login,
        width = 20,
        show = "•",
        borderwidth = "0.1",
        fg = "#ffffff",
        background = Login_entry_color,
        font = ("Segou UI", 10)
    )

    Login_Password_Entry.config(insertbackground= "#ffffff")
    Login_Password_Entry.insert(0,"Password") # the best password
    Login_Password_Entry.focus()
    Login_Password_Entry.place(x= 435, y= 344)

    Login_Button_icon = Image.setImage("Assets/Shell/Boot/Login/Login.png")
    Login_Button = Button(Login,
        width = 30,
        height = 19,
        borderwidth = "0",
        relief = "raised",
        image = Login_Button_icon
    )
    Login_Button.place(x = 495, y = 384)
    
    # Add shutdown button
    def shutdown_system():
        """Shutdown the system safely"""
        # Display a shutdown message
        shutdown_label = Label(
            Login,
            text="Shutting down...",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg="#3b67d6"
        )
        shutdown_label.place(x=430, y=250)
        # Schedule the actual exit after showing the message
        master.after(1500, master.destroy)
    
    # Create shutdown button with power icon
    Shutdown_Button_icon = Image.setImage("Assets/Shell/Boot/Login/Shutdown.png", (24, 24), "#ff00ff", "#3b67d6")
    Shutdown_Button = Button(
        Login,
        width = 24,
        height = 24,
        borderwidth = "0",
        relief = "flat",
        bg = "#3b67d6", 
        activebackground = "#4b77e6",
        image = Shutdown_Button_icon,
        command = shutdown_system
    )
    Shutdown_Button.place(x = 30, y = 30)  # This places the button at the top-left corner
