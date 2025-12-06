"""
gui.py
This module defines the SnakeSight application's graphical user interface.
It provides multiple navigable pages, accessibility features, and integration
with Supabase for image uploading.

Coding Standards Applied:
- Clear docstrings for all classes and methods
- Type hints on all public methods
- 4-space indentation (as chosen)
- 80-character line wrapping
- Descriptive variable names
- Logical grouping of methods
- Separation of concerns across classes
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

import ResultsPageOutPutData
import CSVReader

from supabase import create_client, Client


# ======================================================================
#  Supabase Initialization 
# ======================================================================

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


# ======================================================================
#  Global Styling Constants
# ======================================================================

APP_BG: str = "#000000"
APP_TEXT: str = "#FFFFFF"
BACKGROUND_FILE: str = "background.jpg"


# ======================================================================
#  FlatButton – Custom Clickable Label Styled as a Button
# ======================================================================

class FlatButton(tk.Label):
    """
    A custom flat-styled clickable label used as a button throughout the
    application. The widget supports keyboard activation, hover feedback,
    and accessibility focus behavior.
    """

    def __init__(
        self,
        master: tk.Widget,
        text: str,
        command,
        **kwargs
    ) -> None:
        """
        Initialize the FlatButton widget.

        Args:
            master: Parent container widget.
            text: Text displayed inside the button.
            command: Callable executed when activated.
            **kwargs: Additional styling keyword arguments.
        """
        super().__init__(
            master,
            text=text,
            bg="#000000",
            fg="#FFFFFF",
            padx=10,
            pady=4,
            cursor="hand2",
            **kwargs
        )

        self.command = command

        # Mouse activation
        self.bind("<Button-1>", self._on_click)

        # Hover styling
        self.bind("<Enter>", lambda e: self.config(bg="#222222"))
        self.bind("<Leave>", lambda e: self.config(bg="#000000"))

        # Keyboard activation
        self.bind("<Return>", self._on_click)
        self.bind("<space>", self._on_click)

        # Focusable for keyboard users
        self.configure(takefocus=True)

    # ------------------------------------------------------------------

    def _on_click(self, event=None) -> None:
        """
        Trigger the assigned command when the widget is clicked or activated
        via keyboard.
        """
        if callable(self.command):
            self.command()


# ======================================================================
#  App – Main Application Window and Navigation Controller
# ======================================================================

class App(tk.Tk):
    """
    The main application root window. This class manages global theming,
    accessibility features, window resizing behavior, and navigation between
    individual pages (MainPage, SecondPage, InfoPage, ResultsPage).
    """

    def __init__(self) -> None:
        """Initialize the application window and top-level configuration."""
        super().__init__()

        self.title("Snake Sight App")
        self.geometry("600x500")
        self.configure(background=APP_BG)

        # Font configuration
        self.base_font_size: int = 14
        self.font_family: str = "Didot"

        self._apply_global_font()

        # Keyboard focus highlighting
        self.option_add("*HighlightThickness", 2)
        self.option_add("*HighlightColor", APP_TEXT)

        # Text zoom shortcuts
        self.bind_all("<Control-plus>", self._increase_font)
        self.bind_all("<Control-minus>", self._decrease_font)
        self.bind_all("<Control-0>", self._reset_font)

        # Menu bar
        self._create_menubar()

        # Shared image reference
        self.sharedImage = None

        # Page container
        self.container = tk.Frame(
            self,
            bg=APP_BG,
            highlightthickness=0,
            bd=0
        )
        self.container.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        # Load all pages
        self.frames: dict[str, tk.Frame] = {}

        for PageClass in (MainPage, SecondPage, InfoPage, ResultsPage):
            name = PageClass.__name__
            frame = PageClass(self.container, self)
            self.frames[name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Monitor window resizing
        self.bind("<Configure>", self._on_resize)

        # Show main menu
        self.showFrame("MainPage")

    # ------------------------------------------------------------------

    def _apply_global_font(self) -> None:
        """
        Apply global font settings to all common widgets to ensure consistent,
        accessible typography across the interface.
        """
        font_spec = (self.font_family, self.base_font_size)

        self.option_add("*Font", font_spec)
        self.option_add("*Label.Font", font_spec)
        self.option_add("*Checkbutton.Font", font_spec)
        self.option_add("*Text.Font", font_spec)

        self.option_add("*Background", APP_BG)
        self.option_add("*Foreground", APP_TEXT)

        self.option_add("*Checkbutton.Background", APP_BG)
        self.option_add("*Checkbutton.Foreground", APP_TEXT)

    # ------------------------------------------------------------------

    def _increase_font(self, event=None) -> None:
        """
        Increase the font size globally, improving readability for visually
        impaired users.
        """
        if self.base_font_size < 24:
            self.base_font_size += 2
            self._apply_global_font()

    # ------------------------------------------------------------------

    def _decrease_font(self, event=None) -> None:
        """
        Decrease the global font size within an allowed range.
        """
        if self.base_font_size > 8:
            self.base_font_size -= 2
            self._apply_global_font()

    # ------------------------------------------------------------------

    def _reset_font(self, event=None) -> None:
        """
        Reset the global font size to the default base value.
        """
        self.base_font_size = 14
        self._apply_global_font()

    # ------------------------------------------------------------------

    def _create_menubar(self) -> None:
        """
        Create the accessible menu bar containing view options and
        keyboard shortcuts help.
        """
        menubar = tk.Menu(self)

        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(
            label="Increase Text Size (Ctrl + +)",
            command=self._increase_font
        )
        view_menu.add_command(
            label="Decrease Text Size (Ctrl + -)",
            command=self._decrease_font
        )
        view_menu.add_command(
            label="Reset Text Size (Ctrl + 0)",
            command=self._reset_font
        )
        menubar.add_cascade(label="View", menu=view_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="Keyboard Help",
            command=lambda: messagebox.showinfo(
                "Keyboard Help",
                "Tab / Shift+Tab: Move between controls\n"
                "Space / Enter: Activate control\n"
                "Ctrl + Plus/Minus/0: Adjust text size"
            )
        )
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    # ------------------------------------------------------------------

    def showFrame(self, name: str) -> None:
        """
        Raise the specified page to the front.

        Args:
            name: Name of the frame class as a string.
        """
        frame = self.frames[name]
        frame.updatePage()
        frame.tkraise()

    # ------------------------------------------------------------------

    def _on_resize(self, event) -> None:
        """
        Trigger background resizing on all pages when the main window
        dimensions change.
        """
        if event.widget is self:
            width, height = event.width, event.height

            for frame in self.frames.values():
                if hasattr(frame, "resize_background"):
                    frame.resize_background(width, height)


# ======================================================================
#  BackgroundMixin – Provides Resizable Page Background Image
# ======================================================================

class BackgroundMixin:
    """
    A mixin providing shared functionality for rendering and resizing
    the page background image.
    """

    def _init_background(self) -> None:
        """Load and initialize the background image."""
        self._bg_original = Image.open(BACKGROUND_FILE)
        self._bg_img = ImageTk.PhotoImage(
            self._bg_original.resize((600, 500))
        )

        self._bg_label = tk.Label(
            self,
            image=self._bg_img,
            borderwidth=0,
            highlightthickness=0
        )

        self._bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ------------------------------------------------------------------

    def resize_background(self, width: int, height: int) -> None:
        """
        Resize the background dynamically when the window changes size.

        Args:
            width: New window width.
            height: New window height.
        """
        if width < 1 or height < 1:
            return

        resized = self._bg_original.resize((width, height))
        self._bg_img = ImageTk.PhotoImage(resized)

        self._bg_label.configure(image=self._bg_img)
        self._bg_label.image = self._bg_img


# ======================================================================
#  MainPage – Landing Page UI
# ======================================================================

class MainPage(BackgroundMixin, tk.Frame):
    """
    The main landing page of the application. This page allows the user
    to upload an optional snake image, navigate to the Q&A section, or
    read the safety disclaimer.
    """

    def __init__(
        self,
        parent: tk.Widget,
        controller: App
    ) -> None:
        """Initialize the MainPage UI layout."""
        tk.Frame.__init__(self, parent, bg=APP_BG)
        self.controller = controller

        # Background
        self._init_background()

        # Heading
        heading = tk.Label(
            self,
            text="Welcome to SnakeSight",
            font=(controller.font_family, 24, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        )
        heading.place(x=150, y=60)

        # Snake illustration
        snake_image = Image.open("snakeSightIm.jpg").resize((175, 175))
        self.snakePhoto = ImageTk.PhotoImage(snake_image)

        tk.Label(
            self,
            image=self.snakePhoto,
            bg=APP_BG,
            bd=0,
            highlightthickness=0
        ).place(x=40, y=140)

        # Image description (accessibility)
        tk.Label(
            self,
            text="Illustration of a friendly cartoon snake.",
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=40, y=360)

        # Status label
        self.statusLabel = tk.Label(
            self,
            text="No image selected yet.",
            bg=APP_BG,
            fg=APP_TEXT
        )
        self.statusLabel.place(x=270, y=120)

        # Upload button
        FlatButton(
            self,
            text="Upload Image (optional)",
            command=self.uploadImage
        ).place(x=270, y=160)

        # Navigation buttons
        FlatButton(
            self,
            text="Go to Q&A Page",
            command=lambda: controller.showFrame("SecondPage")
        ).place(x=270, y=320)

        FlatButton(
            self,
            text="Disclaimer / Safety Info",
            command=lambda: controller.showFrame("InfoPage")
        ).place(x=18, y=10)

    # ------------------------------------------------------------------

    def uploadImage(self) -> None:
        """
        Upload an image file, display it locally, and push it to Supabase
        storage. The Supabase code was intentionally left unchanged per
        user request.
        """
        bucket = supabase.storage.from_("Modelimages")

        # User-required unchanged behavior
        response = supabase.storage.from_("Modelimages").remove(
            "blackrat2.jpg"
        )

        filePath = filedialog.askopenfilename(
            title="Choose a snake photo",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif")
            ]
        )

        if filePath:
            try:
                # Display image locally
                tempImg = Image.open(filePath)
                self.controller.sharedImage = ImageTk.PhotoImage(tempImg)

                # Read as bytes for upload
                with open(filePath, "rb") as f:
                    file_bytes = f.read()

                file_name = "snk.jpg"

                # Upload new file
                bucket.upload(
                    path=file_name,
                    file=file_bytes,
                    file_options={"content-type": "image/jpeg"}
                )

                supabase.storage.from_("Modelimages").upload(
                    file_name,
                    file_bytes,
                    {"upsert": "true"}
                )

                self.statusLabel.config(
                    text="Uploaded and replaced blackrat2.jpg"
                )

            except Exception as exc:
                self.statusLabel.config(text="Upload failed")
                print("Error:", exc)

    # ------------------------------------------------------------------

    def updatePage(self) -> None:
        """Refresh status label when returning to this page."""
        if self.controller.sharedImage:
            self.statusLabel.config(
                text="Image submitted. You can continue to the Q&A."
            )
        else:
            self.statusLabel.config(text="No image selected yet.")
# ======================================================================
#  SecondPage – Q&A User Input Page
# ======================================================================

class SecondPage(BackgroundMixin, tk.Frame):
    """
    The Q&A page that collects user input describing the snake's appearance.
    Inputs are later processed into a results lookup.
    """

    def __init__(
        self,
        parent: tk.Widget,
        controller: App
    ) -> None:
        """Initialize the Q&A layout and checkboxes."""
        tk.Frame.__init__(self, parent, bg=APP_BG)
        self.controller = controller

        # Background
        self._init_background()

        # Heading
        tk.Label(
            self,
            text="Q&A",
            font=(controller.font_family, 20, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=275, y=10)

        # Instructions
        instructions = tk.Label(
            self,
            text=(
                "Answer as many questions as you can.\n"
                "Use Tab / Shift+Tab to move; Space to toggle options."
            ),
            bg=APP_BG,
            fg=APP_TEXT,
            justify="left"
        )
        instructions.place(x=20, y=55)

        # Navigation buttons
        FlatButton(
            self,
            text="Back to Main Page",
            command=lambda: controller.showFrame("MainPage")
        ).place(x=18, y=10)

        FlatButton(
            self,
            text="Get Your Results!",
            command=self.showResults
        ).place(x=430, y=10)

        # Section label
        tk.Label(
            self,
            text="What Did The Snake Look Like? (Can Select Multiple)",
            font=(controller.font_family, 16, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=20, y=120)

        # Variables for checkboxes
        self.brownBox = tk.IntVar()
        self.blackBox = tk.IntVar()
        self.whiteBox = tk.IntVar()
        self.yellowBox = tk.IntVar()
        self.greenBox = tk.IntVar()
        self.redBox = tk.IntVar()
        self.orangeBox = tk.IntVar()
        self.threeOrMoreBox = tk.IntVar()

        self.greaterThan36 = tk.IntVar()
        self.checker = tk.IntVar()
        self.length = tk.IntVar()
        self.width = tk.IntVar()

        self.lessThan12 = tk.IntVar()
        self.between12And24 = tk.IntVar()
        self.between24And36 = tk.IntVar()

        self.flatHead = tk.IntVar()
        self.roundHead = tk.IntVar()

        self.rattle = tk.IntVar()
        self.darkSpots = tk.IntVar()
        self.lightSpots = tk.IntVar()

        cb_kwargs = {
            "bg": APP_BG,
            "fg": APP_TEXT,
            "activebackground": APP_BG,
            "activeforeground": APP_TEXT,
            "selectcolor": "#202020",
            "bd": 0,
            "highlightthickness": 0
        }

        # Organized checkbox placement
        tk.Checkbutton(
            self, text="Brown", variable=self.brownBox, **cb_kwargs
        ).place(x=20, y=170)
        tk.Checkbutton(
            self, text="Black", variable=self.blackBox, **cb_kwargs
        ).place(x=20, y=200)
        tk.Checkbutton(
            self, text="White", variable=self.whiteBox, **cb_kwargs
        ).place(x=20, y=230)
        tk.Checkbutton(
            self, text="Yellow", variable=self.yellowBox, **cb_kwargs
        ).place(x=20, y=260)
        tk.Checkbutton(
            self, text="Green", variable=self.greenBox, **cb_kwargs
        ).place(x=20, y=290)
        tk.Checkbutton(
            self, text="Red", variable=self.redBox, **cb_kwargs
        ).place(x=20, y=320)
        tk.Checkbutton(
            self, text="Orange", variable=self.orangeBox, **cb_kwargs
        ).place(x=20, y=350)
        tk.Checkbutton(
            self, text="3 or More Colors", variable=self.threeOrMoreBox,
            **cb_kwargs
        ).place(x=20, y=380)

        tk.Checkbutton(
            self, text="> 36 In.", variable=self.greaterThan36,
            **cb_kwargs
        ).place(x=200, y=170)
        tk.Checkbutton(
            self, text="Checker Pattern", variable=self.checker,
            **cb_kwargs
        ).place(x=200, y=200)
        tk.Checkbutton(
            self, text="Length Stripes", variable=self.length,
            **cb_kwargs
        ).place(x=200, y=230)
        tk.Checkbutton(
            self, text="Width Stripes", variable=self.width,
            **cb_kwargs
        ).place(x=200, y=260)
        tk.Checkbutton(
            self, text="Less Than 12 Inches", variable=self.lessThan12,
            **cb_kwargs
        ).place(x=200, y=290)
        tk.Checkbutton(
            self, text="Between 12 and 24 Inches",
            variable=self.between12And24,
            **cb_kwargs
        ).place(x=200, y=320)
        tk.Checkbutton(
            self, text="Between 24 and 36 Inches",
            variable=self.between24And36,
            **cb_kwargs
        ).place(x=200, y=350)

        tk.Checkbutton(
            self, text="Flat Head", variable=self.flatHead,
            **cb_kwargs
        ).place(x=400, y=380)

        tk.Checkbutton(
            self, text="Round Head", variable=self.roundHead,
            **cb_kwargs
        ).place(x=400, y=170)
        tk.Checkbutton(
            self, text="Rattle", variable=self.rattle,
            **cb_kwargs
        ).place(x=400, y=200)
        tk.Checkbutton(
            self, text="Dark Spots", variable=self.darkSpots,
            **cb_kwargs
        ).place(x=400, y=230)
        tk.Checkbutton(
            self, text="Light Spots", variable=self.lightSpots,
            **cb_kwargs
        ).place(x=400, y=260)

    # ------------------------------------------------------------------

    def updatePage(self) -> None:
        """No dynamic updates required for this page."""
        pass

    # ------------------------------------------------------------------

    def showResults(self) -> None:
        """
        Collect the user's checkbox selections, compute the matching
        snake species, and display the results page.
        """
        controller = self.controller
        resultsPage = controller.frames["ResultsPage"]
        selections: list[int] = []

        # Colors & patterns
        mapping = [
            (self.brownBox, 1), (self.blackBox, 2),
            (self.whiteBox, 3), (self.yellowBox, 4),
            (self.orangeBox, 5), (self.redBox, 6),
            (self.greenBox, 7), (self.threeOrMoreBox, 8),
            (self.checker, 21), (self.greaterThan36, 15),
            (self.length, 22), (self.width, 23),
            (self.lessThan12, 12), (self.between12And24, 13),
            (self.between24And36, 14), (self.flatHead, 16),
            (self.roundHead, 17), (self.rattle, 18),
            (self.darkSpots, 19), (self.lightSpots, 20)
        ]

        for var, code in mapping:
            if var.get():
                selections.append(code)

        # Call to CSVReader (OOP style)
        reader = CSVReader.Reader()
        result_raw = reader.testQuestionaire(selections)

        opd = ResultsPageOutPutData.OutPutData()
        formatted = opd.GetFormattedSnakeInfo(result_raw)

        final_text = "\n".join(formatted)

        resultsPage.addInfo(final_text)
        controller.showFrame("ResultsPage")


# ======================================================================
#  InfoPage – Safety Disclaimer
# ======================================================================

class InfoPage(BackgroundMixin, tk.Frame):
    """
    Displays the safety disclaimer and warnings for users.
    """

    def __init__(
        self,
        parent: tk.Widget,
        controller: App
    ) -> None:
        """Initialize the InfoPage UI."""
        tk.Frame.__init__(self, parent, bg=APP_BG)
        self.controller = controller

        # Background
        self._init_background()

        # Heading
        tk.Label(
            self,
            text="Important Safety Disclaimer",
            font=(controller.font_family, 20, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=130, y=50)

        # Back button
        FlatButton(
            self,
            text="Back to Main Page",
            command=lambda: controller.showFrame("MainPage")
        ).place(x=18, y=10)

        # Disclaimer text
        disclaimer = (
            "Snake Sight is an educational aid only. It does not replace "
            "professional\nmedical or wildlife advice. If you are bitten or feel "
            "unsafe at any time,\ncall emergency services immediately.\n\n"
            "Do not approach or attempt to capture any snake. Keep a safe "
            "distance."
        )

        tk.Label(
            self,
            text=disclaimer,
            bg=APP_BG,
            fg=APP_TEXT,
            justify="left"
        ).place(x=20, y=110)

    # ------------------------------------------------------------------

    def updatePage(self) -> None:
        """No dynamic update required."""
        pass


# ======================================================================
#  ResultsPage – Display Species Results
# ======================================================================

class ResultsPage(BackgroundMixin, tk.Frame):
    """
    Displays the final interpreted snake results to the user after Q&A
    submission and data processing.
    """

    def __init__(
        self,
        parent: tk.Widget,
        controller: App
    ) -> None:
        """Initialize the ResultsPage UI."""
        tk.Frame.__init__(self, parent, bg=APP_BG)
        self.controller = controller

        # Background
        self._init_background()

        # Heading
        tk.Label(
            self,
            text="Your Results",
            font=(controller.font_family, 20, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=220, y=10)

        # Back navigation
        FlatButton(
            self,
            text="Back to Q&A",
            command=lambda: controller.showFrame("SecondPage")
        ).place(x=18, y=10)

        # Subheading
        tk.Label(
            self,
            text="Analysis summary:",
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=20, y=60)

        # Scrollable output text box
        self.outputTextArea = tk.Text(
            self,
            wrap="word",
            height=14,
            width=65,
            bg=APP_BG,
            fg=APP_TEXT,
            insertbackground=APP_TEXT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#303030"
        )
        self.outputTextArea.place(x=20, y=95)

        scrollbar = tk.Scrollbar(self, command=self.outputTextArea.yview)
        scrollbar.place(x=560, y=95, height=230)
        self.outputTextArea.config(yscrollcommand=scrollbar.set)

    # ------------------------------------------------------------------

    def addInfo(self, text: str) -> None:
        """
        Insert newly formatted result text into the scrollable display box.

        Args:
            text: Final results string.
        """
        self.outputTextArea.delete("1.0", tk.END)
        self.outputTextArea.insert(tk.END, text)
        self.outputTextArea.see(tk.END)

    # ------------------------------------------------------------------

    def updatePage(self) -> None:
        """No dynamic update required."""
        pass


# ======================================================================
#  MAIN EXECUTION
# ======================================================================

if __name__ == "__main__":
    app = App()
    app.mainloop()
