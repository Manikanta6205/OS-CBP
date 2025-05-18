from tkinter import Button, Frame, Label, Toplevel
from Libs.pyLogger.Logger import Logger
import subprocess
import os
import platform

__author__ = 'TheBigEye'
__version__ = '1.4'

class VideoPlayer(Frame):
    """
    Video Player class - Uses system's default video player
    """
    def __init__(self, master, video_path):
        """
        Video Player constructor
        """
        Frame.__init__(self, master)
        self.master = master
        self.video_path = video_path
        
        # Create a popup to confirm playing the video
        popup = Toplevel(self.master)
        popup.title("Play Video")
        popup.geometry("400x200")
        popup.resizable(False, False)
        popup.configure(bg="#002C4F")
        
        # Add the video name as a label
        video_name = os.path.basename(video_path)
        name_label = Label(
            popup,
            text=f"Selected video: {video_name}",
            bg="#002C4F",
            fg="#F3F3F3",
            font=("Segoe UI", 10)
        )
        name_label.place(x=20, y=40)
        
        # Add play button
        play_btn = Button(
            popup,
            text="Play with System Player",
            bg="#004080",
            fg="#FFFFFF",
            activebackground="#006080",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10),
            command=lambda: self.play_with_system(popup)
        )
        play_btn.place(x=20, y=100)
        
        # Add close button
        close_btn = Button(
            popup,
            text="Cancel",
            bg="#800000",
            fg="#FFFFFF",
            activebackground="#A00000",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10),
            command=popup.destroy
        )
        close_btn.place(x=200, y=100)
        
        # Make sure the popup stays on top and is centered
        popup.transient(self.master)
        popup.grab_set()
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (self.master.winfo_width() // 2) - (width // 2)
        y = (self.master.winfo_height() // 2) - (height // 2)
        popup.geometry(f"+{x}+{y}")

    def play_with_system(self, popup):
        """Play the video with the system's default video player"""
        try:
            # Close the popup
            popup.destroy()
            
            # Use the appropriate command based on the operating system
            system = platform.system()
            if system == "Windows":
                os.startfile(self.video_path)
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", self.video_path])
            else:  # Linux and other Unix-like systems
                subprocess.Popen(["xdg-open", self.video_path])
                
            Logger.info(f"Playing video with system player: {self.video_path}")
        except Exception as e:
            Logger.error(f"Failed to play video: {e}")
