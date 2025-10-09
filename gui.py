import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Snake Sight App")
        self.geometry("600x400")
        

        # Store uploaded image (shared across pages)
        self.shared_image = None

        # Container for frames
        self.container = tk.Frame(self, width=600, height=400)
        self.container.pack(fill="both", expand=True)
        self.container.pack_propagate(False)

        self.frames = {}
        for F in (MainPage, SecondPage, InfoPage, ResultsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

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
        
        tk.Label(self, text="Welcome to Snake Sight", font=("Arial", 18)).pack(pady=20, padx=(0,75), anchor="center")

        # Status label (not the image itself)
        self.status_label = tk.Label(self, text="No image submitted")
        self.status_label.pack(pady=10, padx=(0,75), anchor="center")

        # Upload button
        upload_btn = tk.Button(self, text="Upload Image", command=self.upload_image)
        upload_btn.pack(pady=30, padx=(0,75), anchor="center")

        # Forward button
        next_btn = tk.Button(
            self, text="Go to Second Page",
            command=lambda: controller.show_frame("SecondPage")
        )
        next_btn.pack(pady=40, padx=(0,75), anchor="center")

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

        tk.Label(self, text="Q&A", font=("Arial", 18)).pack(pady=10, padx=(0,85))

        # Back button
        back_btn = tk.Button(
            self, text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        #back_btn.pack(pady=250, padx=20)
        back_btn.place(x=18, y=10)

        #Get results button
        results_btn = tk.Button(
            self, text="Get Your Results",
            command=self.showResults
        )
        results_btn.place(x=425, y=10)
    def update_page(self):
        """Optional refresh when shown."""
        pass

    def showResults(self):
        controller = self.controller
        results_page = controller.frames["ResultsPage"]

        # Example of text from some external source
        result_text = (
            "Analysis Complete!\n\n"
            "Snake Type: Eastern Diamondback Rattlesnake\n"
            "Venom Severity: High\n"
            "Recommended Action: Seek immediate medical attention.\n\n"
            "Additional Info:\n"
            "The Eastern Diamondback is the largest venomous snake in North America."
        )

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

        tk.Label(self, text="Disclaimer", font=("Arial", 18)).pack(pady=10, padx=(0,85))
        
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

        tk.Label(self, text="Your Results", font=("Arial", 18)).pack(pady=10, padx=(0,75))
        
        #frame for the text area
        text_frame = tk.Frame(self)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            text_frame, 
            wrap="word",        # wraps text at word boundaries
            #height=20,
            yscrollcommand=scrollbar.set, 
            font=("Arial", 18)
        )
        self.text_area.pack(fill="both", expand=True)

        scrollbar.config(command=self.text_area.yview)  

        
    def update_page(self):
        """Optional refresh when shown."""
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
