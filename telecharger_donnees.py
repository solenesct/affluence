"""
Télécharge les fichiers de données du projet
« Affluence du métro parisien un soir de match de pluie »
(période : 1er juillet 2025 -> 30 juin 2026).

Les fichiers sont enregistrés avec les noms attendus par nettoyage.py.

Usage :
    python telecharger_donnees.py
"""
from pathlib import Path

import pandas as pd
import requests

DOSSIER = Path(".")                      # même dossier que nettoyage.py
DEBUT, FIN = "2025-07-01", "2026-06-30"
PORTAIL = "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets"
TRIMESTRES = ["1er", "2eme", "3eme", "4eme"]

# Noms de fichiers attendus par nettoyage.py
NOMS_VALIDATIONS = {
    "1er": "1er-trimestre-validations-reseau-ferre-nombre-validations-par-jour.csv",
    "2eme": "2eme-trimestre-validations-reseau-ferre-nombre-validations-par-jour-2eme-trimestre.csv",
    "3eme": "3eme-trimestre-validations-reseau-ferre-nombre-validations-par-jour.csv",
    "4eme": "4eme-trimestre-validations-reseau-ferre-nombre-validations-par-jour.csv",
}
NOMS_PROFILS = {
    "1er": "validations-reseau-ferre-profils-horaires-par-jour-type-1er-trimestre.csv",
    "2eme": "validations-reseau-ferre-profils-horaires-par-jour-type-2eme-trimestre.csv",
    "3eme": "validations-reseau-ferre-profils-horaires-par-jour-type-3eme-trimestre.csv",
    "4eme": "4eme-trimestre-validations-reseau-ferre-profils-horaires-par-jour-type-4eme-trimestre.csv",
}


def telecharger(url, destination):
    """Télécharge une URL dans un fichier. Renvoie True si ça a marché."""
    try:
        r = requests.get(url, timeout=600)
        r.raise_for_status()
    except requests.RequestException as erreur:
        print(f"   échec : {erreur}")
        return False
    destination.write_bytes(r.content)
    print(f"   OK ({len(r.content) / 1e6:.1f} Mo)")
    return True


def telecharger_idfm(jeu, destination):
    # use_labels=true : mêmes noms de colonnes que l'export manuel (JOUR, NB_VALD...)
    url = f"{PORTAIL}/{jeu}/exports/csv?delimiter=%3B&use_labels=true"
    print(f" - {destination.name}  [{jeu}]")
    return telecharger(url, destination)


# 1. Validations par jour, réseau ferré (un fichier par trimestre)
#    Le nom du jeu de données peut contenir l'année : on essaie plusieurs noms
#    et on garde celui dont les dates sont bien dans la période.
print("1. Validations par jour")
for t in TRIMESTRES:
    base = f"validations-reseau-ferre-nombre-validations-par-jour-{t}-trimestre"
    fichier = DOSSIER / NOMS_VALIDATIONS[t]
    trouve = False
    for jeu in [base, base + "-2025", base + "-2026"]:
        if not telecharger_idfm(jeu, fichier):
            continue
        try:
            jours = pd.to_datetime(pd.read_csv(fichier, sep=";", encoding="utf-8-sig", usecols=["JOUR"])["JOUR"])
        except ValueError:
            colonnes = pd.read_csv(fichier, sep=";", encoding="utf-8-sig", nrows=0).columns.tolist()
            print(f"   colonne JOUR introuvable, colonnes du fichier : {colonnes}")
            continue
        print(f"   période du fichier : {jours.min().date()} -> {jours.max().date()}")
        if jours.min() >= pd.Timestamp(DEBUT) and jours.max() <= pd.Timestamp(FIN):
            trouve = True
            break
        print("   hors de la période étudiée, on essaie un autre jeu de données")
    if not trouve:
        print(f"   ATTENTION : aucun fichier valide pour le {t} trimestre, à télécharger à la main")

# 2. Profils horaires par jour type (un fichier par trimestre)
#    Ces fichiers n'ont pas de colonne de date : l'année est à vérifier sur le portail.
print("2. Profils horaires")
for t in TRIMESTRES:
    telecharger_idfm(f"validations-reseau-ferre-profils-horaires-par-jour-type-{t}-trimestre",
                     DOSSIER / NOMS_PROFILS[t])

# 3. Météo horaire à Paris (Open-Meteo), même format que ton fichier actuel
print("3. Météo")
nom_meteo = "open-meteo-48.89N2.29E36m.csv"
print(f" - {nom_meteo}")
telecharger("https://archive-api.open-meteo.com/v1/archive?latitude=48.89&longitude=2.29"
            f"&start_date={DEBUT}&end_date={FIN}"
            "&hourly=temperature_2m,precipitation,rain,weather_code"
            "&timezone=Europe%2FParis&format=csv",
            DOSSIER / nom_meteo)

# 4. Jours fériés de métropole (converti au même format CSV que ton fichier actuel)
print("4. Jours fériés")
print(" - jours_feries_metropole.csv")
try:
    r = requests.get("https://calendrier.api.gouv.fr/jours-feries/metropole.json", timeout=60)
    r.raise_for_status()
    feries = pd.DataFrame(list(r.json().items()), columns=["date", "nom_jour_ferie"])
    feries["annee"] = feries["date"].str[:4].astype(int)
    feries["zone"] = "Métropole"
    feries = feries[["date", "annee", "zone", "nom_jour_ferie"]].sort_values("date")
    feries.to_csv(DOSSIER / "jours_feries_metropole.csv", index=False)
    print(f"   OK ({len(feries)} jours fériés)")
except requests.RequestException as erreur:
    print(f"   échec : {erreur}")

# 5. Calendrier scolaire : fichier complet (le filtre sur Paris est fait par nettoyage.py)
print("5. Calendrier scolaire")
print(" - fr-en-calendrier-scolaire.csv")
fichier = DOSSIER / "fr-en-calendrier-scolaire.csv"
if telecharger("https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
               "fr-en-calendrier-scolaire/exports/csv?delimiter=%3B&use_labels=true", fichier):
    colonnes = pd.read_csv(fichier, sep=";", encoding="utf-8-sig", nrows=0).columns
    attendues = ["Description", "Population", "Date de début", "Date de fin", "Académies", "Zones"]
    manquantes = [c for c in attendues if c not in colonnes]
    if manquantes:
        print(f"   ATTENTION : colonnes absentes {manquantes}, nettoyage.py ne fonctionnera pas tel quel")

# 6. Matchs : pas de téléchargement automatique (calendrier du PSG, saisi à la main)
print("6. Matchs")
if (DOSSIER / "matchs_paris_2025_2026.csv").exists():
    print(" - matchs_paris_2025_2026.csv déjà présent")
else:
    print(" - ATTENTION : matchs_paris_2025_2026.csv est à placer dans le dossier (source : psg.fr)")

print("\nTerminé. Lance maintenant : python nettoyage.py")
