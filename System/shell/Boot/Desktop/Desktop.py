import time
from tkinter import Button, Frame, Label, Toplevel
import random
from tkinter import Listbox, Scrollbar
import os
import subprocess

try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False

from Libs.pyImage.Image import Image
from Libs.pyLogger.Logger import Logger
from Libs.pyUtils.pyData import JSON
from System.core.kernel import KRNL_Bug_check
from System.programs.File_manager.File_manager import File_manager
from System.programs.Map.Map import Map
from System.programs.Terminal.Terminal import WM_Terminal, DE_Terminal
from System.shell.Boot.Desktop.Startmenu import startmenu
from System.shell.Boot.Desktop.Taskbar import Taskbar_button
from System.shell.Message_box import MessageBox
from System.utils.utils import Execute, check_internet
from System.utils.vars import Assets_directory, XCursor_2
from System.programs.VideoPlayer.VideoPlayer import VideoPlayer

__author__ = 'TheBigEye'
__version__ = '2.1'

BOOT_DATA_FILE = (Assets_directory + "/Data/System data/Boot/Boot.json")
DESKTOP_MODE = JSON.get(BOOT_DATA_FILE, "Desktop_mode")

def Terminal_programm(master):
    if DESKTOP_MODE == 0:
        Execute(master, 400, WM_Terminal, master, True)
    elif DESKTOP_MODE == 1:
        Execute(master, 400, DE_Terminal, master, True)

def File_manager_programm(master):
    Execute(master, 1000, File_manager, master, True)

def Browser_programm(master):
    try:
        # Import the Browser module
        from System.programs.Browser.Browser import Browser
        
        # Display a warning but continue with launching the browser
        MessageBox(master, "The browser may not work perfectly as it's still in development", "Warning", True)
        
        # Launch the browser
        Execute(master, 1200, Browser, master, True)
    except Exception as e:
        # If there's an error, show a message box with the error
        MessageBox(master, f"Error launching browser: {str(e)}", "Error", True)
        Logger.error(f"Failed to launch browser: {str(e)}")

def Map_programm(master):
    Execute(master, 800, Map, master, True)

class Desktop(Frame):
    def __init__(self, master):

        Frame.__init__(self, master)

        self.master = master
        self.sound_popup = None  # Track the sound popup window

        # Initialize the desktop
        Desktop.desktop_initializer(self)
        Logger.info("### Desktop initialized!")

# -------------------------------------------------------------[ Desktop ]--------------------------------------------------------------

    def desktop_initializer(self):

        Logger.info("### Loading desktop enviroment ...")

        # Initialize the Wallpaper
        self.Wallpaper_image = Image.setImage("Assets/Shell/Desktop/Wallpapers/Space_panorama.png")
        self.Wallpaper = Label(
            self.master,
            image= self.Wallpaper_image,
            borderwidth="0",
            relief="flat",
            bg="#001023"
        )
        self.Wallpaper.place(x=0, y=0)
        Logger.info("Wallpaper processed and loaded")

        # Initialize the Cursor
        self.master.configure(background = "#001023",cursor = XCursor_2)
        Logger.info("Cursor processed and loaded")

        # Initialize the Taskbar
        self.Taskbar_image = Image.setImage("Assets/Shell/Desktop/Taskbar/Taskbar.png")
        self.Taskbar = Label(
            self.master,
            width = 740,
            height = 29,
            borderwidth = "0",
            image = self.Taskbar_image,
            background = "black",
            foreground = "gray",
            relief = "flat",
        )
        self.Taskbar.place(x= 109, y= 571)
        self.Taskbar.lift()
        Logger.info("Taskbar processed and loaded")

        # Initialize the Start bar
        self.Startbar_image = Image.setImage("Assets/Shell/Desktop/Taskbar/Startbar.png")
        self.Startbar = Label(
            self.master,
            width = 109,
            height = 29,
            borderwidth = "0",
            image = self.Startbar_image,
            background = "white",
            foreground = "gray",
            relief = "flat",
        )
        self.Startbar.place(x= 0, y= 571)
        self.Startbar.lift()
        Logger.info("Startbar processed and loaded")

        # Initialize the Clockbar
        self.Clockbar_image = Image.setImage("Assets/Shell/Desktop/Taskbar/Clockbar.png")
        self.Clockbar = Label(
            self.master,
            width = 284,
            height = 29,
            borderwidth = "0",
            image = self.Clockbar_image,
            background = "white",
            foreground = "gray",
            relief = "flat",
        )
        self.Clockbar.place(x= 849, y= 571)
        self.Clockbar.lift()
        Logger.info("Clockbar processed and loaded")

        # Initialize the Start menu
        startmenu(self.master, self.Startbar)

