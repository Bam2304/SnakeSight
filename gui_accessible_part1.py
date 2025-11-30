import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
#pip install import-ipynb
#import import_ipynb #allows importing of notebook files, should not need if using just .py files
import ResultsPageOutPutData
import CSVReader


# Partial accessibility / styling constants
APP_BG = "#FFFFFF"          # light, high-contrast background
APP_ACCENT = "#004C4C"      # darker teal accent for better contrast
APP_TEXT = "#000000"        # black text




class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Snake Sight App")
        self.geometry("600x400")
        

        # Store uploaded image (shared across pages)
        self.sharedImage = None

        # Container for frames
        self.container = tk.Frame(self, width=600, height=400)
        self.container.place(x=0, y=0, width=600, height=400)
        

        self.frames = {}
        for F in (MainPage, SecondPage, InfoPage, ResultsPage):
            pageName = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[pageName] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)  # makes each frame fill the window
            

        self.showFrame("MainPage")

    def showFrame(self, page_name):
        """Raise the frame to the front."""
        frame = self.frames[page_name]
        frame.updatePage()  # let the page refresh its content
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background=APP_BG)

        heading = tk.Label(
            self,
            text="Welcome to Snake Sight",
            font=("Arial", 23, "bold"),
            background=APP_ACCENT,
            foreground=APP_TEXT
        )
        heading.place(x=150, y=10)

        # Snake illustration (decorative)
        snakeImage = Image.open("snakeSightIm.jpg")
        snakeImage = snakeImage.resize((175, 175))
        self.snakePhoto = ImageTk.PhotoImage(snakeImage)
        img_label = tk.Label(self, image=self.snakePhoto, background=APP_BG)
        img_label.place(x=30, y=140)

        # Text description of image for users who can't see it
        img_desc = tk.Label(
            self,
            text="Illustration of a friendly cartoon snake.",
            background=APP_BG,
            foreground=APP_TEXT,
            justify="left"
        )
        img_desc.place(x=30, y=320)

        # Status label for uploaded photo
        self.statusLabel = tk.Label(
            self,
            text="No image selected yet.",
            background=APP_BG,
            foreground=APP_TEXT
        )
        self.statusLabel.place(x=250, y=100)

        # Upload button
        uploadButton = tk.Button(
            self,
            text="Upload Image (optional)",
            command=self.uploadImage
        )
        uploadButton.place(x=250, y=130)

        # Forward button
        nextButton = tk.Button(
            self,
            text="Go to Q&A Page",
            command=lambda: controller.showFrame("SecondPage")
        )
        nextButton.place(x=245, y=300)

        # Disclaimer button
        infoButton = tk.Button(
            self,
            text="Disclaimer / Safety Info",
            command=lambda: controller.showFrame("InfoPage")
        )
        infoButton.place(x=18, y=10)

    def uploadImage(self):
        """Upload an image for potential photo recognition."""
        filePath = filedialog.askopenfilename(
            title="Choose a snake photo",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if filePath:
            try:
                tempImg = Image.open(filePath)
                self.controller.sharedImage = ImageTk.PhotoImage(tempImg)
                self.statusLabel.config(text="Image submitted. You can continue to the Q&A.")
            except Exception:
                self.statusLabel.config(text="Error opening that file. Please try a different image.")
                messagebox.showerror(
                    "Image error",
                    "We couldn't open that image file. Please choose another image in PNG, JPG, or GIF format."
                )

    def updatePage(self):
        """Refresh page when shown."""
        if self.controller.sharedImage:
            self.statusLabel.config(text="Image submitted. You can continue to the Q&A.")
        else:
            self.statusLabel.config(text="No image selected yet.")
class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        
        super().__init__(parent)
        self.controller = controller
        self.configure(background="#6AB187")

        tk.Label(self, text="Q&A", font=("Arial", 18), 
                 background="#20948B").place(x=275, y=10)

        # Back button
        backButton = tk.Button(
            self, text="Back to Main Page",
            command=lambda: controller.showFrame("MainPage")
        )
        
        backButton.place(x=18, y=10)

        #Get results button
        resultsButton = tk.Button(
            self, text="Get Your Results!",
            command=self.showResults
        )
        resultsButton.place(x=425, y=10)

        #label for selecting colors
        tk.Label(self, text="What Did The Snake Look Like? (Can Select Multiple)", 
                 font=("Arial", 17), background="#20948B").place(x=20, y=70)

        #variables to hold states of checkboxes
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

        #creating the checkboxes for selecting snake color
        tk.Checkbutton(self, text="Brown", variable=self.brownBox).place(x=20, y=120)
        tk.Checkbutton(self, text="Black", variable=self.blackBox).place(x=20, y=150)
        tk.Checkbutton(self, text="White", variable=self.whiteBox).place(x=20, y=180)
        tk.Checkbutton(self, text="Yellow", variable=self.yellowBox).place(x=20, y=210)
        tk.Checkbutton(self, text="Green", variable=self.greenBox).place(x=20, y=240)
        tk.Checkbutton(self, text="Red", variable=self.redBox).place(x=20, y=270)
        tk.Checkbutton(self, text="Orange", variable=self.orangeBox).place(x=20, y=300)
        tk.Checkbutton(self, text="3 or More Colors", 
                       variable=self.threeOrMoreBox).place(x=20, y=330)

        tk.Checkbutton(self, text="> 36 In.", variable=self.greaterThan36).place(x=100, y=120)
        tk.Checkbutton(self, text="Checker Pattern", variable=self.checker).place(x=100, y=150)
        tk.Checkbutton(self, text="Length Stripes", variable=self.length).place(x=100, y=180)
        tk.Checkbutton(self, text="Width Stripes", variable=self.width).place(x=100, y=210)
        tk.Checkbutton(self, text="Less Than 12 Inches", variable=self.lessThan12).place(x=100, y=240)
        tk.Checkbutton(self, text="Between 12 and 24 Inches", variable=self.between12And24).place(x=100, y=270)
        tk.Checkbutton(self, text="Between 24 and 36 Inches", variable=self.between24And36).place(x=100, y=300)
        tk.Checkbutton(self, text="Flat Head", variable=self.flatHead).place(x=240, y=330)

        tk.Checkbutton(self, text="Round Head", variable=self.roundHead).place(x=240, y=120)
        tk.Checkbutton(self, text="Rattle", variable=self.rattle).place(x=240, y=150)
        tk.Checkbutton(self, text="Dark Spots", variable=self.darkSpots).place(x=240, y=180)
        tk.Checkbutton(self, text="Light Spots", variable=self.lightSpots).place(x=240, y=210)

    def updatePage(self):
        """Optional refresh when shown."""
        pass

    def showResults(self):
        """This method will take the calculations for best snake match
        and ouput the results to the Results Page"""

        controller = self.controller
        resultsPage = controller.frames["ResultsPage"]
        qnaResults = []

        if self.brownBox.get(): #if the checkbox is clicked, append the corresponding score
            qnaResults.append(1)
        if self.blackBox.get():
            qnaResults.append(2)
        if self.whiteBox.get():
            qnaResults.append(3)
        if self.yellowBox.get():
            qnaResults.append(4)
        if self.orangeBox.get():
            qnaResults.append(5)
        if self.redBox.get():
            qnaResults.append(6)
        if self.greenBox.get():
            qnaResults.append(7)
        if self.threeOrMoreBox.get():
            qnaResults.append(8)
        if self.checker.get():
            qnaResults.append(21)
        if self.greaterThan36.get():
            qnaResults.append(15)
        if self.length.get():
            qnaResults.append(22)
        if self.width.get():
            qnaResults.append(23)
        if self.lessThan12.get():
            qnaResults.append(12)
        if self.between12And24.get():
            qnaResults.append(13)
        if self.between24And36.get():
            qnaResults.append(14)
        if self.flatHead.get():
            qnaResults.append(16)
        if self.roundHead.get():
            qnaResults.append(17)
        if self.rattle.get():
            qnaResults.append(18)
        if self.darkSpots.get():
            qnaResults.append(19)
        if self.lightSpots.get():
            qnaResults.append(20)

        OUTPUTResult = CSVReader.testQuestionaire(qnaResults)
        OUTPUTResultOutput = ResultsPageOutPutData.GetFormattedSnakeInfo(OUTPUTResult) 

        

        resultText = "\n".join(OUTPUTResultOutput)
        
        # Add text to ResultsPage
        resultsPage.outputTextArea.delete("1.0", tk.END)  # clear old text 
        
        if type(resultText) != str:
            resultText = "The type of result is not string. Error."
        
        resultsPage.addInfo(resultText)

        # Switch to the ResultsPage
        controller.showFrame("ResultsPage")

class InfoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background=APP_BG)

        heading = tk.Label(
            self,
            text="Important Safety Disclaimer",
            font=("Arial", 18, "bold"),
            background=APP_ACCENT,
            foreground=APP_TEXT
        )
        heading.place(x=150, y=10)

        # Back button
        backButton = tk.Button(
            self,
            text="Back to Main Page",
            command=lambda: controller.showFrame("MainPage")
        )
        backButton.place(x=18, y=10)

        # Disclaimer body text
        body_text = (
            "Snake Sight is an educational aid only. It does not replace professional\n"
            "medical or wildlife advice. If you are bitten or feel unsafe at any time,\n"
            "call emergency services immediately and follow local guidance.\n\n"
            "Do not approach, touch, or attempt to capture any snake based on what\n"
            "this app shows. When in doubt, keep a safe distance."
        )

        disclaimer_label = tk.Label(
            self,
            text=body_text,
            background=APP_BG,
            foreground=APP_TEXT,
            justify="left"
        )
        disclaimer_label.place(x=20, y=80)

    def updatePage(self):
        """Optional refresh when shown."""
        pass
