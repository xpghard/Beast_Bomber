import os
import subprocess
import requests
import json
from datetime import datetime

# ustawienia projektu
REPO_URL = 'https://github.com/un1cum/Beast_Bomber.git'
PROJECT_DIR = os.getcwd()
VERSION_FILE = 'version.txt'

# funkcja pobierająca najnowszą wersję z Githuba
def update_project():
    # sprawdzenie daty ostatniej aktualizacji projektu
    os.chdir(PROJECT_DIR)
    try:
        git_log = subprocess.check_output(['git', 'log', '-1', '--format=%cd'], stderr=subprocess.STDOUT)
        last_updated = datetime.strptime(git_log.decode().strip(), '%a %b %d %H:%M:%S %Y %z')
    except subprocess.CalledProcessError as e:
        print(f'Błąd podczas wykonywania polecenia "git log": {e.output.decode()}')
        last_updated = None
    # sprawdzenie daty najnowszej wersji na Githubie
    repo_url = REPO_URL[:-4] if REPO_URL.endswith('.git') else REPO_URL
    try:
        response = requests.get(repo_url)
        print(response)
        response.raise_for_status()  # rzuć wyjątek, jeśli otrzymana odpowiedź zawiera błędy
        latest_version_date = datetime.strptime(response.json()['published_at'], '%Y-%m-%dT%H:%M:%S%z')
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f'Błąd podczas pobierania najnowszej wersji z Githuba: {e}')
        latest_version_date = None
    # porównanie dat i pobranie najnowszej wersji, jeśli daty się różnią
    if latest_version_date and latest_version_date > last_updated:
        subprocess.call(['git', 'pull'])
        with open(os.path.join(PROJECT_DIR, VERSION_FILE), 'w') as f:
            f.write(latest_version_date.strftime('%Y%m%d'))
        print(f'Projekt został zaktualizowany do wersji z {latest_version_date}')
    elif last_updated:
        print(f'Projekt jest już aktualny (ostatnia aktualizacja: {last_updated})')
    else:
        print('Nie można ustalić daty ostatniej aktualizacji projektu.')

update_project()

# dalszy kod Twojego programu
