import requests

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

def main():
    print("Währungsrechner (Frankfurter API, EZB-Daten)")
    try:
        currencies = get_supported_currencies()
        print("\nVerfügbare Währungen:")
        print(", ".join(sorted(currencies)))

        base = input("\nAusgangswährung (z.B. EUR): ").upper()
        targets_input = input("Zielwährung(en), kommasepariert (z.B. USD,JPY): ").upper()
        target_currencies = [c.strip() for c in targets_input.split(",")]

        if base not in currencies or any(t not in currencies for t in target_currencies):
            print("Ungültige Währung(en). Bitte aus der Liste wählen.")
            return

        amount = float(input(f"Betrag in {base}: "))
        rates = fetch_exchange_rates(base, target_currencies)

        print("\nUmrechnung:")
        for currency, rate in rates.items():
            result = convert_currency(amount, rate)
            print(f"{amount:.2f} {base} = {result:.2f} {currency} (Kurs: {rate:.4f})")

    except Exception as e:
        print("Fehler:", e)

if __name__ == "__main__":
    main()