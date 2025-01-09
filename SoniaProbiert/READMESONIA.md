To Do 

### **1. Kategorienverwaltung**
- **Löschen von Kategorien**:
  - Aktuell können Kategorien gelöscht werden, jedoch fehlt die visuelle Rückmeldung (z. B. direktes Aktualisieren des Dropdowns).
  - Die Liste der Kategorien sollte nach dem Löschen dynamisch aktualisiert werden.

- **Kategorien-Duplikate verhindern**:
  - Es gibt bereits eine Prüfung auf Duplikate. Jedoch sollte dies für unterschiedliche Fälle (Groß-/Kleinschreibung) erweitert werden: `"DHBW"` ≠ `"dhbw"`.

---

### **2. Filter- und Sortierfunktionen**
- **Filter nach Kategorie und Priorität**:
  - Es fehlt eine Funktion, um Aufgaben in der Liste basierend auf einer Kategorie oder Priorität zu filtern.
  - Beispielsweise: Zeige nur **"Hohe Priorität"** oder nur Aufgaben der Kategorie **"DHBW"**.

- **Sortierung**:
  - Aufgaben sollten sortiert werden können, z. B. nach Fälligkeitsdatum oder Priorität.

---

### **3. Erinnerungen**
- Es fehlt die Implementierung einer **Erinnerungsfunktion**, die:
  - Benutzer über bevorstehende Fälligkeitsdaten informiert.
  - Erinnerungen in der Form von Pop-ups oder Benachrichtigungen bereitstellt.

---

### **4. Materialmanagement**
- **Dateianhänge oder Links zu Aufgaben**:
  - Die Möglichkeit, Dateien oder Links zu Aufgaben hinzuzufügen, ist nicht vorhanden.
  - Dies könnte über ein zusätzliches Feld oder eine Liste in der GUI umgesetzt werden.

---

### **5. Benutzeroberfläche**
- **Abbrechen-Button funktioniert nicht korrekt**:
  - Im aktuellen Code fehlt die Initialisierung des `self.cancel_button`. Das wurde oben bereits korrigiert.
  
- **Klarere Ansichten**:
  - Aufgabenansicht und Eingabemaske könnten deutlicher voneinander getrennt werden, z. B. durch Tabs oder Panels.
  
- **Dynamische Aktualisierungen**:
  - Änderungen an Kategorien oder Aufgaben sollten die GUI direkt aktualisieren, ohne dass eine manuelle Aktion (z. B. Neustart) nötig ist.

---

### **6. Fehlerbehebung**
- **Fehler bei der Bearbeitung von Aufgaben**:
  - Werte der ausgewählten Aufgabe werden nicht korrekt in die Eingabefelder geladen.
  - Der Fehler hängt damit zusammen, dass der `cancel_button` nicht initialisiert ist und die Logik zur Auswahl der Aufgaben nicht sauber umgesetzt wurde.

- **Logische Struktur der Module**:
  - Einige Funktionen sind möglicherweise redundant oder nicht optimal strukturiert (z. B. doppelte Definitionen von Methoden wie `change_value` in `core.py` und `models.py`).

---

### **7. Zusätzliche Funktionen**
- **Export/Import-Funktion**:
  - Exportieren oder Importieren von Aufgaben, z. B. in JSON- oder CSV-Format, ist eine sinnvolle Erweiterung.

- **Kalenderansicht**:
  - Die Funktion `show_calendar_view` ist ein Platzhalter. Eine tatsächliche Kalenderansicht könnte implementiert werden.

---

### Zusammenfassung: Was fehlt konkret?
1. **Filter und Sortierung** der Aufgaben.
2. **Erinnerungsfunktionen**.
3. **Dateianhänge oder Links** für Aufgaben.
4. Dynamische **GUI-Aktualisierung** (z. B. Dropdown-Menüs, Treeview).
5. Korrekte Initialisierung und Nutzung des **Abbrechen-Buttons**.
6. Eine funktionsfähige **Kalenderansicht**.
7. **Export-/Import-Optionen**.
