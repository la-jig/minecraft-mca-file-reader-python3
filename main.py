import os
import anvil

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.region = None
        self.chunk = (0,0)
        self.file = None

    def set_chunk(self, chunk: str, window: Toplevel):
        self.chunk = (int(chunk.split(", ")[0]), int(chunk.split(", ")[1]))
        window.destroy()
        
        for i in range(16):
            self.update()
            for i1 in range(256):
                self.update()
                for i2 in range(16):
                    self.update()
                    print(anvil.Chunk.from_region(self.region, self.chunk[0], self.chunk[1]).get_block(i, i1, i2))


    def open_file(self):
        self.file = filedialog.askopenfilename(filetypes=(("Mca files", "*.mca"), ("All files", "*.*")), initialdir=os.getcwd())

        try:
            self.region = anvil.Region.from_file(self.file)
        except Exception as ex:
            messagebox.showwarning("ERROR", str(ex))
        else:
            window = Toplevel(self)
            window.resizable(0,0)
            window.title("Select Region")
            passed = False
            
            listbox1 = Listbox(window, width=25, height=10)
            Button(window, text="Select", command=lambda: self.set_chunk(listbox1.get(listbox1.curselection()), window)).place(x=145, y=138)
            for i in range(32):
                for i1 in range(32):
                    try:
                        anvil.Chunk.from_region(self.region, i, i1)

                        listbox1.insert("end", f"{str(i)}, {str(i1)}")
                        passed = True
                    except Exception as ex:
                        print(ex)

            listbox1.pack()
            if passed:
                window.mainloop()
            else:
                window.destroy()
                messagebox.showerror("ERROR", "No non-empty chunk found!")




    def build_gui(self):
        self.menubar = Menu(self, tearoff=0)
        self.config(menu=self.menubar)

        self.filemenu = Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.filemenu.add_command(label="Open...", command=self.open_file)

        self.canvas = Canvas(self)
        self.canvas.pack(expand=True)

if __name__ == "__main__":
    window = MainWindow()
    window.build_gui()
    window.mainloop()