# -------------------------------------------------------------[ Startbar buttons ]-----------------------------------------------------------

        # Modules icon in startbar
        self.Modules_startbar_button = Taskbar_button(
            self.Startbar,
            button_image_path = "Assets/Shell/Desktop/Taskbar/Modules_icon.png",
            master_image_path = "Assets/Shell/Desktop/Taskbar/Startbar.png",
            position = (37, 2)
        )
        self.Modules_startbar_button.bind("<Button-1>", lambda event: Map_programm(self.master))
        self.Modules_startbar_button.place(x=37, y=2)
        Logger.info("Modules icon loaded on startbar")

        # Search icon in startbar
        self.Search_startbar_button = Taskbar_button(
            self.Startbar,
            button_image_path = "Assets/Shell/Desktop/Taskbar/Search_icon.png",
            master_image_path = "Assets/Shell/Desktop/Taskbar/Startbar.png",
            position = (68, 2)
        )
        self.Search_startbar_button.bind("<Button-1>", lambda event: MessageBox(self.master, "This feature is not yet available", "Warning", True))
        self.Search_startbar_button.place(x=68, y=2)
        Logger.info("Search icon loaded on startbar")

# -------------------------------------------------------------[ Taskbar buttons ]-----------------------------------------------------------

        # Terminal icon in taskbar
        self.Terminal_taskbar_button = Taskbar_button(
            self.Taskbar,
            button_image_path = "Assets/Shell/Programs/Terminal/Terminal_icon.png",
            master_image_path = "Assets/Shell/Desktop/Taskbar/Taskbar.png",
            position = (109, 2)
        )
        self.Terminal_taskbar_button.bind("<Button-1>", lambda event: Terminal_programm(self.master))
        self.Terminal_taskbar_button.update_idletasks()
        Logger.info("Terminal icon loaded on taskbar")

        # File manager icon in taskbar
        self.File_manager_taskbar_button = Taskbar_button(
            self.Taskbar,
            button_image_path = "Assets/Shell/Programs/File manager/File_manager_icon.png",
            master_image_path = "Assets/Shell/Desktop/Taskbar/Taskbar.png",
            position = (109, 2)
        )
        self.File_manager_taskbar_button.bind("<Button-1>", lambda event: File_manager_programm(self.master))
        self.File_manager_taskbar_button.update_idletasks()
        Logger.info("File manager icon loaded on taskbar")

        # Shutdown icon in taskbar (replacing Browser icon)
        def shutdown_system():
            """Shutdown the system safely"""
            # Display a shutdown message
            shutdown_label = Label(
                self.master,
                text="Shutting down...",
                font=("Segoe UI", 14, "bold"),
                fg="#ffffff",
                bg="#3b67d6"
            )
            shutdown_label.place(relx=0.5, rely=0.5, anchor="center")
            # Schedule the actual exit after showing the message
            self.master.after(1500, self.master.destroy)
            
        self.Shutdown_taskbar_button = Taskbar_button(
            self.Taskbar,
            button_image_path = "Assets/Shell/Desktop/Taskbar/shutdown.png",
            master_image_path = "Assets/Shell/Desktop/Taskbar/Taskbar.png",
            position = (109, 2)
        )
        self.Shutdown_taskbar_button.bind("<Button-1>", lambda event: shutdown_system())
        self.Shutdown_taskbar_button.update_idletasks()
        Logger.info("Shutdown icon loaded on taskbar")

        # se crea una lista de los botones de la barra de tarea
        self.taskbar_buttons = [self.Terminal_taskbar_button, self.File_manager_taskbar_button, self.Shutdown_taskbar_button]

        # los botones se posicionan en la barra de tareas en el orden de la lista
        for i in range(len(self.taskbar_buttons)):
            self.taskbar_buttons[i].place(x=8 + (i * 32), y=2)
        Logger.info("Taskbar buttons loaded and placed")

        # self.master.after(2000, Welcome_dialog(self.master, False))

