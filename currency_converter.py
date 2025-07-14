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
    targets = [c for c in target_currencies if c != base_currency]
    if not targets:
        return {base_currency: 1.0}
    try:
        response = session.get(f"{API_BASE}/latest", params={"from": base_currency, "to": ",".join(targets)})
        response.raise_for_status()
        return response.json().get("rates", {})
    except requests.RequestException:
        raise ValueError("Fehler beim Abrufen der Wechselkurse.")

def convert_currency(amount, rate):
    return amount * rate

def perform_conversion():
    try:
        base = base_currency_var.get()
        target = target_currency_var.get()
        amount = float(amount_var.get())
        if base not in currencies or target not in currencies:
            raise ValueError("Ungültige Währungsauswahl.")
        rates = fetch_exchange_rates(base, [target])
        rate = rates.get(target, 1.0)
        converted = convert_currency(amount, rate)
        result_label.config(text=f"{amount:.2f} {base} = {converted:.2f} {target} (Kurs: {rate:.4f})")
    except ValueError as ve:
        messagebox.showerror("Fehler", str(ve))
    except Exception:
        messagebox.showerror("Fehler", "Ungültige Eingabe.")

root = tk.Tk()
root.title("Währungsrechner (Frankfurter API)")

try:
    currencies = get_supported_currencies()
    currency_list = sorted(currencies)
except Exception as e:
    messagebox.showerror("Fehler beim Start", str(e))
    root.destroy()
    exit()

base_currency_var = tk.StringVar(value="EUR")
target_currency_var = tk.StringVar(value="USD")
amount_var = tk.StringVar(value="1.0")

entries = [
    ("Ausgangswährung:", ttk.Combobox(root, textvariable=base_currency_var, values=currency_list, state="readonly")),
    ("Zielwährung:", ttk.Combobox(root, textvariable=target_currency_var, values=currency_list, state="readonly")),
    ("Betrag:", tk.Entry(root, textvariable=amount_var)),
]

for i, (label_text, widget) in enumerate(entries):
    tk.Label(root, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
    widget.grid(row=i, column=1, padx=5, pady=5)

tk.Button(root, text="Umrechnen", command=perform_conversion).grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", justify="left", font=("Courier", 10))
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()