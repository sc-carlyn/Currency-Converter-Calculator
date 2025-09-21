import tkinter as tk
from tkinter import ttk
import requests

# API anahtarınızı buraya girin
API_KEY = '62cd50e8a86bc56c18c8859c'

# Döviz kuru verilerini al
def get_exchange_rate(base, target):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base}"
    response = requests.get(url)
    data = response.json()
    if data['result'] == 'success':
        return data['conversion_rates'].get(target, None)
    return None

# Döviz dönüştürme işlemi
def convert_currency():
    base_currency = base_currency_combobox.get()
    target_currency = target_currency_combobox.get()
    amount = amount_entry.get()
    
    if not amount.replace('.', '', 1).isdigit():
        result_label.config(text="Lütfen geçerli bir miktar girin.")
        return
    
    amount = float(amount)
    rate = get_exchange_rate(base_currency, target_currency)
    
    if rate:
        converted_amount = amount * rate
        result_label.config(text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
    else:
        result_label.config(text="Kur alınamadı. Lütfen internet bağlantınızı kontrol edin.")

# Hesap makinesi işlemleri
def press(key):
    current = display_var.get()
    display_var.set(current + str(key))

def clear():
    display_var.set("")

def calculate():
    try:
        result = eval(display_var.get())
        display_var.set(result)
    except Exception as e:
        display_var.set("Hata")

# Ana pencere
root = tk.Tk()
root.title("Döviz Dönüştürücü ve Hesap Makinesi")
root.geometry("400x600")
root.configure(bg="#2c3e50")

# Döviz dönüştürücü
frame_converter = tk.Frame(root, bg="#34495e")
frame_converter.pack(fill="both", expand=True, padx=10, pady=10)

tk.Label(frame_converter, text="Miktar:", fg="white", bg="#34495e").grid(row=0, column=0, padx=5, pady=5)
amount_entry = tk.Entry(frame_converter, width=15)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_converter, text="Kaynak Para Birimi:", fg="white", bg="#34495e").grid(row=1, column=0, padx=5, pady=5)
base_currency_combobox = ttk.Combobox(frame_converter, values=["USD", "EUR", "GBP", "TRY"], width=10)
base_currency_combobox.grid(row=1, column=1, padx=5, pady=5)
base_currency_combobox.set("USD")

tk.Label(frame_converter, text="Hedef Para Birimi:", fg="white", bg="#34495e").grid(row=2, column=0, padx=5, pady=5)
target_currency_combobox = ttk.Combobox(frame_converter, values=["USD", "EUR", "GBP", "TRY"], width=10)
target_currency_combobox.grid(row=2, column=1, padx=5, pady=5)
target_currency_combobox.set("TRY")

convert_button = tk.Button(frame_converter, text="Dönüştür", command=convert_currency)
convert_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(frame_converter, text="", fg="white", bg="#34495e")
result_label.grid(row=4, column=0, columnspan=2, pady=5)

# Hesap makinesi
frame_calculator = tk.Frame(root, bg="#34495e")
frame_calculator.pack(fill="both", expand=True, padx=10, pady=10)

display_var = tk.StringVar()
display = tk.Entry(frame_calculator, textvariable=display_var, font=("Arial", 20), bd=5, relief="sunken", justify="right")
display.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

buttons = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', '.', '=', '+')
]

for r, row in enumerate(buttons, 1):
    for c, button in enumerate(row):
        if button == "=":
            tk.Button(frame_calculator, text=button, width=5, height=2, command=calculate).grid(row=r, column=c, padx=5, pady=5)
        else:
            tk.Button(frame_calculator, text=button, width=5, height=2, command=lambda key=button: press(key)).grid(row=r, column=c, padx=5, pady=5)

clear_button = tk.Button(frame_calculator, text="C", width=5, height=2, command=clear)
clear_button.grid(row=5, column=0, columnspan=4, pady=5)

root.mainloop()
