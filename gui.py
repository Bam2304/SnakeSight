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
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MainPage, SecondPage, InfoPage):
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
        
        tk.Label(self, text="Welcome to Snake Sight", font=("Arial", 18)).pack(pady=10, padx=250)

        # Status label (not the image itself)
        self.status_label = tk.Label(self, text="No image submitted")
        self.status_label.pack(pady=10)

        # Upload button
        upload_btn = tk.Button(self, text="Upload Image", command=self.upload_image)
        upload_btn.pack(pady=65, padx=50)

        # Forward button
        next_btn = tk.Button(
            self, text="Go to Second Page",
            command=lambda: controller.show_frame("SecondPage")
        )
        next_btn.pack(pady=55, padx=50)

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

        tk.Label(self, text="Q&A", font=("Arial", 18)).pack(pady=10, padx=250)

        # Back button
        back_btn = tk.Button(
            self, text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        #back_btn.pack(pady=250, padx=20)
        back_btn.place(x=18, y=10)
    def update_page(self):
        """Optional refresh when shown."""
        pass

class InfoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(background='blue')

        tk.Label(self, text="Disclaimer", font=("Arial", 18)).pack(pady=10, padx=250)
        
        #disclaimer message for info page
        message = "Warning: This app is for demonstration purposes only. " \
        "Advice given here is to be taken with a grain of salt, and does not replace " \
        "the advice of actual medical professionals."
        disclaimer_space = tk.Message(self, text=message, width=300, font=("Arial", 20), justify="center")
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

if __name__ == "__main__":
    app = App()
    app.mainloop()
