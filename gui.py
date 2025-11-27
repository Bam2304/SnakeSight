import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
#pip install import-ipynb
#import import_ipynb #allows importing of notebook files, should not need if using just .py files
import ResultsPageOutPutData
import CSVReader



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
        self.configure(background="#6AB187")
        
        tk.Label(self, text="Welcome to Snake Sight!", font=("Arial", 23), 
                 background="#20948B").place(x=193, y=10)
        
        # Image to look a little nicer
        # credit: https://stock.adobe.com/search?k=%22funny+snake%22
        snakeImage = Image.open("snakeSightIm.jpg")  
        snakeImage = snakeImage.resize((175, 175))
        self.snakePhoto = ImageTk.PhotoImage(snakeImage)
        tk.Label(self, image=self.snakePhoto).place(x=30, y=140)



        # Status label (not the image itself)
        self.statusLabel = tk.Label(self, text="No Image", background="#20948B")
        self.statusLabel.place(x=250, y=100)

        # Upload button
        uploadButton = tk.Button(self, text="Upload Image", command=self.uploadImage)
        uploadButton.place(x=250, y=130)

        # Forward button
        nextButton = tk.Button(
            self, text="Go to Q&A Page",
            command=lambda: controller.showFrame("SecondPage")
        )
        nextButton.place(x=245, y=300)

        #Disclaimer button
        infoButton = tk.Button(
            self, text="DISCLAIMER!",
            command=lambda: controller.showFrame("InfoPage")
        )
        infoButton.place(x=18, y=10)

    def uploadImage(self):
        """Upload an image for potential photo recognition"""
        filePath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if filePath:
            # Load & store image 
            tempImg = Image.open(filePath)
            try:
                self.controller.sharedImage = ImageTk.PhotoImage(tempImg)
                self.statusLabel.config(text="Image submitted ✅")
            except Exception: #ImageTk could throw error opening file
                self.statusLabel.config(text="Error opening file. " \
                "Please choose another file.")

    def updatePage(self):
        """Refresh page when shown."""
        if self.controller.sharedImage:
            self.statusLabel.config(text="Image submitted ✅")
        else:
            self.statusLabel.config(text="No image submitted")


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

        #instantiate CSVReader and get results
        OUTPUTResult = CSVReader.Reader().testQuestionaire(qnaResults)
        opd = ResultsPageOutPutData.OutPutData()
        OUTPUTResultOutput = opd.GetFormattedSnakeInfo(OUTPUTResult) 

        

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
        self.configure(background='red')

        tk.Label(self, text="Disclaimer!", font=("Arial", 18)).place(x=245, y=10)
        
        #disclaimer message for info page
        disclaimerMessage = "Warning: This app is for demonstration purposes only. " \
        "Advice given here is to be taken with a grain of salt, and does not replace " \
        "the advice of actual medical professionals."
        disclaimerSpace = tk.Message(self, text=disclaimerMessage, width=300, 
                                      font=("Arial", 22), justify="center")
        disclaimerSpace.place(x=150, y=125)

        # Back button
        backButton = tk.Button(
            self, text="Back to Main Page",
            command=lambda: controller.showFrame("MainPage")
        )
        #back_btn.pack(pady=250, padx=20)
        backButton.place(x=425, y=10)

    def updatePage(self):
        """Optional refresh when shown."""
        pass

class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background="#6AB187")

         
        tk.Label(self, text="Your Results:", font=("Arial", 22), 
                 background="#20948B").place(x=225, y=15)
        
        # Back button
        backButton = tk.Button(
            self, text="Back to Q&A Page",
            command=lambda: controller.showFrame("SecondPage")
        )
        
        backButton.place(x=18, y=10)
        
        #text area for the output text
        self.outputTextArea = tk.Text(
             self, 
             wrap="word",        
             height=12,
             width=40, 
             font=("Arial", 17)
         )
        self.outputTextArea.place(x=80, y=90)
         


    def addInfo(self, text):
        """Adds info to the text area on the Results Page"""
        self.outputTextArea.insert(tk.END, text)
        self.outputTextArea.see(tk.END)
        
    def updatePage(self):
        """Optional refresh when shown."""
        pass

if __name__ == "__main__":
    app = App()  # instantiate and run the app
    app.mainloop()