# -------------------------------------------------------------[ Clockbar ]-----------------------------------------------------------

        # Clock icon in clockbar
        def clock():
            Time = time.strftime("%I:%M %p")
            Date = time.strftime("%d/%m/%Y")

            ClockStr = ""
            ClockStr += Time
            ClockStr += "\n"
            ClockStr += Date

            self.Clock.config(text=ClockStr)
            self.Clock.after(200, clock)

        self.Clock = Label(
            self.Clockbar,
            width = 12,
            height = 2,
            borderwidth = "0",
            background = "#002C4F",
            foreground = "#F3F3F3",
            relief = "flat",
            font=("Segoe UI Semibold", 7),
            text = "",
        )
        self.Clock.place(x= 96, y= 0.5)
        clock()
        Logger.info("Clock component loaded")

        # Sound volume icon in clockbar
        self.Sound_button = Image.setImage("Assets/Shell/Desktop/Taskbar/high-volume.png", (24, 24), "#ff00ff", "#002C4F")
        self.Sound_button_light = Image.setImage("Assets/Shell/Desktop/Taskbar/high-volume.png", (24, 24), "#ff00ff", "#004C82")
        self.Sound_clockbar_button = Button(
            self.Clockbar,
            width = 16,
            height = 32,
            borderwidth="0",
            relief="flat",
            bg="#002C4F",
            activebackground = "#002C4F",
            image = self.Sound_button
        )
        
        def close_sound_popup(event=None):
            if self.sound_popup is not None and self.sound_popup.winfo_exists():
                self.sound_popup.destroy()
                self.sound_popup = None
                # Unbind the click event from the desktop
                self.master.unbind("<Button-1>")

        def on_desktop_click(event):
            # If popup exists and click is outside popup, close it
            if self.sound_popup is not None and self.sound_popup.winfo_exists():
                x, y = event.x_root, event.y_root
                px = self.sound_popup.winfo_rootx()
                py = self.sound_popup.winfo_rooty()
                pw = self.sound_popup.winfo_width()
                ph = self.sound_popup.winfo_height()
                if not (px <= x <= px+pw and py <= y <= py+ph):
                    close_sound_popup()

        def show_sound_control():
            # If already open, do nothing
            if self.sound_popup is not None and self.sound_popup.winfo_exists():
                return
            # Create popup window for volume control
            popup = Toplevel(self.master)
            self.sound_popup = popup
            popup.title("Volume Control")
            popup.geometry("250x200")
            popup.resizable(False, False)
            popup.configure(bg="#002C4F")
            
            # Add a close button in the top right
            close_btn = Button(
                popup, 
                text="×", 
                font=("Arial", 12, "bold"),
                bg="#002C4F",
                fg="#F3F3F3",
                activebackground="#004C82",
                activeforeground="#FFFFFF",
                relief="flat",
                borderwidth=0,
                command=close_sound_popup
            )
            close_btn.place(x=220, y=5)
            
            # Add a title
            title_label = Label(
                popup,
                text="Volume Control",
                bg="#002C4F",
                fg="#F3F3F3",
                font=("Segoe UI", 12, "bold")
            )
            title_label.place(x=20, y=15)
            
            # Add volume slider
            from tkinter import Scale, IntVar
            volume_var = IntVar()
            volume_var.set(50)  # Default volume level
            
            volume_slider = Scale(
                popup,
                from_=0,
                to=100,
                orient="horizontal",
                length=200,
                variable=volume_var,
                bg="#002C4F",
                fg="#F3F3F3",
                highlightthickness=0,
                troughcolor="#004C82",
                activebackground="#004C82"
            )
            volume_slider.place(x=25, y=60)
            
            # Current volume value display
            volume_label = Label(
                popup,
                text="Current Volume: 50%",
                bg="#002C4F",
                fg="#F3F3F3",
                font=("Segoe UI", 10)
            )
            volume_label.place(x=25, y=100)
            
            # Function to update the volume label
            def update_volume_label(event):
                volume_label.config(text=f"Current Volume: {volume_var.get()}%")
                
                # Update system volume if psutil is available
                if _HAS_PSUTIL:
                    try:
                        # This would be where actual system volume control happens
                        # Note: psutil doesn't actually handle audio, this is a placeholder
                        # In a real implementation, you would use a library like pycaw on Windows
                        # or similar libraries for other platforms
                        pass
                    except Exception:
                        pass
            
            volume_slider.bind("<Motion>", update_volume_label)
            
            # Add mute button
            mute_var = IntVar()
            mute_var.set(0)  # Default: not muted
            
            def toggle_mute():
                if mute_var.get() == 1:
                    # Muted state
                    mute_button.config(text="Unmute")
                    volume_slider.config(state="disabled")
                else:
                    # Unmuted state
                    mute_button.config(text="Mute")
                    volume_slider.config(state="normal")
            
            mute_button = Button(
                popup,
                text="Mute",
                font=("Segoe UI", 10),
                bg="#004C82",
                fg="#F3F3F3",
                activebackground="#006CB2",
                activeforeground="#FFFFFF",
                relief="flat",
                borderwidth=1,
                command=toggle_mute,
                variable=mute_var,
                indicatoron=0
            )
            mute_button.place(x=25, y=140)
            
            # Apply button
            apply_button = Button(
                popup,
                text="Apply",
                font=("Segoe UI", 10),
                bg="#004C82",
                fg="#F3F3F3",
                activebackground="#006CB2",
                activeforeground="#FFFFFF",
                relief="flat",
                borderwidth=1,
                command=popup.destroy
            )
            apply_button.place(x=150, y=140)
            
            # Make sure the popup stays on top
            popup.transient(self.master)
            popup.grab_set()
            
            # Center the popup on the screen
            popup.update_idletasks()
            width = popup.winfo_width()
            height = popup.winfo_height()
            x = (self.master.winfo_width() // 2) - (width // 2)
            y = (self.master.winfo_height() // 2) - (height // 2)
            popup.geometry(f"+{x}+{y}")
            # Bind click on desktop to close popup
            self.master.bind("<Button-1>", on_desktop_click)

            # When popup is closed by any means, cleanup
            def on_popup_close():
                close_sound_popup()
            popup.protocol("WM_DELETE_WINDOW", on_popup_close)

        self.Sound_clockbar_button.bind("<Button-1>", lambda event: show_sound_control())
        self.Sound_clockbar_button.bind("<Enter>", lambda event: self.Sound_clockbar_button.config(image = self.Sound_button_light))
        self.Sound_clockbar_button.bind("<Leave>", lambda event: self.Sound_clockbar_button.config(image = self.Sound_button))
        Logger.info("Sound volume icon loaded on clockbar")

        # Battery icon in clockbar
        self.Battery_button = Image.setImage("Assets/Shell/Desktop/Taskbar/high-battery.png", (24, 24), "#ff00ff", "#002C4F")
        self.Battery_button_light = Image.setImage("Assets/Shell/Desktop/Taskbar/high-battery.png", (24, 24), "#ff00ff", "#004C82")
        self.Battery_clockbar_button = Button(
            self.Clockbar,
            width = 16,
            height = 32,
            borderwidth="0",
            relief="flat",
            bg="#002C4F",
            activebackground = "#002C4F",
            image = self.Battery_button
        )

        def show_battery_status():
            # Try to get battery info using psutil
            if _HAS_PSUTIL:
                try:
                    battery = psutil.sensors_battery()
                    if battery is not None:
                        percent = battery.percent
                        plugged = battery.power_plugged
                        msg = f"Battery: {percent}%"
                        if plugged:
                            msg += " (Plugged in)"
                        create_battery_popup(msg)
                        return
                except Exception:
                    pass
            # Fallback: show random battery percentage
            percent = random.randint(20, 100)
            create_battery_popup(f"Battery: {percent}%")
            
        def create_battery_popup(message):
            popup = Toplevel(self.master)
            popup.title("Battery Status")
            popup.geometry("200x100")
            popup.resizable(False, False)
            popup.configure(bg="#002C4F")
            
            # Add a close button in the top right
            close_btn = Button(
                popup, 
                text="×", 
                font=("Arial", 12, "bold"),
                bg="#002C4F",
                fg="#F3F3F3",
                activebackground="#004C82",
                activeforeground="#FFFFFF",
                relief="flat",
                borderwidth=0,
                command=popup.destroy
            )
            close_btn.place(x=170, y=5)
            
            # Display the battery message
            msg_label = Label(
                popup,
                text=message,
                bg="#002C4F",
                fg="#F3F3F3",
                font=("Segoe UI", 10)
            )
            msg_label.place(x=20, y=40)
            
            # Make sure the popup stays on top
            popup.transient(self.master)
            popup.grab_set()
            
            # Center the popup on the screen
            popup.update_idletasks()
            width = popup.winfo_width()
            height = popup.winfo_height()
            x = (self.master.winfo_width() // 2) - (width // 2)
            y = (self.master.winfo_height() // 2) - (height // 2)
            popup.geometry(f"+{x}+{y}")

        self.Battery_clockbar_button.bind("<Button-1>", lambda event: show_battery_status())
        self.Battery_clockbar_button.bind("<Enter>", lambda event: self.Battery_clockbar_button.config(image = self.Battery_button_light))
        self.Battery_clockbar_button.bind("<Leave>", lambda event: self.Battery_clockbar_button.config(image = self.Battery_button))
        Logger.info("Battery icon loaded on clockbar")

        # Internet icon in clockbar
        self.Internet_button = Image.setImage("Assets/Shell/Desktop/Taskbar/high-internet.png", (24, 24), "#ff00ff", "#002C4F")
        self.Internet_button_light = Image.setImage("Assets/Shell/Desktop/Taskbar/high-internet.png", (24, 24), "#ff00ff", "#004C82")
        self.Internet_clockbar_button = Button(
            self.Clockbar,
            width = 16,
            height = 32,
            borderwidth="0",
            relief="flat",
            bg="#002C4F",
            activebackground = "#002C4F",
            image = self.Internet_button
        )
        
        def show_internet_status():
            # Instead of checking internet connection, just display a development message
            status_msg = "In development..."
            
            # Create popup window
            popup = Toplevel(self.master)
            popup.title("Internet Status")
            popup.geometry("200x100")
            popup.resizable(False, False)
            popup.configure(bg="#002C4F")
            
            # Add a close button in the top right
            close_btn = Button(
                popup, 
                text="×", 
                font=("Arial", 12, "bold"),
                bg="#002C4F",
                fg="#F3F3F3",
                activebackground="#004C82",
                activeforeground="#FFFFFF",
                relief="flat",
                borderwidth=0,
                command=popup.destroy
            )
            close_btn.place(x=170, y=5)
            
            # Display the development message
            msg_label = Label(
                popup,
                text=status_msg,
                bg="#002C4F",
                fg="#F3F3F3",
                font=("Segoe UI", 10)
            )
            msg_label.place(x=20, y=40)
            
            # Make sure the popup stays on top
            popup.transient(self.master)
            popup.grab_set()
            
            # Center the popup on the screen
            popup.update_idletasks()
            width = popup.winfo_width()
            height = popup.winfo_height()
            x = (self.master.winfo_width() // 2) - (width // 2)
            y = (self.master.winfo_height() // 2) - (height // 2)
            popup.geometry(f"+{x}+{y}")
        
        self.Internet_clockbar_button.bind("<Button-1>", lambda event: show_internet_status())
        self.Internet_clockbar_button.bind("<Enter>", lambda event: self.Internet_clockbar_button.config(image = self.Internet_button_light))
        self.Internet_clockbar_button.bind("<Leave>", lambda event: self.Internet_clockbar_button.config(image = self.Internet_button))
        Logger.info("Internet icon loaded on clockbar")

        # se crea una lista de los botones de la barra de tarea
        self.clockbar_buttons = [self.Battery_clockbar_button, self.Internet_clockbar_button, self.Sound_clockbar_button]

        # los botones se posicionan en la barra de tareas en el orden de la lista
        for i in range(len(self.clockbar_buttons)):
            self.clockbar_buttons[i].place(x=16 + (i * 24), y=-2)
        Logger.info("Clockbar buttons loaded and placed")

        # -------------------------------------------------------------[ Videos Folder ]-----------------------------------------------------------

        # Videos folder icon on desktop
        self.Videos_folder_image = Image.setImage("Assets/Shell/Icons/Folder_icon.png", (48, 48), "#ff00ff", "#001023")
        self.Videos_folder = Label(
            self.master,
            image=self.Videos_folder_image,
            borderwidth="0",
            relief="flat",
            bg="#001023"
        )
        self.Videos_folder.place(x=150, y=150)
        Logger.info("Videos folder icon loaded on desktop")

        # Bind click event to open Videos in file manager
        self.Videos_folder.bind("<Button-1>", lambda event: self.open_videos_folder())

        # Add "Videos" label under the folder icon
        self.Videos_folder_label = Label(
            self.master,
            text="Videos",
            font=("Segoe UI", 9),
            bg="#001023",
            fg="#FFFFFF"
        )
        self.Videos_folder_label.place(x=155, y=200)
        
        Logger.info("Videos folder icon added to desktop")
    
    def open_videos_folder(self):
        """Open the videos folder and display video files."""
        videos_path = "Assets/Videos"  # Path to the videos folder
        if not os.path.exists(videos_path):
            os.makedirs(videos_path)  # Create the folder if it doesn't exist

        # Create a popup window for the Videos folder
        popup = Toplevel(self.master)
        popup.title("Videos")
        popup.geometry("400x300")
        popup.resizable(False, False)
        popup.configure(bg="#002C4F")

        # Add a close button
        close_btn = Button(
            popup,
            text="×",
            font=("Arial", 12, "bold"),
            bg="#002C4F",
            fg="#F3F3F3",
            activebackground="#004C82",
            activeforeground="#FFFFFF",
            relief="flat",
            borderwidth=0,
            command=popup.destroy
        )
        close_btn.place(x=370, y=5)

        # Add a listbox to display video files
        video_listbox = Listbox(
            popup,
            bg="#001633",
            fg="#FFFFFF",
            font=("Consolas", 10),
            selectbackground="#004080",
            selectforeground="#FFFFFF",
            width=50,
            height=15
        )
        video_listbox.place(x=20, y=40)

        # Add a scrollbar for the listbox
        scrollbar = Scrollbar(popup, orient="vertical", command=video_listbox.yview)
        scrollbar.place(x=360, y=40, height=240)
        video_listbox.config(yscrollcommand=scrollbar.set)

        # Populate the listbox with video files
        video_files = [f for f in os.listdir(videos_path) if f.endswith(('.mp4', '.avi', '.mkv'))]
        for video in video_files:
            video_listbox.insert("end", video)

        # Define a function to play the selected video
        def play_video(event):
            selected_index = video_listbox.curselection()
            if selected_index:
                video_name = video_listbox.get(selected_index[0])
                video_path = os.path.join(videos_path, video_name)
                popup.destroy()  # Close the folder popup
                VideoPlayer(self.master, video_path)  # Open the video player

        # Bind double-click event to play the selected video
        video_listbox.bind("<Double-1>", play_video)

        Logger.info("Videos folder opened")