class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background=APP_BG)

        heading = tk.Label(
            self,
            text="Your Results",
            font=("Arial", 18, "bold"),
            background=APP_ACCENT,
            foreground=APP_TEXT
        )
        heading.place(x=220, y=10)

        # Back button
        backButton = tk.Button(
            self,
            text="Back to Q&A Page",
            command=lambda: controller.showFrame("SecondPage")
        )
        backButton.place(x=18, y=10)

        # Label for the results area
        results_label = tk.Label(
            self,
            text="Analysis summary:",
            background=APP_BG,
            foreground=APP_TEXT
        )
        results_label.place(x=20, y=60)

        # Scrollable text area for output
        self.outputTextArea = tk.Text(self, wrap="word", height=14, width=65)
        self.outputTextArea.place(x=20, y=90)

        scrollbar = tk.Scrollbar(self, command=self.outputTextArea.yview)
        scrollbar.place(x=560, y=90, height=230)
        self.outputTextArea.config(yscrollcommand=scrollbar.set)

    def addInfo(self, text):
        """Adds info to the text area on the Results Page"""
        self.outputTextArea.delete("1.0", tk.END)
        self.outputTextArea.insert(tk.END, text)
        self.outputTextArea.see(tk.END)

    def updatePage(self):
        """Optional refresh when shown."""
        pass


if __name__ == "__main__":
    app = App()  # instantiate and run the app
    app.mainloop()
