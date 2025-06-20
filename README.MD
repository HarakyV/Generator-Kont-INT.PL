# 🚀 INT.PL - Selenium Generator Kont

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/selenium-%3E=4.x-green.svg" alt="Selenium 4+">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-lightgrey.svg" alt="CustomTkinter">
</p>

## 📌 Opis

**INT.PL - Selenium Generator Kont** to aplikacja z interfejsem graficznym, która automatycznie:

✅ tworzy konta e-mail na [int.pl](https://int.pl)  
✅ loguje się na utworzone konta  
✅ pozwala konfigurować liczbę kont, długość loginu i hasła, czas logowania  
✅ zapisuje dane kont do pliku `accounts.txt` (opcjonalnie)

---

## ⚙️ Wymagania

- Python **3.8+**
- Biblioteki:  
  - `selenium`  
  - `customtkinter`  
  - `Pillow`  
  - `CTkMessagebox`
- Pobrany `chromedriver.exe` zgodny z Twoją wersją Chrome.

---

## 📁 Pliki

| Plik | Opis |
|------|------|
| `main.py` | Główny program |
| `config.txt` | Plik konfiguracyjny |
| `accounts.txt` | Zapisane konta (jeśli włączono zapisywanie) |
| `info.txt` | Krótkie instrukcje użytkowania |

---

## 🖱️ Funkcjonalności

- **Ekran główny:**  
  - Start generatora kont  
  - Start logowania na konto  
  - Przycisk otwierający `info.txt`
  - Przycisk konfiguracji

- **Ekran konfiguracji:**  
  - Ścieżka do chromedrivera  
  - Ilość kont  
  - Czas logowania  
  - Długość loginu i hasła  
  - Checkbox zapisywania kont

- **Tryb headless:**  
  - Checkbox decyduje, czy widzisz przeglądarkę podczas działania.

---

KONTAKT: harakyx@gmail.com

## 🚀 Jak uruchomić?

```bash
# Zainstaluj wymagane biblioteki
pip install selenium customtkinter pillow CTkMessagebox

# Uruchom program
python main.py


