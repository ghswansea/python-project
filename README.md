🧱 1. Ce que tu vas construire
🧰 Tool CLI (ligne de commande)
python log_analyzer.py logs.txt

👉 Output :

résumé dans le terminal
fichier report.html
📄 2. Exemple de logs (simple)

Crée un fichier logs.txt :

2026-04-07 10:00:01 INFO Service started
2026-04-07 10:01:15 ERROR Database connection failed
2026-04-07 10:02:20 WARNING High memory usage
2026-04-07 10:03:05 ERROR Timeout on API call
2026-04-07 10:04:10 INFO Request processed
⚙️ 3. Fonctionnalités à implémenter
✅ Analyse
compter :
nombre de ERROR
nombre de WARNING
nombre de INFO
✅ Détection
extraire toutes les lignes ERROR
détecter les erreurs fréquentes
✅ Output console

Exemple :

Total lines: 5
ERROR: 2
WARNING: 1
INFO: 2
✅ Génération HTML (clé 💥)

Créer un fichier report.html :

tableau des erreurs
stats globales
🧑‍💻 4. Structure du projet (simple et propre)
log-tool/
│── log_analyzer.py
│── logs.txt
│── templates/
│     └── report.html.j2