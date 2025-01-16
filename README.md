# FIIT STU ZS 2024/25: Evolučný algoritmus

### Téma: Návrh evolučného algoritmu na optimalizáciu správania agentov

**Autor:** Martin Kvietok, Slovenská technická univerzita v Bratislave

---

## **Popis projektu**

Cieľom projektu je implementácia evolučného algoritmu, ktorý optimalizuje správanie agentov na nájdenie piatich pokladov na 2D hracom poli (7x7). Každý agent je reprezentovaný sekvenciou inštrukcií spracovaných virtuálnym strojom s 64-bajtovou pamäťou. Algoritmus využíva genetické operácie (kríženie, mutácia) a princípy evolúcie na postupné zlepšovanie výkonnosti agentov počas generácií.

---

## **Kľúčové koncepty**

### 1. **Inicializácia počiatočnej generácie**
- Vytvorenie prostredia (class `Environment`) z údajov v súbore `input.txt`.
- Generovanie 201 agentov (class `Agent`) s náhodnými inštrukčnými sadami.
- Maximálny počet generácií: 2000.

### 2. **Fitness funkcia**
- Vyhodnotenie agentov na základe:
  - Počtu nájdených pokladov.
  - Efektívnosti krokov (bonus za kratšiu trajektóriu).
  - Penalizácie za prechod mimo hracie pole alebo prekročenie limitu inštrukcií.

### 3. **Tvorba novej generácie**
- Triedenie populácie podľa fitness hodnôt.
- **Elitizmus:** Najlepší jedinec je vždy zachovaný.
- Výber jedincov na kríženie pomocou turnajového výberu alebo predvýberu.

### 4. **Genetické operácie**
- **Kríženie:**
  - Uprednostnenie génov rodiča s vyššou fitness hodnotou.
  - Generovanie dvoch potomkov pre zvýšenie diverzity.
- **Mutácia:**
  - Úprava inštrukcií (inkrementácia, dekrementácia, výmena hodnôt).
  - Dynamické nastavenie intenzity mutácie podľa generácie.
- **Budič:**
  - Randomizácia inštrukčných sád po 200-300 generáciách na prekonanie stagnácie.

---

## **Finálne testovanie a výsledky**
- Najúspešnejšie generácie nachádzajú všetkých 5 pokladov s počtom krokov v rozmedzí 19–30.
- Efektivita algoritmu závisí od kombinácie vstupných parametrov a diverzity populácie.
- Grafy zobrazujú priebeh evolúcie a zlepšovanie fitness hodnôt.

---

## **Použitie programu**

1. Spustite súbor `setup.py` v prostredí Visual Studio 2022.
2. Program vykonáva simuláciu a vypisuje:
   - Počet generácií.
   - Počet nájdených pokladov.
   - Počet krokov potrebných na úspešné nájdenie pokladov.
3. Po skončení simulácie sa zobrazí graf zobrazujúci evolúciu fitness funkcie.

---

## **Záver**

Evolučný algoritmus úspešne rieši zadaný problém s vysokou efektivitou. Hlavné prínosy:
- Možnosť nájsť všetkých 5 pokladov za relatívne krátky čas (do 200 generácií).
- Diverzita populácie a genetické operácie zlepšujú výsledky.

Možnosti na vylepšenie:
- Implementácia hodnotenia individuálnych inštrukcií v génových sadách.
- Optimalizácia najlepšej cesty k pokladom.
