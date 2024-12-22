import os
import tkinter as tk
from tkinter import ttk, filedialog
import openpyxl
import chardet

def choose_folder_path():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)
    else:
        folder_path_var.set("No folder selected.")

def read_excel_files_in_folder(folder_path):
    # 检查文件夹路径是否存在
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.lower().endswith((".xls", ".xlsx", ".xlsm")):  # 仅处理Excel文件
                print(f"Reading Excel file: {file_path}")
                # 检测文件编码
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    encoding = chardet.detect(raw_data)['encoding']

                # 使用正确的编码方式打开文件
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    print(content)

def generate_event():
    selected_folder = folder_path_var.get()
    if selected_folder:
        print("Generating with folder path:", selected_folder)
        read_excel_files_in_folder(selected_folder)  # 调用读取Excel文件夹函数
    else:
        print("No folder selected.")

# 创建主窗口
root = tk.Tk()
root.title("Excel Files Selector")

# 添加容器框架
frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

# 添加输入框和按钮
folder_path_var = tk.StringVar()
folder_path_entry = ttk.Entry(frame, textvariable=folder_path_var, width=50, state="readonly")
folder_path_entry.grid(row=0, column=0, padx=5, pady=5)

choose_button = ttk.Button(frame, text="Choose Folder", command=choose_folder_path)
choose_button.grid(row=0, column=1, padx=5, pady=5)

generate_button = ttk.Button(frame, text="Generate", command=generate_event)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)

# 运行主循环
root.mainloop()
