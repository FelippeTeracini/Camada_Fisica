from tkinter import *
from tkinter import filedialog
from tkinter import ttk
def filename():
    root.fileName=filedialog.askopenfilename(filetype=(("All files","*.*"),))

    x=root.fileName
    print(x)
    exit()
root=Tk()
root.geometry("600x600")
btn1=ttk.Button(root,text="escolha a imagem")
btn1.pack()

btn1.config(command=filename)
mainloop()
