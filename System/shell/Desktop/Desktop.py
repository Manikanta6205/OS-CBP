"""
    Module Name:
        Desktop.py

    Module Description:
        This module implements the Desktop interface.
        - add_shutdown_button
        etc ...
"""

import os
from tkinter import Button, Label
from Libs.pyImage.Image import Image

__author__ = "TheBigEye"

def add_shutdown_button(desktop):
    """Add a shutdown button to the desktop"""
    
    def shutdown_system():
        """Shutdown the system safely"""
        # Display a shutdown message
        shutdown_label = Label(
            desktop,
            text="Shutting down...",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg="#3b67d6"
        )
        shutdown_label.place(relx=0.5, rely=0.5, anchor="center")
        # Schedule the actual exit after showing the message
        desktop.after(1500, desktop.destroy)
    
    # Create shutdown button with power icon
    try:
        # First try to use a power icon image
        Shutdown_Button_icon = Image.setImage("Assets/Shell/Desktop/Icons/power.png", (32, 32))
    except:
        # If image not found, set icon to None for text fallback
        Shutdown_Button_icon = None
    
    # Create the shutdown button
    Shutdown_Button = Button(
        desktop,
        width = 32 if Shutdown_Button_icon else 3,
        height = 32 if Shutdown_Button_icon else 1,
        borderwidth = 1,
        relief = "raised",
        bg = "#ffffff", 
        activebackground = "#e0e0e0",
        image = Shutdown_Button_icon,
        text = "⏻" if not Shutdown_Button_icon else "",  # Power symbol as fallback
        command = shutdown_system
    )
    
    # Place button on desktop - bottom right corner
    Shutdown_Button.place(x=desktop.winfo_width()-50, y=desktop.winfo_height()-50)
    
    # Save references to prevent garbage collection
    desktop.shutdown_button_icon = Shutdown_Button_icon
    desktop.shutdown_button = Shutdown_Button
    
    return Shutdown_Button

# Call this function after desktop initialization
# add_shutdown_button(desktop)  # Add this line where 'desktop' is your main desktop frame/window