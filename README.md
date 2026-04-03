# Jobbsökare för Arbetsförmedlingen

Ett enkelt Python-script som söker efter jobb på Arbetsförmedlingen och sparar resultaten till Excel och CSV.

## Vad gör det?

- Söker jobb via Arbetsförmedlingens API
- Filtrerar bort irrelevanta jobb
- Sparar nya jobb till `jobs.csv` och `jobs.xlsx`
- Håller koll på vad som är nytt sedan förra gången

## Installation

1. Klona projektet:
```bash
git clone https://github.com/ThBuKj/jobsearch-arbetsformedlingen-python.git
cd jobsearch-arbetsformedlingen-python
```

2. Installera dependencies:
```bash
pip install pandas pyyaml requests openpyxl
```

## Användning

1. Redigera `config.yml` och lägg till dina egna sökord och platser

2. Kör scriptet:
```bash
python src/main.py
```

3. Öppna `jobs.xlsx` eller `jobs.csv` för att se resultaten

## Konfigurera sökningen

Öppna `config.yml` och ändra:

- **keywords**: Vad du söker efter (använd `-senior` för att exkludera ord)
- **locations**: Vilka kommuner du söker i
- **include_words**: Ord som MÅSTE finnas i jobbet
- **exclude_words**: Ord som INTE får finnas i jobbet

## Projektstruktur

```
jobsearch-arbetsformedlingen-python/
├── config.yml          # Konfiguration
├── jobs.csv           # Resultat (skapas automatiskt, gitignored)
├── jobs.xlsx          # Resultat (skapas automatiskt, gitignored)
└── src/
    ├── main.py        # Huvudscript
    └── api.py         # API-anrop till Arbetsförmedlingen
```

## Tips

- Kör scriptet regelbundet (t.ex. varje dag) för att hitta nya jobb
- Använd `-senior -lead` i sökorden för att filtrera bort roller med mycket erfarenhetskrav
- Testa olika sökord för att hitta fler relevanta jobb
