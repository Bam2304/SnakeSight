import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import ResultsPageOutPutData
import CSVReader
import os

from supabase import create_client, Client
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


# ===== Global styling constants =====
APP_BG = "#000000"        # dark base
APP_TEXT = "#FFFFFF"      # white text for contrast
BACKGROUND_FILE = "background.jpg"   # background image file


# ===== Custom flat button (black box) =====
class FlatButton(tk.Label):
    def __init__(self, master, text, command, **kwargs):
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
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda e: self.config(bg="#222222"))
        self.bind("<Leave>", lambda e: self.config(bg="#000000"))
        # Keyboard activation
        self.bind("<Return>", self._on_click)
        self.bind("<space>", self._on_click)
        self.configure(takefocus=True)

    def _on_click(self, event=None):
        if callable(self.command):
            self.command()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Snake Sight App")
        self.geometry("600x500")
        self.configure(background=APP_BG)

        # Luxury font settings
        self.base_font_size = 14
        self.font_family = "Didot"

        self._apply_global_font()

        # Visible focus outline
        self.option_add("*HighlightThickness", 2)
        self.option_add("*HighlightColor", APP_TEXT)

        # Zoom shortcuts
        self.bind_all("<Control-plus>", self._increase_font)
        self.bind_all("<Control-minus>", self._decrease_font)
        self.bind_all("<Control-0>", self._reset_font)

        # Menu bar
        self._create_menubar()

        # Store uploaded image globally
        self.sharedImage = None

        # Main container
        self.container = tk.Frame(self, bg=APP_BG, highlightthickness=0, bd=0)
        self.container.place(x=0, y=0, relwidth=1, relheight=1)

        # Pages
        self.frames = {}
        for F in (MainPage, SecondPage, InfoPage, ResultsPage):
            name = F.__name__
            frame = F(self.container, self)
            self.frames[name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Resize background when window resizes
        self.bind("<Configure>", self._on_resize)

        self.showFrame("MainPage")

    # ===== Global font & theme =====
    def _apply_global_font(self):
        font_spec = (self.font_family, self.base_font_size)
        self.option_add("*Font", font_spec)
        self.option_add("*Label.Font", font_spec)
        self.option_add("*Checkbutton.Font", font_spec)
        self.option_add("*Text.Font", font_spec)

        # Default dark + white
        self.option_add("*Background", APP_BG)
        self.option_add("*Foreground", APP_TEXT)
        self.option_add("*Checkbutton.Background", APP_BG)
        self.option_add("*Checkbutton.Foreground", APP_TEXT)

    def _increase_font(self, event=None):
        if self.base_font_size < 24:
            self.base_font_size += 2
            self._apply_global_font()

    def _decrease_font(self, event=None):
        if self.base_font_size > 8:
            self.base_font_size -= 2
            self._apply_global_font()

    def _reset_font(self, event=None):
        self.base_font_size = 14
        self._apply_global_font()

    def _create_menubar(self):
        menubar = tk.Menu(self)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Increase Text Size (Ctrl + +)", command=self._increase_font)
        view_menu.add_command(label="Decrease Text Size (Ctrl + -)", command=self._decrease_font)
        view_menu.add_command(label="Reset Text Size (Ctrl + 0)", command=self._reset_font)
        menubar.add_cascade(label="View", menu=view_menu)

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

    def showFrame(self, name):
        frame = self.frames[name]
        frame.updatePage()
        frame.tkraise()

    # Called whenever window is resized
    def _on_resize(self, event):
        if event.widget is self:
            width, height = event.width, event.height
            for frame in self.frames.values():
                if hasattr(frame, "resize_background"):
                    frame.resize_background(width, height)


# ===================== COMMON MIXIN FOR BACKGROUND =======================

class BackgroundMixin:
    def _init_background(self):
        # Load original image once per frame
        self._bg_original = Image.open(BACKGROUND_FILE)
        self._bg_img = ImageTk.PhotoImage(self._bg_original.resize((600, 500)))
        self._bg_label = tk.Label(self, image=self._bg_img, borderwidth=0, highlightthickness=0)
        self._bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def resize_background(self, width, height):
        # Avoid zero-size errors
        if width < 1 or height < 1:
            return
        resized = self._bg_original.resize((width, height))
        self._bg_img = ImageTk.PhotoImage(resized)
        self._bg_label.configure(image=self._bg_img)
        self._bg_label.image = self._bg_img


# ===================== MAIN PAGE =======================

class MainPage(BackgroundMixin, tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=APP_BG)
        self.controller = controller

        # Background
        self._init_background()

        # Title
        heading = tk.Label(
            self,
            text="Welcome to SnakeSight",
            font=(controller.font_family, 24, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        )
        heading.place(x=150, y=60)

        # Snake image
        snakeImage = Image.open("snakeSightIm.jpg").resize((175, 175))
        self.snakePhoto = ImageTk.PhotoImage(snakeImage)
        tk.Label(self, image=self.snakePhoto, bg=APP_BG, bd=0, highlightthickness=0).place(x=40, y=140)

        # Image description (moved down so it doesn't collide with button)
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

        # Upload button (FlatButton)
        FlatButton(
            self,
            text="Upload Image (optional)",
            command=self.uploadImage
        ).place(x=270, y=160)

        # Next button (FlatButton)
        FlatButton(
            self,
            text="Go to Q&A Page",
            command=lambda: controller.showFrame("SecondPage")
        ).place(x=270, y=320)

        # Disclaimer button (FlatButton)
        FlatButton(
            self,
            text="Disclaimer / Safety Info",
            command=lambda: controller.showFrame("InfoPage")
        ).place(x=18, y=10)

    def uploadImage(self):
        
        bucket = supabase.storage.from_("Modelimages")
        bucket.remove("blackrat2.jpg")

        filePath = filedialog.askopenfilename(
            title="Choose a snake photo",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )

        

        if filePath:
            try:
                # Display locally
                tempImg = Image.open(filePath)
                self.controller.sharedImage = ImageTk.PhotoImage(tempImg)

                # Read image bytes for upload
                with open(filePath, "rb") as f:
                    file_bytes = f.read()

                # Forced filename
                
                # 1. Delete old file (ignore errors if it doesn't exist)
                
                file_name = "blackrat2.jpg"

                # 2. Upload new file
                result = bucket.upload(
                    path=file_name,
                    file=file_bytes,
                    file_options={"content-type": "image/jpeg"}
                )

                print("Uploaded:", result)
                self.statusLabel.config(text="Uploaded and replaced blackrat2.jpg")

            except Exception as e:
                print("Error:", e)
                self.statusLabel.config(text="Upload failed")


    def updatePage(self):
        if self.controller.sharedImage:
            self.statusLabel.config(text="Image submitted. You can continue to the Q&A.")
        else:
            self.statusLabel.config(text="No image selected yet.")


# ===================== SECOND PAGE =======================

class SecondPage(BackgroundMixin, tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=APP_BG)
        self.controller = controller

        # Background
        self._init_background()

        # Q&A heading
        tk.Label(
            self,
            text="Q&A",
            font=(controller.font_family, 20, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=275, y=10)

        instructions = tk.Label(
            self,
            text="Answer as many questions as you can.\nUse Tab / Shift+Tab to move; Space to toggle options.",
            bg=APP_BG,
            fg=APP_TEXT,
            justify="left"
        )
        instructions.place(x=20, y=55)

        # Back button (FlatButton)
        FlatButton(
            self,
            text="Back to Main Page",
            command=lambda: controller.showFrame("MainPage")
        ).place(x=18, y=10)

        # Get results button (FlatButton)
        FlatButton(
            self,
            text="Get Your Results!",
            command=self.showResults
        ).place(x=430, y=10)

        tk.Label(
            self,
            text="What Did The Snake Look Like? (Can Select Multiple)",
            font=(controller.font_family, 16, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=20, y=120)

        # ===== Checkbox Variables =====
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

        # Checkboxes – spaced so nothing overlaps
        tk.Checkbutton(self, text="Brown", variable=self.brownBox, **cb_kwargs).place(x=20, y=170)
        tk.Checkbutton(self, text="Black", variable=self.blackBox, **cb_kwargs).place(x=20, y=200)
        tk.Checkbutton(self, text="White", variable=self.whiteBox, **cb_kwargs).place(x=20, y=230)
        tk.Checkbutton(self, text="Yellow", variable=self.yellowBox, **cb_kwargs).place(x=20, y=260)
        tk.Checkbutton(self, text="Green", variable=self.greenBox, **cb_kwargs).place(x=20, y=290)
        tk.Checkbutton(self, text="Red", variable=self.redBox, **cb_kwargs).place(x=20, y=320)
        tk.Checkbutton(self, text="Orange", variable=self.orangeBox, **cb_kwargs).place(x=20, y=350)
        tk.Checkbutton(self, text="3 or More Colors", variable=self.threeOrMoreBox, **cb_kwargs).place(x=20, y=380)

        tk.Checkbutton(self, text="> 36 In.", variable=self.greaterThan36, **cb_kwargs).place(x=200, y=170)
        tk.Checkbutton(self, text="Checker Pattern", variable=self.checker, **cb_kwargs).place(x=200, y=200)
        tk.Checkbutton(self, text="Length Stripes", variable=self.length, **cb_kwargs).place(x=200, y=230)
        tk.Checkbutton(self, text="Width Stripes", variable=self.width, **cb_kwargs).place(x=200, y=260)
        tk.Checkbutton(self, text="Less Than 12 Inches", variable=self.lessThan12, **cb_kwargs).place(x=200, y=290)
        tk.Checkbutton(self, text="Between 12 and 24 Inches", variable=self.between12And24, **cb_kwargs).place(x=200, y=320)
        tk.Checkbutton(self, text="Between 24 and 36 Inches", variable=self.between24And36, **cb_kwargs).place(x=200, y=350)

        tk.Checkbutton(self, text="Flat Head", variable=self.flatHead, **cb_kwargs).place(x=400, y=380)

        tk.Checkbutton(self, text="Round Head", variable=self.roundHead, **cb_kwargs).place(x=400, y=170)
        tk.Checkbutton(self, text="Rattle", variable=self.rattle, **cb_kwargs).place(x=400, y=200)
        tk.Checkbutton(self, text="Dark Spots", variable=self.darkSpots, **cb_kwargs).place(x=400, y=230)
        tk.Checkbutton(self, text="Light Spots", variable=self.lightSpots, **cb_kwargs).place(x=400, y=260)

    def updatePage(self):
        pass

    def showResults(self):
        controller = self.controller
        resultsPage = controller.frames["ResultsPage"]
        qnaResults = []

        # Append answer codes
        if self.brownBox.get(): qnaResults.append(1)
        if self.blackBox.get(): qnaResults.append(2)
        if self.whiteBox.get(): qnaResults.append(3)
        if self.yellowBox.get(): qnaResults.append(4)
        if self.orangeBox.get(): qnaResults.append(5)
        if self.redBox.get(): qnaResults.append(6)
        if self.greenBox.get(): qnaResults.append(7)
        if self.threeOrMoreBox.get(): qnaResults.append(8)

        if self.checker.get(): qnaResults.append(21)
        if self.greaterThan36.get(): qnaResults.append(15)
        if self.length.get(): qnaResults.append(22)
        if self.width.get(): qnaResults.append(23)

        if self.lessThan12.get(): qnaResults.append(12)
        if self.between12And24.get(): qnaResults.append(13)
        if self.between24And36.get(): qnaResults.append(14)

        if self.flatHead.get(): qnaResults.append(16)
        if self.roundHead.get(): qnaResults.append(17)

        if self.rattle.get(): qnaResults.append(18)
        if self.darkSpots.get(): qnaResults.append(19)
        if self.lightSpots.get(): qnaResults.append(20)


        #instantiate CSVReader and get results
        OUTPUTResult = CSVReader.Reader().testQuestionaire(qnaResults)
        opd = ResultsPageOutPutData.OutPutData()
        OUTPUTResultOutput = opd.GetFormattedSnakeInfo(OUTPUTResult)
        final_text = "\n".join(OUTPUTResultOutput)

        resultsPage.addInfo(final_text)
        controller.showFrame("ResultsPage")


# ===================== INFO PAGE =======================

class InfoPage(BackgroundMixin, tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=APP_BG)

        # Background
        self._init_background()

        # Heading moved down so it doesn't collide with Back button
        tk.Label(
            self,
            text="Important Safety Disclaimer",
            font=(controller.font_family, 20, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=130, y=50)

        # Back button (FlatButton)
        FlatButton(
            self,
            text="Back to Main Page",
            command=lambda: controller.showFrame("MainPage")
        ).place(x=18, y=10)

        disclaimer = (
            "Snake Sight is an educational aid only. It does not replace professional\n"
            "medical or wildlife advice. If you are bitten or feel unsafe at any time,\n"
            "call emergency services immediately.\n\n"
            "Do not approach or attempt to capture any snake. Keep a safe distance."
        )

        tk.Label(
            self,
            text=disclaimer,
            bg=APP_BG,
            fg=APP_TEXT,
            justify="left"
        ).place(x=20, y=110)

    def updatePage(self):
        pass


# ===================== RESULTS PAGE =======================

class ResultsPage(BackgroundMixin, tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=APP_BG)
        self.controller = controller

        # Background
        self._init_background()

        tk.Label(
            self,
            text="Your Results",
            font=(controller.font_family, 20, "bold"),
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=220, y=10)

        # Back to Q&A button (FlatButton)
        FlatButton(
            self,
            text="Back to Q&A",
            command=lambda: controller.showFrame("SecondPage")
        ).place(x=18, y=10)

        tk.Label(
            self,
            text="Analysis summary:",
            bg=APP_BG,
            fg=APP_TEXT
        ).place(x=20, y=60)

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

    def addInfo(self, text):
        self.outputTextArea.delete("1.0", tk.END)
        self.outputTextArea.insert(tk.END, text)
        self.outputTextArea.see(tk.END)

    def updatePage(self):
        pass


# ===================== RUN APP =======================

if __name__ == "__main__":
    app = App()
    app.mainloop()
