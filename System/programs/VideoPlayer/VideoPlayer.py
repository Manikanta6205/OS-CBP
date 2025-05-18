from tkinter import Button, Frame, Label, Toplevel, Scale, ttk, HORIZONTAL, VERTICAL, IntVar
from Libs.pyLogger.Logger import Logger
import subprocess
import os
import platform
import time
import threading
import sys

__author__ = 'TheBigEye'
__version__ = '2.0'

class VideoPlayer(Frame):
    """
    Video Player class - Embedded video player with controls
    """
    def __init__(self, master, video_path):
        """
        Video Player constructor
        """
        Frame.__init__(self, master)
        self.master = master
        self.video_path = video_path
        
        # Set VLC availability flag to False by default
        self.has_vlc = False
        
        try:
            # Only try importing VLC if we're not in a try/except block already
            if 'vlc' not in sys.modules:
                try:
                    import vlc
                    self.has_vlc = True
                except (ImportError, FileNotFoundError, OSError) as e:
                    Logger.warning(f"VLC library not available: {str(e)}")
                    self.has_vlc = False
            else:
                self.has_vlc = True
        except:
            # Catch-all for any other errors
            self.has_vlc = False
            Logger.warning("VLC library not found. Using system player as fallback.")
        
        if self.has_vlc:
            try:
                self.create_vlc_player()
            except Exception as e:
                Logger.error(f"Failed to create VLC player: {str(e)}")
                self.has_vlc = False
                self.create_system_player_prompt()
        else:
            # Skip the prompt and directly play with the system player
            # This is a more reliable approach when VLC is not available
            self.play_with_system_player()
    
    def play_with_system_player(self):
        """Play the video with the system's default video player directly"""
        try:
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
            self.show_error_message(f"Failed to play video: {str(e)}")
    
    def show_error_message(self, message):
        """Show an error message to the user"""
        popup = Toplevel(self.master)
        popup.title("Error Playing Video")
        popup.geometry("400x150")
        popup.resizable(False, False)
        popup.configure(bg="#002C4F")
        
        error_label = Label(
            popup,
            text=message,
            bg="#002C4F",
            fg="#FF5555",
            font=("Segoe UI", 10),
            wraplength=350
        )
        error_label.pack(pady=20)
        
        close_btn = Button(
            popup,
            text="Close",
            bg="#800000",
            fg="#FFFFFF",
            activebackground="#A00000",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10),
            command=popup.destroy
        )
        close_btn.pack(pady=10)
        
        # Center the window
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (self.master.winfo_width() // 2) - (width // 2)
        y = (self.master.winfo_height() // 2) - (height // 2)
        popup.geometry(f"+{x}+{y}")

    def create_vlc_player(self):
        # Import VLC here to avoid errors if it's not installed
        import vlc
        
        # Create main window
        self.window = Toplevel(self.master)
        self.window.title("Video Player")
        self.window.geometry("800x600")
        self.window.configure(bg="#001023")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Get video filename
        video_name = os.path.basename(self.video_path)
        self.window.title(f"Video Player - {video_name}")
        
        # Create frame for VLC player
        self.video_frame = Frame(self.window, bg="black", width=780, height=440)
        self.video_frame.pack(pady=10)
        self.video_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Create control variables
        self.is_playing = False
        self.volume = IntVar()
        self.volume.set(70)  # Default volume 70%
        
        # Initialize VLC instance and media player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(self.video_path)
        self.player.set_media(self.media)
        
        # Set video output window
        if platform.system() == "Windows":
            self.player.set_hwnd(self.video_frame.winfo_id())
        elif platform.system() == "Darwin":  # macOS
            self.player.set_nsobject(self.video_frame.winfo_id())
        else:  # Linux
            self.player.set_xwindow(self.video_frame.winfo_id())
        
        # Create controls frame
        self.controls_frame = Frame(self.window, bg="#002C4F", height=100)
        self.controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Create progress bar
        self.progress_var = IntVar()
        self.progress_bar = Scale(
            self.controls_frame,
            from_=0,
            to=1000,
            orient=HORIZONTAL,
            variable=self.progress_var,
            showvalue=False,
            sliderrelief="flat",
            bg="#002C4F",
            fg="#FFFFFF",
            troughcolor="#004080",
            activebackground="#0060A0",
            highlightthickness=0,
            length=760,
            command=self.seek
        )
        self.progress_bar.pack(pady=10)
        
        # Time display
        self.time_label = Label(
            self.controls_frame,
            text="00:00 / 00:00",
            bg="#002C4F",
            fg="#FFFFFF",
            font=("Segoe UI", 9)
        )
        self.time_label.pack(pady=5)
        
        # Buttons frame
        self.buttons_frame = Frame(self.controls_frame, bg="#002C4F")
        self.buttons_frame.pack(fill="x", padx=10, pady=5)
        
        # Play/Pause button
        self.play_button = Button(
            self.buttons_frame,
            text="▶",
            width=3,
            bg="#004080",
            fg="#FFFFFF",
            activebackground="#0060A0",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 12),
            command=self.toggle_play
        )
        self.play_button.pack(side="left", padx=10)
        
        # Rewind button
        self.rewind_button = Button(
            self.buttons_frame,
            text="⏪",
            width=3,
            bg="#004080",
            fg="#FFFFFF",
            activebackground="#0060A0",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 12),
            command=lambda: self.skip(-10)  # Skip back 10 seconds
        )
        self.rewind_button.pack(side="left", padx=5)
        
        # Forward button
        self.forward_button = Button(
            self.buttons_frame,
            text="⏩",
            width=3,
            bg="#004080",
            fg="#FFFFFF",
            activebackground="#0060A0",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 12),
            command=lambda: self.skip(10)  # Skip forward 10 seconds
        )
        self.forward_button.pack(side="left", padx=5)
        
        # Volume control
        self.volume_label = Label(
            self.buttons_frame,
            text="Volume:",
            bg="#002C4F",
            fg="#FFFFFF",
            font=("Segoe UI", 9)
        )
        self.volume_label.pack(side="left", padx=(20, 5))
        
        self.volume_scale = Scale(
            self.buttons_frame,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            variable=self.volume,
            bg="#002C4F",
            fg="#FFFFFF",
            troughcolor="#004080",
            activebackground="#0060A0",
            highlightthickness=0,
            length=100,
            command=self.set_volume
        )
        self.volume_scale.pack(side="left")
        
        # Set initial volume
        self.player.audio_set_volume(70)
        
        # Start update timer
        self.is_user_dragging = False
        self.update_thread = threading.Thread(target=self.update_timer)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        # Start playing the video
        self.toggle_play()
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.master.winfo_width() // 2) - (width // 2)
        y = (self.master.winfo_height() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")
        
        Logger.info(f"Playing video in embedded player: {self.video_path}")
    
    def create_system_player_prompt(self):
        """Create a prompt to use the system player since VLC is not available"""
        # Create a popup to confirm playing the video
        popup = Toplevel(self.master)
        popup.title("Play Video")
        popup.geometry("400x200")
        popup.resizable(False, False)
        popup.configure(bg="#002C4F")
        
        # Add the video name as a label
        video_name = os.path.basename(self.video_path)
        name_label = Label(
            popup,
            text=f"Selected video: {video_name}",
            bg="#002C4F",
            fg="#F3F3F3",
            font=("Segoe UI", 10)
        )
        name_label.place(x=20, y=40)
        
        # Add message about VLC not being available
        vlc_label = Label(
            popup,
            text="VLC library is not available on this system.\nWould you like to use the system player instead?",
            bg="#002C4F",
            fg="#F3F3F3",
            font=("Segoe UI", 10),
            justify="left"
        )
        vlc_label.place(x=20, y=70)
        
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
        play_btn.place(x=20, y=130)
        
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
        close_btn.place(x=200, y=130)
        
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
        # Close the popup
        popup.destroy()
        
        # Use the play_with_system_player method
        self.play_with_system_player()
    
    def toggle_play(self):
        """Toggle between play and pause"""
        if not self.has_vlc:
            return
            
        if self.is_playing:
            self.player.pause()
            self.play_button.config(text="▶")
            self.is_playing = False
        else:
            self.player.play()
            self.play_button.config(text="⏸")
            self.is_playing = True
    
    def seek(self, value):
        """Seek to position in video"""
        if not self.has_vlc:
            return
            
        # Only seek if not being called from the update timer
        if not self.is_user_dragging:
            self.is_user_dragging = True
            position = int(float(value)) / 1000.0
            self.player.set_position(position)
            
            # Release the dragging flag after a short delay
            self.master.after(100, self.release_drag_flag)
    
    def release_drag_flag(self):
        """Release the user dragging flag"""
        self.is_user_dragging = False
    
    def skip(self, seconds):
        """Skip forward or backward by specified seconds"""
        if not self.has_vlc:
            return
            
        current_time = self.player.get_time()
        new_time = current_time + (seconds * 1000)  # VLC uses milliseconds
        
        # Ensure new time is within bounds
        if new_time < 0:
            new_time = 0
        elif self.player.get_length() > 0 and new_time > self.player.get_length():
            new_time = self.player.get_length()
            
        self.player.set_time(new_time)
    
    def set_volume(self, value):
        """Set the volume level"""
        if not self.has_vlc:
            return
            
        volume = int(float(value))
        self.player.audio_set_volume(volume)
    
    def update_timer(self):
        """Update the progress bar and time display"""
        while self.has_vlc:
            try:
                if hasattr(self, 'window') and not self.window.winfo_exists():
                    break
                    
                if self.is_playing and not self.is_user_dragging and self.player.get_length() > 0:
                    # Update progress bar
                    position = int(self.player.get_position() * 1000)
                    self.progress_var.set(position)
                    
                    # Update time display
                    current = self.player.get_time() // 1000  # Convert to seconds
                    total = self.player.get_length() // 1000  # Convert to seconds
                    
                    current_min, current_sec = divmod(current, 60)
                    total_min, total_sec = divmod(total, 60)
                    
                    time_str = f"{current_min:02d}:{current_sec:02d} / {total_min:02d}:{total_sec:02d}"
                    
                    # Schedule the update on the main thread
                    if hasattr(self, 'time_label') and self.time_label.winfo_exists():
                        self.master.after_idle(lambda: self.time_label.config(text=time_str))
                
                # Sleep to avoid high CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                Logger.error(f"Error updating player: {e}")
                time.sleep(1)  # Wait longer on error
    
    def on_closing(self):
        """Handle window closing"""
        if self.has_vlc:
            # Stop the player
            self.player.stop()
            # Close the window
            self.window.destroy()
