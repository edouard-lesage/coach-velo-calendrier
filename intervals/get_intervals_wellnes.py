"""Export des données bien-être intervals.icu vers un CSV.

Usage :
    python intervals/get_intervals_wellnes.py                      # 90 derniers jours (aujourd'hui inclus)
    python intervals/get_intervals_wellnes.py --oldest 2026-11-01 --newest 2026-11-12
    python intervals/get_intervals_wellnes.py --oldest 2026-11-01 --newest 2026-11-12 --output mon_fichier.csv

Identifiants lus dans le fichier .env ou les variables d'environnement :
    INTERVALS_ATHLETE_ID  (ex. i123456)
    INTERVALS_API_KEY     (Réglages intervals.icu > Developer Settings)

Dépendances : pip install requests pandas python-dotenv
"""

import argparse
import os
import sys
from datetime import date, timedelta

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()  # lit le .env du projet ; les variables déjà définies dans le shell restent prioritaires

BASE_URL = "https://intervals.icu/api/v1"
COLUMNS = [
    "id",
    "updated",
    "restingHR",
    "hrv",
    "sleepSecs",
    "sleepScore",
    "sleepQuality",
    "steps",
    "floorsClimbed",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export bien-être intervals.icu -> CSV")
    parser.add_argument("--oldest", type=date.fromisoformat,
                        help="Date de début incluse (AAAA-MM-JJ, défaut : newest - 89 jours)")
    parser.add_argument("--newest", type=date.fromisoformat,
                        help="Date de fin incluse (AAAA-MM-JJ, défaut : aujourd'hui)")
    parser.add_argument("--output", help="Chemin du CSV (défaut : wellness_<oldest>_<newest>.csv)")
    args = parser.parse_args()
    if args.newest is None:
        args.newest = date.today()
    if args.oldest is None:
        args.oldest = args.newest - timedelta(days=89)
    if args.oldest > args.newest:
        parser.error("--oldest doit être antérieure ou égale à --newest")
    return args


def get_credentials() -> tuple[str, str]:
    athlete_id = os.environ.get("INTERVALS_ATHLETE_ID")
    api_key = os.environ.get("INTERVALS_API_KEY")
    if not athlete_id or not api_key:
        sys.exit("Erreur : définir INTERVALS_ATHLETE_ID et INTERVALS_API_KEY.")
    return athlete_id, api_key


def fetch_wellness(athlete_id: str, api_key: str, oldest: date, newest: date) -> list[dict]:
    url = f"{BASE_URL}/athlete/{athlete_id}/wellness"
    params = {"oldest": oldest.isoformat(), "newest": newest.isoformat()}
    resp = requests.get(url, params=params, auth=("API_KEY", api_key), timeout=30)
    if resp.status_code == 401:
        sys.exit("Erreur 401 : clé API ou identifiant d'athlète incorrect.")
    resp.raise_for_status()
    return resp.json()


def to_dataframe(records: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    # reindex : garantit toutes les colonnes, même si l'API n'en renvoie aucune valeur
    df = df.reindex(columns=COLUMNS)
    if not df.empty:
        df = df.sort_values("id").reset_index(drop=True)
    return df


def main() -> None:
    args = parse_args()
    athlete_id, api_key = get_credentials()

    records = fetch_wellness(athlete_id, api_key, args.oldest, args.newest)
    df = to_dataframe(records)

    output = args.output or f"wellness_latest.csv"
    df.to_csv(output, index=False, encoding="utf-8")
    print(f"{len(df)} jour(s) exporté(s) -> {output}")


if __name__ == "__main__":
    main()