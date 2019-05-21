import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import ttk
import tkdemo_decode
import tkdemo_embed

class NewWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("360水印系统")
        self.geometry("300x150")

        self.name_label = ttk.Label(self, text="360水印系统", anchor="center")
        self.encode_button = ttk.Button(self, text="嵌入水印", command=self.onEncode)
        self.decode_button = ttk.Button(self, text="提取水印", command=self.onDecode)

        self.name_label.pack(fill=tk.BOTH, expand=1)
        self.encode_button.pack(fill=tk.X, expand=1)
        self.decode_button.pack(fill=tk.X, expand=1)

    def onDecode(self):
        tkDecode = tkdemo_decode.tkDecode()
        tkDecode.mainloop()

    def onEncode(self):
        tkEncode = tkdemo_embed.tkEncode()
        tkEncode.mainloop()



if __name__ == "__main__":
    newWindow = NewWindow()
    newWindow.mainloop()
