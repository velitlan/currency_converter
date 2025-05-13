import requests

API_BASE = "https://api.frankfurter.app"
session = requests.Session()

def get_supported_currencies():
    try:
        response = session.get(f"{API_BASE}/currencies")
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise ValueError("Liste nicht abrufbar.")

def fetch_exchange_rate(base_currency, target_currency):
    if base_currency == target_currency:
        return 1.0
    try:
        response = session.get(f"{API_BASE}/latest", params={"from": base_currency, "to": target_currency})
        response.raise_for_status()
        data = response.json()
        return data["rates"].get(target_currency)
    except requests.RequestException:
        raise ValueError("Fehler beim Abrufen des Wechselkurses.")

def convert_currency(amount, rate):
    return amount * rate

def main():
    print("Währungsrechner (Frankfurter API, EZB-Daten)")
    try:
        currencies = get_supported_currencies()
        print("\nVerfügbare Währungen:")
        print(", ".join(sorted(currencies)))

        base = input("\nAusgangswährung (z.B. EUR): ").upper()
        target = input("Zielwährung (z.B. USD): ").upper()

        if base not in currencies or target not in currencies:
            print("Ungültige Währung. Bitte aus der Liste wählen.")
            return

        amount = float(input(f"Betrag in {base}: "))
        rate = fetch_exchange_rate(base, target)
        if rate is None:
            print("Wechselkurs nicht auffindbar.")
            return

        result = convert_currency(amount, rate)
        print(f"\n{amount:.2f} {base} = {result:.2f} {target} (Kurs: {rate:.4f})")

    except Exception as e:
        print("Fehler:", e)

if __name__ == "__main__":
    main()