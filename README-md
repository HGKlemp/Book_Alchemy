# 📚 Book Alchemy

**Book Alchemy** ist eine Flask-Webanwendung zur Verwaltung einer digitalen Bibliothek.

Mit der Anwendung können Autoren und Bücher in einer Datenbank gespeichert und über eine Weboberfläche verwaltet werden. Die Datenbankanbindung erfolgt mit **Flask-SQLAlchemy**.

---

## Funktionen

Die Anwendung bietet folgende Funktionen:

* Autoren hinzufügen
* Bücher hinzufügen
* Bücher und zugehörige Autoren anzeigen
* Bücher nach Titel suchen
* Bücher alphabetisch nach Titel sortieren
* Bücher nach Autor sortieren
* Bücher löschen
* Automatisches Löschen eines Autors, wenn dessen letztes Buch gelöscht wurde
* Dauerhafte Speicherung der Daten in einer SQLite-Datenbank

---

## Verwendete Technologien

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* SQLite
* HTML
* Jinja2

---

## Projektstruktur

```text
Book_Alchemy/
│
├── app.py
├── data_models.py
├── main.py
│
├── data/
│   └── library.sqlite
│
└── templates/
    ├── home.html
    ├── add_author.html
    └── add_book.html
```

### `app.py`

Enthält die Flask-Anwendung sowie die verschiedenen Routen der Webanwendung.

Dazu gehören unter anderem:

* Startseite
* Suche
* Sortierung
* Autoren hinzufügen
* Bücher hinzufügen
* Bücher löschen

### `data_models.py`

Enthält die SQLAlchemy-Datenmodelle `Author` und `Book` sowie deren Beziehung zueinander.

### `templates/`

Enthält die HTML-Templates für die Weboberfläche.

---

## Datenbank

Die Anwendung verwendet eine SQLite-Datenbank.

Die Datenbank befindet sich unter:

```text
data/library.sqlite
```

Die benötigten Tabellen werden beim Start der Anwendung automatisch mit SQLAlchemy erstellt.

---

## Datenmodelle

### Author

Das Modell `Author` speichert die Informationen zu einem Autor.

Gespeicherte Daten:

* ID
* Name
* Geburtsdatum
* optionales Todesdatum

Ein Autor kann mehrere Bücher besitzen.

### Book

Das Modell `Book` speichert die Informationen zu einem Buch.

Gespeicherte Daten:

* ID
* ISBN
* Titel
* Erscheinungsjahr
* Autor

Jedes Buch ist über einen Foreign Key mit einem Autor verbunden.

---

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/HGKlemp/Book_Alchemy.git
```

### 2. In das Projektverzeichnis wechseln

```bash
cd Book_Alchemy
```

### 3. Benötigte Python-Pakete installieren

```bash
pip install flask flask-sqlalchemy
```

---

## Anwendung starten

Für die Ausführung der Anwendung in **Codio** wird folgender Befehl verwendet:

```bash
flask run --host=0.0.0.0 --port=5002
```

Die Anwendung läuft damit auf **Port 5002**.

Der Port sollte für die Ausführung in Codio nicht verändert werden.

Für eine lokale Ausführung kann die Anwendung alternativ mit folgendem Befehl gestartet werden:

```bash
python app.py
```

---

## Bedienung

Nach dem Start der Anwendung wird auf der Startseite die gespeicherte Buchsammlung angezeigt.

### Autor hinzufügen

Über **Add Author** kann ein neuer Autor angelegt werden.

Dabei werden folgende Informationen erfasst:

* Name
* Geburtsdatum
* optionales Todesdatum

### Buch hinzufügen

Über **Add Book** kann einem vorhandenen Autor ein neues Buch zugeordnet werden.

Dabei werden folgende Informationen gespeichert:

* ISBN
* Titel
* Erscheinungsjahr
* Autor

### Bücher suchen

Auf der Startseite können Bücher anhand ihres Titels gesucht werden.

### Bücher sortieren

Die Buchliste kann alphabetisch nach Titel oder nach Autor sortiert werden.

### Buch löschen

Ein Buch kann direkt aus der Bibliothek gelöscht werden.

Wird das letzte vorhandene Buch eines Autors gelöscht, wird auch der zugehörige Autor automatisch aus der Datenbank entfernt.

---

## Beziehung zwischen Autoren und Büchern

Zwischen `Author` und `Book` besteht eine **One-to-Many-Beziehung**.

```text
Author
   │
   │ 1
   │
   └─────────────── *
                     Book
```

Ein Autor kann mehrere Bücher besitzen, während jedes Buch genau einem Autor zugeordnet ist.

Die Zuordnung erfolgt über:

```python
author_id = db.Column(
    db.Integer,
    db.ForeignKey("authors.id"),
    nullable=False
)
```

---

## Ziel des Projekts

Ziel des Projekts ist es, den Umgang mit folgenden Technologien und Konzepten praktisch anzuwenden:

* Flask
* SQLAlchemy
* relationale Datenbanken
* Datenmodelle
* One-to-Many-Beziehungen
* Foreign Keys
* CRUD-Operationen
* Flask-Routing
* HTML-Templates mit Jinja2
* Verarbeitung von Formularen
* Suche und Sortierung von Datenbankeinträgen

---

## Autor

**Hans-Günter Klemp**

GitHub:
https://github.com/HGKlemp

---

## Repository

Book Alchemy auf GitHub:

https://github.com/HGKlemp/Book_Alchemy
