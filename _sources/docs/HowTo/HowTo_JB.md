# How-To Jupyter-Book (GitHub-Pages) erstellen

[Offizielle JupyterBook Dokumentation](https://jupyterbook.org/intro.html)

## Installation der Tools und Konfiguration

* `Jupyter Book` installieren mit `pip install -U jupyter-book` 
   
* Einstellungen sind in `_config.yml`
    - [Hinweise zu _config.yml von der offiziellen Webseite](https://jupyterbook.org/customize/config.html)
	
* Ordnen der Dokumente über das Inhaltsverzeichnis in `_toc.yml`
    - [Hinweise zu _toc.yml von der offiziellen Webseite](https://jupyterbook.org/customize/toc.html)

## Jupyter-Book kompilieren und veröffentlichen

* Zum Erstellen des Jupyter-Books im Verzeichnis des geklonten Repositoriums: `jupyter-book build .` im Terminal ausführen
    - unter `_build/html/index.html` kann das Jupyter-Book lokal betrachtet werden

* ghp-import installieren mit `pip install ghp-import`

* `ghp-import -n -p -f _build/html` im Verzeichnis des geklonten Repositoriums ausführen
	- dadurch werden die Inhalte des Jupyter-Books automatisch in die Branch `gh-pages` des Git-repo ge-push-t
