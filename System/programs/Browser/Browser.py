from tkinter import Label, Entry, Button, StringVar, Frame
import tkinterweb
from Libs.pyImage.Image import Image

__author__ = 'TheBigEye'
__version__ = '1.2'

def Browser(master, *args):
    """
    Create and display the web browser with Google-like interface.

    Parameters:
    `master` : string
        The parent where the Browser will be placed.

    Returns:
    None
    """

# Browser UI setup ---------------------------------------------------------------------------------------------------------------

    global Browser, Browser_GUI_Image
    Browser_GUI_Image = Image.setImage("Assets/Shell/Programs/Browser/Browser.png")

    Browser = Label(
        master,
        bg="white",
        image=Browser_GUI_Image,
        borderwidth="0",
    )

    Browser.place(x=32, y=32)

    # Main frame for browser content
    browser_content = Frame(
        Browser,
        width=700,
        height=450,
        borderwidth=0,
        bg="white",
    )
    # Center browser_content in the Browser label
    browser_content.place(relx=0.5, rely=0.5, anchor="center")

    # Web content frame - placed in the center with Google loaded directly
    Page_frame = tkinterweb.HtmlFrame(browser_content, messages_enabled=False)
    Page_frame.load_website('https://google.com')
    # Center the web frame and make it fill the browser content area
    # Moved down 40 units from the center position
    Page_frame.place(relx=0.5, rely=0.5, y=40, anchor="center", width=700, height=450)
    
    # Function to handle search (kept for future reference)
    def search_web(query, frame):
        if not query:
            frame.load_website('https://google.com')
            return
            
        search_url = f'https://www.google.com/search?q={query}'
        frame.load_website(search_url)
