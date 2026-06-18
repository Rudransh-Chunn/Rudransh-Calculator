import tkinter as tk
import math

button_values = [
    ["AC", "+/-", "%", "÷", "sin"],
    ["7", "8", "9", "×", "cos"],
    ["4", "5", "6", "-", "tan"],
    ["1", "2", "3", "+", "log"],
    ["0", ".", "√", "=", "ln"],
    ["x²", "xʸ", "π", "e", ""]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]

row_count = len(button_values)
column_count = len(button_values[0])

color_black = "#0D0D0D"
color_dark_gray = "#1A1A1A"
color_light_gray = "#2A2A2A"
color_neon = "#00FFAA"

root = tk.Tk()
root.title("Neon Scientific Calculator")
root.resizable(False, False)
root.configure(bg=color_black)

frame = tk.Frame(root, bg=color_black)
frame.pack(side="left", padx=5, pady=5)

history_box = tk.Listbox(
    root,
    height=18,
    width=15,
    bg="#050505",
    fg=color_neon,
    font=("Consolas", 11),
    bd=0,
    highlightthickness=0,
    selectbackground=color_neon,
    selectforeground=color_black
)
history_box.pack(side="right", fill="y")

scroll = tk.Scrollbar(root)
scroll.pack(side="right", fill="y")
history_box.config(yscrollcommand=scroll.set)
scroll.config(command=history_box.yview)

label = tk.Label(
    frame,
    text="0",
    font=("Consolas", 38, "bold"),
    bg=color_black,
    fg=color_neon,
    anchor="e",
    width=column_count
)
label.grid(row=0, column=0, columnspan=column_count, sticky="we", padx=8, pady=8)

A = "0"
operator = None
B = None
history = []

def clear_all():
    global A, B, operator
    A = "0"
    B = None
    operator = None

def remove_zero_decimal(number):
    if number % 1 == 0:
        return str(int(number))
    return str(number)

def flash():
    label.config(bg="#002B2B")
    root.after(100, lambda: label.config(bg=color_black))

def button_clicked(value):
    global A, B, operator

    if value in right_symbols:

        if value == "=":
            if operator is not None:
                B = label["text"]
                numA = float(A)
                numB = float(B)

                if operator == "+":
                    result = numA + numB
                elif operator == "-":
                    result = numA - numB
                elif operator == "×":
                    result = numA * numB
                elif operator == "÷":
                    if numB == 0:
                        label["text"] = "Error"
                        return
                    result = numA / numB
                elif operator == "^":
                    result = numA ** numB

                result_str = remove_zero_decimal(result)

                history_entry = f"{A} {operator} {B} = {result_str}"
                history.append(history_entry)
                history_box.insert(tk.END, history_entry)

                if len(history) > 10:
                    history.pop(0)
                    history_box.delete(0)

                label["text"] = result_str
                flash()
                clear_all()

        else:
            if operator is None:
                A = label["text"]
                label["text"] = "0"
            operator = value

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = "0"

        elif value == "+/-":
            result = float(label["text"]) * -1
            label["text"] = remove_zero_decimal(result)

        elif value == "%":
            result = float(label["text"]) / 100
            label["text"] = remove_zero_decimal(result)

    else:
        if value == ".":
            if "." not in label["text"]:
                label["text"] += value

        elif value == "√":
            num = float(label["text"])
            result = num ** 0.5
            label["text"] = remove_zero_decimal(result)

        elif value == "sin":
            result = math.sin(math.radians(float(label["text"])))
            label["text"] = remove_zero_decimal(result)

        elif value == "cos":
            result = math.cos(math.radians(float(label["text"])))
            label["text"] = remove_zero_decimal(result)

        elif value == "tan":
            result = math.tan(math.radians(float(label["text"])))
            label["text"] = remove_zero_decimal(result)

        elif value == "log":
            result = math.log10(float(label["text"]))
            label["text"] = remove_zero_decimal(result)

        elif value == "ln":
            result = math.log(float(label["text"]))
            label["text"] = remove_zero_decimal(result)

        elif value == "x²":
            num = float(label["text"])
            result = num ** 2
            label["text"] = remove_zero_decimal(result)

        elif value == "xʸ":
            A = label["text"]
            operator = "^"
            label["text"] = "0"

        elif value == "π":
            label["text"] = str(math.pi)

        elif value == "e":
            label["text"] = str(math.e)

        else:
            if label["text"] == "0":
                label["text"] = value
            else:
                label["text"] += value

def animate_click(button, value):
    w, h = button["width"], button["height"]
    button.config(width=w-1, height=h-1)
    root.after(100, lambda: button.config(width=w, height=h))
    button_clicked(value)

def on_enter(e):
    e.widget.config(bg="#00FFAA", fg=color_black)

def on_leave(e):
    value = e.widget["text"]
    if value in top_symbols:
        e.widget.config(bg=color_light_gray, fg=color_neon)
    elif value in right_symbols:
        e.widget.config(bg="#002B2B", fg=color_neon)
    else:
        e.widget.config(bg=color_dark_gray, fg=color_neon)

for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]

        if value == "":
            continue

        button = tk.Button(
            frame,
            text=value,
            font=("Consolas", 14, "bold"),
            width=5,
            height=2,
            relief="flat",
            bd=0,
            activebackground=color_neon,
            activeforeground=color_black
        )

        button.config(command=lambda b=button, v=value: animate_click(b, v))

        if value in top_symbols:
            button.config(bg=color_light_gray, fg=color_neon)
        elif value in right_symbols:
            button.config(bg="#002B2B", fg=color_neon)
        else:
            button.config(bg=color_dark_gray, fg=color_neon)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        button.grid(row=row+1, column=column, padx=2, pady=2)

root.update()
w = root.winfo_width()
h = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f"{w}x{h}+{x}+{y}")

root.mainloop()