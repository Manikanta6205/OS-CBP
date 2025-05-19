"""
    Module Name:
        ShutdownButton.py

    Module Description:
        This module implements a shutdown button for the desktop.
"""

from tkinter import Button, Label
from Libs.pyImage.Image import Image

def create_shutdown_button(master):
    """Creates a shutdown button in the bottom-right corner of the desktop"""
    
    def shutdown_system():
        """Shutdown the system safely"""
        # Display a shutdown message
        shutdown_label = Label(
            master,
            text="Shutting down...",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg="#3b67d6"
        )
        shutdown_label.place(relx=0.5, rely=0.5, anchor="center")
        # Schedule the actual exit after showing the message
        master.after(1500, master.destroy)
    
    # Create shutdown button with power icon
    try:
        # Try to load SVG if available
        Shutdown_Button_icon = Image.svg_to_image("Assets/Shell/Desktop/Icons/Shutdown.svg", (24, 24), "#3b67d6")
    except:
        # Fallback to PNG
        try:
            Shutdown_Button_icon = Image.setImage("Assets/Shell/Desktop/Icons/Shutdown.png", (24, 24), "#ff00ff", "#3b67d6")
        except:
            # Create a simple colored button if image loading fails
            Shutdown_Button_icon = None
    
    # Create the button in the taskbar area (bottom of screen)
    Shutdown_Button = Button(
        master,
        width = 24 if Shutdown_Button_icon else 2,
        height = 24 if Shutdown_Button_icon else 1,
        borderwidth = "0",
        relief = "flat",
        bg = "#3b67d6", 
        activebackground = "#4b77e6",
        image = Shutdown_Button_icon,
        text = "⏻" if not Shutdown_Button_icon else "",  # Power symbol as fallback
        command = shutdown_system
    )
    
    # Place in the bottom-right corner of the screen
    Shutdown_Button.place(x=master.winfo_screenwidth()-40, y=master.winfo_screenheight()-40, anchor="se")
    
    # Keep a reference to prevent garbage collection
    master.shutdown_button_icon = Shutdown_Button_icon
    master.shutdown_button = Shutdown_Button
    
    return Shutdown_Button
