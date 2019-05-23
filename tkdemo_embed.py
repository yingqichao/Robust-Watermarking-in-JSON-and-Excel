import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
import encode
import logger
import json


class tkEncode(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("360水印嵌入 v1")
        self.geometry("500x300")

        self.notebook = Notebook(self)

        main = tk.Frame(self.notebook)
        second = tk.Frame(self.notebook)
        secondhalf = tk.Frame(self.notebook)
        third = tk.Frame(self.notebook)

        self.conduct_button = tk.Button(main, text="嵌入", command=self.encode)
        self.conduct_button.pack(side=tk.BOTTOM, fill=tk.X)

        # self.data_str = tk.Text(main, bg="lightgrey", fg="black"width=50, height=50)
        # self.data_str.pack(side=tk.TOP, fill=tk.X)

        self.json_str = tk.Text(main, bg="white", fg="black")
        self.json_str.pack(side=tk.TOP, fill=tk.BOTH)

        # self.italian_copy_button = tk.Button(italian_tab, text="Copy to Clipboard", command=self.copy_to_clipboard)
        # self.italian_copy_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.watermark = tk.StringVar(second)
        self.watermark.set("")

        self.copy_button = tk.Button(second, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.BOTTOM, fill=tk.X)


        self.watermark_label = tk.Text(second, bg="white", fg="black")
        self.watermark_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)



        self.data_str = tk.Text(secondhalf, bg="white", fg="black")
        self.data_str.pack(side=tk.TOP, fill=tk.BOTH)

        self.loginfo = tk.StringVar(third)
        self.loginfo.set("")

        self.loginfo_label = tk.Label(third, textvar=self.loginfo, bg="white", fg="black")
        self.loginfo_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.notebook.add(main, text="输入JSON格式")
        self.notebook.add(secondhalf, text="秘密信息")
        self.notebook.add(second, text="嵌入结果")
        self.notebook.add(third, text="日志")

        self.notebook.pack(fill=tk.BOTH, expand=1)

    def encode(self):
        try:
            text = self.json_str.get(1.0, tk.END)
            data = self.data_str.get(1.0, tk.END)
            JSON = json.loads(text)
            log = logger.Logger(filename=None)
            enc = encode.encode(data, log=log)
            embeddedJSON = enc.run(JSON)
            # self.watermark.set(embeddedJSON)
            self.watermark_label.insert(10.0,json.dumps(embeddedJSON))
            self.loginfo.set(log.str)
            msg.showinfo("Embed Successful", "Embed Successful")
        except Exception as e:
            msg.showerror("Embed Failed", str(e))

    def copy_to_clipboard(self, text=None):
        if not text:
            text = self.watermark_label.get(1.0, tk.END)

        self.clipboard_clear()
        self.clipboard_append(text)
        msg.showinfo("Copied Successfully", "Text copied to clipboard")

    # def copy_to_clipboard(self, text=None):
    #     if not text:
    #         text = self.italian_translation.get()
    #
    #     self.clipboard_clear()
    #     self.clipboard_append(text)
    #     msg.showinfo("Copied Successfully", "Text copied to clipboard")


if __name__ == "__main__":
    tkEncode = tkEncode()
    tkEncode.mainloop()
