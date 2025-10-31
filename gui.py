import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
#pip install import-ipynb
#import import_ipynb #allows importing of notebook files, should not need if using just .py files
import ResultsPageOutPutData

OUTPUTResult = {1:10.0, 2:9.0 , 3:8.0 , 4:7.0 , 5:6.0}#remove when integrating with actual results page
OUTPUTResultOutput = ResultsPageOutPutData.GetFormattedSnakeInfo(OUTPUTResult) #List[Dict{}]


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
        self.configure(background='orange')
        
        tk.Label(self, text="Welcome to Snake Sight", font=("Arial", 18)).place(x=220, y=10)

        # Status label (not the image itself)
        self.statusLabel = tk.Label(self, text="No image submitted")
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
            # Load & store image (not displayed)
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
        self.configure(background='orange')

        tk.Label(self, text="Q&A", font=("Arial", 18)).place(x=275, y=10)

        # Back button
        backButton = tk.Button(
            self, text="Back to Main Page",
            command=lambda: controller.showFrame("MainPage")
        )
        #back_btn.pack(pady=250, padx=20)
        backButton.place(x=18, y=10)

        #Get results button
        resultsButton = tk.Button(
            self, text="Get Your Results!",
            command=self.showResults
        )
        resultsButton.place(x=425, y=10)

        #label for selecting colors
        tk.Label(self, text="What Color Was The Snake? (Can Select Multiple Colors)", 
                 font=("Arial", 14)).place(x=20, y=70)

        #variables to hold states of checkboxes
        self.brownBox = tk.IntVar()
        self.blackBox = tk.IntVar()
        self.whiteBox = tk.IntVar()
        self.yellowBox = tk.IntVar()
        self.greenBox = tk.IntVar()
        self.redBox = tk.IntVar()
        self.orangeBox = tk.IntVar()
        self.threeOrMoreBox = tk.IntVar()

        #creating the checkboxes for selecting snake color
        tk.Checkbutton(self, text="Brown", variable=self.brownBox).place(x=20, y=120)
        tk.Checkbutton(self, text="Black", variable=self.blackBox).place(x=20, y=150)
        tk.Checkbutton(self, text="White", variable=self.whiteBox).place(x=20, y=180)
        tk.Checkbutton(self, text="Yellow", variable=self.yellowBox).place(x=20, y=210)
        tk.Checkbutton(self, text="Green", variable=self.greenBox).place(x=20, y=240)
        tk.Checkbutton(self, text="Red", variable=self.redBox).place(x=20, y=270)
        tk.Checkbutton(self, text="Orange", variable=self.orangeBox).place(x=20, y=300)
        tk.Checkbutton(self, text="3 or More Colors", variable=self.threeOrMoreBox).place(x=20, y=330)

    def updatePage(self):
        """Optional refresh when shown."""
        pass

    def showResults(self):
        """This method will take the calculations for best snake match
        and ouput the results to the Results Page"""

        controller = self.controller
        resultsPage = controller.frames["ResultsPage"]
        qnaResults = []
        if self.brownBox: #if the checkbox is clicked, append the corresponding score
            qnaResults.append(1)
        if self.blackBox:
            qnaResults.append(2)
        if self.whiteBox:
            qnaResults.append(3)
        if self.yellowBox:
            qnaResults.append(4)
        if self.orangeBox:
            qnaResults.append(5)
        if self.redBox:
            qnaResults.append(6)
        if self.greenBox:
            qnaResults.append(7)
        if self.threeOrMoreBox:
            qnaResults.append(8)
        #def ChangeIntoSeprateInfo(ResultInput)
        # Example of text from some external source
        #"\n".join(ResultOutput)

        resultText = "\n".join(OUTPUTResultOutput)
        # (
        #     "Analysis Complete!\n\n"
        #     "Snake Type: Eastern Diamondback Rattlesnake\n"
        #     "Venom Severity: High\n"
        #     "Recommended Action: Seek immediate medical attention.\n\n"
        #     "Additional Info:\n"
        #     "The Eastern Diamondback is the largest venomous snake in North America."
            
        # )

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
        self.configure(background='blue')

        tk.Label(self, text="Disclaimer", font=("Arial", 18)).place(x=245, y=10)
        
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
        self.configure(background='gray')

         
        tk.Label(self, text="Your Results:", font=("Arial", 18)).place(x=225, y=10)
        
        
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
    app = App()
    app.mainloop()
