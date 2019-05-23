import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
import decode
import logger
import json


class tkDecode(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("360水印提取 v1")
        self.geometry("500x300")

        self.notebook = Notebook(self)

        main = tk.Frame(self.notebook)
        second = tk.Frame(self.notebook)
        secondhalf = tk.Frame(self.notebook)
        third = tk.Frame(self.notebook)

        self.conduct_button = tk.Button(main, text="提取", command=self.decode)
        self.conduct_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.json_str = tk.Text(main, bg="white", fg="black")
        self.json_str.pack(side=tk.TOP, expand=1)

        # self.italian_copy_button = tk.Button(italian_tab, text="Copy to Clipboard", command=self.copy_to_clipboard)
        # self.italian_copy_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.watermark = tk.StringVar(second)
        self.watermark.set("")

        self.watermark_label = tk.Label(second, textvar=self.watermark, bg="lightgrey", fg="black")
        self.watermark_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.data_str = tk.Text(secondhalf, bg="white", fg="black")
        self.data_str.pack(side=tk.TOP, fill=tk.BOTH)

        self.loginfo = tk.StringVar(third)
        self.loginfo.set("")

        self.loginfo_label = tk.Label(third, textvar=self.loginfo, bg="white", fg="black")
        self.loginfo_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.notebook.add(main, text="输入JSON格式")
        self.notebook.add(secondhalf, text="信息长度")
        self.notebook.add(second, text="提取结果")
        self.notebook.add(third, text="日志")

        self.notebook.pack(fill=tk.BOTH, expand=1)

    def decode(self):
        try:
            text = self.json_str.get(1.0, tk.END)
            JSON = json.loads(text)
            log = logger.Logger(filename=None)
            dec = decode.decode(log=log)
            watermark = dec.run(JSON, int(self.data_str.get(1.0, tk.END)))
            self.watermark.set(watermark)
            self.loginfo.set(log.str)
            msg.showinfo("Decode Successful", "Decode Successful")
        except Exception as e:
            msg.showerror("Decode Failed", str(e))

    # def copy_to_clipboard(self, text=None):
    #     if not text:
    #         text = self.italian_translation.get()
    #
    #     self.clipboard_clear()
    #     self.clipboard_append(text)
    #     msg.showinfo("Copied Successfully", "Text copied to clipboard")


if __name__ == "__main__":
    tkDecode = tkDecode()
    tkDecode.mainloop()
