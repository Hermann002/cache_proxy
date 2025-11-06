# Caching Proxy

Un petit serveur proxy de mise en cache (GET-only) écrit en Python.

Ce dépôt fournit une application simple qui relaie les requêtes vers un serveur d'origine
et met en cache les réponses localement pour accélérer les requêtes suivantes.

## Prérequis

- Python 3.8 ou plus
- pip
- (optionnel) virtualenv/venv

## Installation

1. Cloner le dépôt :

```bash
git clone <repo-url> caching-proxy
cd caching-proxy
```

2. (Recommandé) Créer et activer un environnement virtuel :

```bash
python -m venv env
source env/bin/activate
```

3. Installer le package en mode editable (installe le script CLI) :

```bash
pip install -e .
```

Après l'installation, le script CLI `caching-proxy` est disponible dans l'environnement.

## Usage

Le point d'entrée CLI est `caching-proxy` (défini dans `setup.py`).

- Démarrer le proxy (exemple) :

```bash
caching-proxy --port 8000 --origin http://dummyjson.com
```

- Démarrer via le module (sans installation) :

```bash
python -m cache_proxy --port 8000 --origin http://dummyjson.com
```

- Effacer le cache local :

```bash
caching-proxy --clear-cache
```

Remarques importantes :
- Les options `--port` et `--origin` sont requises sauf si vous utilisez `--clear-cache`.
- L'argument `--origin` doit commencer par `http://` ou `https://`.

## Fichier de cache

Le cache est stocké dans le fichier `.caching_proxy_cache.pkl` à la racine du projet (variable `CACHE_FILE`).
Le CLI affiche le chemin absolu du fichier de cache au démarrage.

## Exemple rapide

1. Démarrez le proxy :

```bash
source env/bin/activate   # si vous avez créé un venv
caching-proxy --port 8000 --origin https://httpbin.org
```

2. Testez via curl :

```bash
curl http://localhost:8000/get
```

La première requête sera transmise à l'origine et mise en cache ; les suivantes seront servies depuis le cache.

## Tests simples

Le dépôt contient un petit fichier `cache_proxy/test.py` (script de démonstration). Pour l'exécuter :

```bash
python -m cache_proxy.test
```

Ce script n'est pas une suite de tests automatisés (pytest), c'est un utilitaire d'exemple/démo.

## Dépannage

- Si vous obtenez des erreurs d'import, vérifiez que vous utilisez le bon environnement virtuel et que
	le package a été installé (`pip install -e .`).
- Si le fichier de cache est corrompu ou que vous voulez repartir de zéro, utilisez `--clear-cache`.

## Notes et améliorations possibles

- Le proxy gère uniquement les requêtes GET pour l'instant.
- Améliorations possibles : gestion des en-têtes HTTP, invalidation fine du cache, stockage persistant plus robuste, tests automatisés.

---

Rédigé pour le projet d'exercice — instructions minimales pour installation et exécution.


- roadmap project url: https://roadmap.sh/projects/caching-server