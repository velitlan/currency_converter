import requests
import tkinter as tk
from tkinter import ttk, messagebox

API_BASE = "https://api.frankfurter.app"
session = requests.Session()

def get_supported_currencies():
    try:
        response = session.get(f"{API_BASE}/currencies")
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise ValueError("Liste der Währungen konnte nicht abgerufen werden.")

def fetch_exchange_rates(base_currency, target_currencies):
    if base_currency in target_currencies:
        target_currencies.remove(base_currency)
    if not target_currencies:
        return {base_currency: 1.0}
    try:
        response = session.get(f"{API_BASE}/latest", params={"from": base_currency, "to": ",".join(target_currencies)})
        response.raise_for_status()
        data = response.json()
        return data["rates"]
    except requests.RequestException:
        raise ValueError("Fehler beim Abrufen der Wechselkurse.")

def convert_currency(amount, rate):
    return amount * rate

def perform_conversion():
    try:
        base = base_currency_var.get()
        targets = [target_currency_var.get()]
        amount = float(amount_var.get())

        if base not in currencies or any(t not in currencies for t in targets):
            raise ValueError("Ungültige Währungen.")

        rates = fetch_exchange_rates(base, targets)

        result_text = ""
        for currency, rate in rates.items():
            converted = convert_currency(amount, rate)
            result_text += f"{amount:.2f} {base} = {converted:.2f} {currency} (Kurs: {rate:.4f})\n"

        result_label.config(text=result_text.strip())
    except Exception as e:
        messagebox.showerror("Fehler", str(e))

#GUI Setup
root = tk.Tk()
root.title("Währungsrechner (Frankfurter API)")

try:
    currencies = get_supported_currencies()
    currency_list = sorted(currencies.keys())
except Exception as e:
    messagebox.showerror("Fehler", str(e))
    root.destroy()
    exit()

#Elemente
base_currency_var = tk.StringVar(value="EUR")
target_currency_var = tk.StringVar(value="USD")
amount_var = tk.StringVar(value="1.0")

tk.Label(root, text="Ausgangswährung:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ttk.Combobox(root, textvariable=base_currency_var, values=currency_list).grid(row=0, column=1)

tk.Label(root, text="Zielwährung:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
ttk.Combobox(root, textvariable=target_currency_var, values=currency_list).grid(row=1, column=1)

tk.Label(root, text="Betrag:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=amount_var).grid(row=2, column=1)

tk.Button(root, text="Umrechnen", command=perform_conversion).grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", justify="left", font=("Courier", 10))
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()