import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from data import combat_options
from score_calculator import calculate_score
import os
import sys
from ttkbootstrap import Style
import webbrowser

chaos_selectable = ["思维矫正", "朝谒", "魂灵朝谒", "授法", "不容拒绝"]
emergency_selectable = ["信号灯", "劫虚济实", "鸭速公路", "玩具的报复"]

def resource_path(relative_path):
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error in getting resource path: {e}")
        return relative_path

def open_github():
    """打开 GitHub 页面"""
    webbrowser.open("https://github.com/SankRea/ScoreCalculation")

def create_ui():
    style = Style(theme='sandstone')
    root = style.master
    root.title("白金杯分数计算器")
    root.geometry("800x600")
    root.configure(bg="#f4f4f4")

    icon_path = resource_path('title.ico')
    root.iconbitmap(icon_path)

    label = tk.Label(root, text="白金杯分数计算器", font=("Segoe UI", 18), pady=20, bg="#f4f4f4", fg="#333")
    label.pack()

    main_frame = tk.Frame(root, bg="#f4f4f4")
    main_frame.pack(fill="both", expand=True)

    frame_container = tk.Frame(main_frame, bg="#f4f4f4")
    frame_container.pack(side="left", fill="both", expand=True)

    canvas = tk.Canvas(frame_container, bg="#f4f4f4", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f4f4f4")

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    def update_scroll_region():
        """更新滚动区域"""
        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def _on_mouse_wheel(event):
        """鼠标滚轮滚动"""
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    root.bind("<MouseWheel>", _on_mouse_wheel)  
    root.after(100, update_scroll_region)

    selected_options = []
    chaos_status = {}
    emergency_status = {}

    def update_selected_options():
        selected_options.clear()
        for frame in frames:
            if frame.var.get() == 1:
                selected_options.append(frame.option)
                if hasattr(frame, 'chaos_var'):
                    chaos_status[frame.option] = frame.chaos_var.get()
                if hasattr(frame, 'emergency_var'):
                    emergency_status[frame.option] = frame.emergency_var.get()

    frames = []
    def create_option_frame(option):
        frame = tk.Frame(scrollable_frame, bg="#f4f4f4", pady=5)
        frame.pack(fill="x", padx=20, pady=5)

        var = tk.IntVar()
        checkbox = tk.Checkbutton(frame, text=option, variable=var, font=("Segoe UI", 12), 
                                  command=update_selected_options, bg="white", activebackground="white", 
                                  fg="#555", selectcolor="white", indicatoron=0)
        checkbox.pack(side="left", padx=10)

        frame.var = var
        frame.option = option

        if option in chaos_selectable:
            chaos_var = tk.StringVar(value="正常")
            chaos_options = ["正常", "混乱"]
            if option == "授法":
                chaos_options.extend(["正常+滚动先祖", "混乱+滚动先祖"])
            if option == "不容拒绝":
                chaos_options.extend(["正常+终结的实相", "混乱+终结的实相"])

            chaos_menu = ttk.Combobox(frame, textvariable=chaos_var, values=chaos_options, state="readonly",
                                       font=("Segoe UI", 12), width=15)
            chaos_menu.pack(side="right", padx=10)
            frame.chaos_var = chaos_var

        if option in emergency_selectable:
            emergency_var = tk.StringVar(value="普通")
            emergency_options = ["普通", "紧急"]
            emergency_menu = ttk.Combobox(frame, textvariable=emergency_var, values=emergency_options, state="readonly",
                                           font=("Segoe UI", 12), width=15)
            emergency_menu.pack(side="right", padx=10)
            frame.emergency_var = emergency_var

        return frame

    for option in combat_options:
        frame = create_option_frame(option)
        frames.append(frame)

    right_frame = tk.Frame(main_frame, bg="#f4f4f4", width=250)
    right_frame.pack(side="right", fill="y")

    input_fields = [
        ("隐藏怪", [str(i) for i in range(21)], "0"),
        ("藏品", None, ""),
        ("临时招募4星", None, ""),
        ("临时招募5星", None, ""),
        ("临时招募6星", None, ""),
        ("剩余取款额度", None, ""),
        ("起始存款", None, ""),
        ("终止存款", None, ""),
        ("结算页得分", None, "")
    ]

    entries = {}
    for idx, (label_text, values, default_value) in enumerate(input_fields):
        label = tk.Label(right_frame, text=label_text, font=("Segoe UI", 12), bg="#f4f4f4")
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

        if values:
            entry = ttk.Combobox(right_frame, values=values, font=("Segoe UI", 12), width=10, state="readonly")
            entry.set(default_value)
        else:
            entry = tk.Entry(right_frame, font=("Segoe UI", 12), width=20)
            entry.insert(0, default_value)

        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[label_text] = entry

    def calculate_button_click():
        update_selected_options()
        score = calculate_score(
            selected_options,
            entries["隐藏怪"].get(),
            entries["藏品"].get(),
            entries["临时招募4星"].get(),
            entries["临时招募5星"].get(),
            entries["临时招募6星"].get(),
            entries["起始存款"].get(),
            entries["终止存款"].get(),
            entries["剩余取款额度"].get(),
            entries["结算页得分"].get(),
            chaos_status,
            emergency_status
        )

        result_window = tk.Toplevel(root)
        result_window.title("计算结果")
        result_window.geometry("500x400")
        result_window.configure(bg="#f4f4f4")

        result_label = tk.Label(result_window, text="计算结果", font=("Segoe UI", 16, "bold"), bg="#f4f4f4", fg="#333")
        result_label.pack(pady=20)

        score_label = tk.Label(result_window, text=f"总分: {score}", font=("Segoe UI", 24, "bold"), bg="#f4f4f4", fg="#e74c3c")
        score_label.pack(pady=20)

        other_info = (
            f"隐藏怪数量: {entries['隐藏怪'].get()}\n"
            f"藏品: {entries['藏品'].get()}\n"
            f"临时招募4星: {entries['临时招募4星'].get()}\n"
            f"临时招募5星: {entries['临时招募5星'].get()}\n"
            f"临时招募6星: {entries['临时招募6星'].get()}\n"
            f"起始存款: {entries['起始存款'].get()}\n"
            f"终止存款: {entries['终止存款'].get()}\n"
            f"剩余取款额度: {entries['剩余取款额度'].get()}\n"
            f"结算页得分: {entries['结算页得分'].get()}"
        )

        info_label = tk.Label(result_window, text=other_info, font=("Segoe UI", 12), bg="#f4f4f4", fg="#333")
        info_label.pack(pady=10)

        close_button = tk.Button(result_window, text="关闭", command=result_window.destroy, font=("Segoe UI", 12), bg="#3498db", fg="white")
        close_button.pack(pady=20)

        result_window.mainloop()


    calculate_button = tk.Button(right_frame, text="计算分数", command=calculate_button_click, font=("Segoe UI", 14), 
                                 padx=20, pady=10, bg="#2a8fbd", fg="white")
    calculate_button.grid(row=len(input_fields), column=0, columnspan=2, pady=20)

    github_label = tk.Label(root, text="GitHub: https://github.com/SankRea/ScoreCalculation", font=("Segoe UI", 10), fg="blue", bg="#f4f4f4", cursor="hand2")
    github_label.pack(side="bottom", pady=10)
    github_label.bind("<Button-1>", lambda e: open_github())

    root.mainloop()
