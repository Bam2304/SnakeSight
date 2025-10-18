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
        self.shared_image = None

        # Container for frames
        self.container = tk.Frame(self, width=600, height=400)
        self.container.place(x=0, y=0, width=600, height=400)
        

        self.frames = {}
        for F in (MainPage, SecondPage, InfoPage, ResultsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)  # makes each frame fill the window
            

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        """Raise the frame to the front."""
        frame = self.frames[page_name]
        frame.update_page()  # let the page refresh its content
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background='orange')
        
        tk.Label(self, text="Welcome to Snake Sight", font=("Arial", 18)).place(x=220, y=10)

        # Status label (not the image itself)
        self.status_label = tk.Label(self, text="No image submitted")
        self.status_label.place(x=250, y=100)

        # Upload button
        upload_btn = tk.Button(self, text="Upload Image", command=self.upload_image)
        upload_btn.place(x=250, y=130)

        # Forward button
        next_btn = tk.Button(
            self, text="Go to Q&A Page",
            command=lambda: controller.show_frame("SecondPage")
        )
        next_btn.place(x=245, y=300)

        #Disclaimer button
        info_btn = tk.Button(
            self, text="DISCLAIMER!",
            command=lambda: controller.show_frame("InfoPage")
        )
        info_btn.place(x=18, y=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if file_path:
            # Load & store image (not displayed)
            img = Image.open(file_path)
            self.controller.shared_image = ImageTk.PhotoImage(img)
            self.status_label.config(text="Image submitted ✅")

    def update_page(self):
        """Refresh page when shown."""
        if self.controller.shared_image:
            self.status_label.config(text="Image submitted ✅")
        else:
            self.status_label.config(text="No image submitted")


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        
        super().__init__(parent)
        self.controller = controller
        self.configure(background='orange')

        tk.Label(self, text="Q&A", font=("Arial", 18)).place(x=275, y=10)

        # Back button
        back_btn = tk.Button(
            self, text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        #back_btn.pack(pady=250, padx=20)
        back_btn.place(x=18, y=10)

        #Get results button
        results_btn = tk.Button(
            self, text="Get Your Results!",
            command=self.showResults
        )
        results_btn.place(x=425, y=10)

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

    def update_page(self):
        """Optional refresh when shown."""
        pass

    def showResults(self):
        controller = self.controller
        results_page = controller.frames["ResultsPage"]
        qnaResults = []
        if self.brownBox:
            qnaResults.append(1)
        if self.blackBox:
            qnaResults.append(2)
        if self.whiteBoxBox:
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

        result_text = "\n".join(OUTPUTResultOutput)
        # (
        #     "Analysis Complete!\n\n"
        #     "Snake Type: Eastern Diamondback Rattlesnake\n"
        #     "Venom Severity: High\n"
        #     "Recommended Action: Seek immediate medical attention.\n\n"
        #     "Additional Info:\n"
        #     "The Eastern Diamondback is the largest venomous snake in North America."
            
        # )

        # Add text to ResultsPage
        results_page.text_area.delete("1.0", tk.END)  # clear old text 
        
        results_page.add_info(result_text)

        # Switch to the ResultsPage
        controller.show_frame("ResultsPage")

class InfoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background='blue')

        tk.Label(self, text="Disclaimer", font=("Arial", 18)).place(x=245, y=10)
        
        #disclaimer message for info page
        message = "Warning: This app is for demonstration purposes only. " \
        "Advice given here is to be taken with a grain of salt, and does not replace " \
        "the advice of actual medical professionals."
        disclaimer_space = tk.Message(self, text=message, width=300, font=("Arial", 22), justify="center")
        disclaimer_space.place(x=150, y=125)

        # Back button
        back_btn = tk.Button(
            self, text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        #back_btn.pack(pady=250, padx=20)
        back_btn.place(x=425, y=10)
    def update_page(self):
        """Optional refresh when shown."""
        pass

class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background='gray')

         
        tk.Label(self, text="Your Results:", font=("Arial", 18)).place(x=225, y=10)
        
        
        #text area for the output text
        self.text_area = tk.Text(
             self, 
             wrap="word",        # wraps text at word boundaries
             height=12,
             width=40,
             #yscrollcommand=scrollbar.set, 
             font=("Arial", 17)
         )
        self.text_area.place(x=80, y=90)
         


    def add_info(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        
    def update_page(self):
        """Optional refresh when shown."""
        pass

    def add_info(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()
