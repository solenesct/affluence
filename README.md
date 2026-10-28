# Affluence du métro parisien un soir de match de pluie : sources des données

Période étudiée : 1er juillet 2025 → 30 juin 2026.

## Validations journalières (IDFM)

| Fichier | Période | Source |
|---|---|---|
| `1er-trimestre-validations-reseau-ferre-nombre-validations-par-jour.csv` | 01/01 → 31/03/2026 | [data.gouv.fr](https://www.data.gouv.fr/datasets/search?q=validation+2025+1+trimestre) |
| `2eme-trimestre-validations-reseau-ferre-nombre-validations-par-jour-2eme-trimestre.csv` | 01/04 → 30/06/2026 | [IDFM Open Data](https://data.iledefrance-mobilites.fr/explore/dataset/validations-reseau-ferre-nombre-validations-par-jour-2eme-trimestre/export/) |
| `3eme-trimestre-validations-reseau-ferre-nombre-validations-par-jour.csv` | 01/07 → 30/09/2025 | [data.gouv.fr](https://www.data.gouv.fr/datasets/search?q=validation+2025+1+trimestre) |
| `4eme-trimestre-validations-reseau-ferre-nombre-validations-par-jour.csv` | 01/10 → 31/12/2025 | [data.gouv.fr](https://www.data.gouv.fr/datasets/search?q=validation+2025+1+trimestre) |

## Profils horaires par jour type (IDFM)

Part des validations par tranche horaire et par type de jour, pour chaque arrêt.

| Fichier | Source |
|---|---|
| `validations-reseau-ferre-profils-horaires-par-jour-type-1er-trimestre.csv` | [IDFM Open Data](https://data.iledefrance-mobilites.fr/explore/dataset/validations-reseau-ferre-profils-horaires-par-jour-type-1er-trimestre/export/) |
| `validations-reseau-ferre-profils-horaires-par-jour-type-2eme-trimestre.csv` | [IDFM Open Data](https://data.iledefrance-mobilites.fr/explore/dataset/validations-reseau-ferre-profils-horaires-par-jour-type-2eme-trimestre/export/) |
| `validations-reseau-ferre-profils-horaires-par-jour-type-3eme-trimestre.csv` | [IDFM Open Data](https://data.iledefrance-mobilites.fr/explore/dataset/validations-reseau-ferre-profils-horaires-par-jour-type-3eme-trimestre/export/) |
| `4eme-trimestre-validations-reseau-ferre-profils-horaires-par-jour-type-4eme-trimestre.csv` | [IDFM Open Data](https://data.iledefrance-mobilites.fr/explore/dataset/validations-reseau-ferre-profils-horaires-par-jour-type-4eme-trimestre/export/) |

Colonnes : `CODE_STIF_TRNS`, `CODE_STIF_RES`, `CODE_STIF_ARRET`, `ID_ZDC`, `LIBELLE_ARRET`, `CAT_JOUR`, `TRNC_HORR_60`, `Pourcentage_validations`.
Ces fichiers n'ont pas de colonne de date : l'année de chaque trimestre est à confirmer sur la page de téléchargement.

## Autres données

| Fichier | Contenu | Source |
|---|---|---|
| `open-meteo-48.89N2.29E36m.csv` | Météo horaire (température, précipitations, code météo), 2025 uniquement | [Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api) |
| `fr-en-calendrier-scolaire.csv` | Vacances scolaires | [data.gouv.fr](https://www.data.gouv.fr/datasets/le-calendrier-scolaire) |
| `jours_feries_metropole.csv` | Jours fériés en métropole | [data.gouv.fr](https://www.data.gouv.fr/dataservices/jours-feries) |
| `matchs_paris_2025_2026.csv` | 27 matchs du PSG à Paris | [psg.fr](https://www.psg.fr/en/mens-football/fixtures/season/2025-26) |

