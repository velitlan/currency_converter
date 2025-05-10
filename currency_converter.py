import requests

def get_supported_currencies():
    url = "https://api.frankfurter.app/currencies"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Konnte die Liste der Währungen nicht abrufen.")

def fetch_exchange_rate(base_currency, target_currency):
    if base_currency == target_currency:
        return 1.0
    url = f"https://api.frankfurter.app/latest?from={base_currency}&to={target_currency}"
    response = requests.get(url)
    data = response.json()
    if "rates" in data and target_currency in data["rates"]:
        return data["rates"][target_currency]
    else:
        raise ValueError("Fehler beim Abrufen des Wechselkurses.")

def convert_currency(amount, rate):
    return amount * rate

def main():
    print("🌍 Währungsrechner (Frankfurter API, EZB-Daten)")
    try:
        currencies = get_supported_currencies()
        print("\nVerfügbare Währungen:")
        print(", ".join(sorted(currencies.keys())))

        base = input("\nAusgangswährung (z.B. EUR): ").upper()
        target = input("Zielwährung (z.B. USD): ").upper()

        if base not in currencies or target not in currencies:
            print("Ungültige Währung. Bitte aus der Liste wählen.")
            return

        amount = float(input(f"Betrag in {base}: "))
        rate = fetch_exchange_rate(base, target)
        result = convert_currency(amount, rate)

        print(f"\n{amount:.2f} {base} = {result:.2f} {target} (Kurs: {rate:.4f})")

    except Exception as e:
        print("Fehler:", e)

if __name__ == "__main__":
    main()