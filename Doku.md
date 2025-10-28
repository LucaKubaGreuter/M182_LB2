## **Projektdokumentation — Systemsicherheit implementieren**

### **1. Projektübersicht**

**Thema:**
Absicherung eines Linux-Servers mit einer sicheren Webanwendung.

**Zielsetzung:**

* Bereitstellung und Härtung eines Linux-Servers in Azure nach Security-Best-Practices.
* Umsetzung von Sicherheitsmechanismen auf Betriebssystem- und Anwendungsebene.
* Entwicklung einer sicheren Webapplikation mit moderner Authentifizierung (Login, Passwort-Hashing, Zwei-Faktor-Authentifizierung).

---

### **2. Infrastrukturaufbau mit Terraform**

Die Serverinfrastruktur wurde vollständig automatisiert mit **Terraform** in **Azure** erstellt.

**Wichtige Punkte der Infrastruktur:**

* **Resource Group:** `rg-lucgr-001`
* **Region:** North Europe (nahegelegen, kostengünstig)
* **Virtuelles Netzwerk** mit Subnetz für die Web-VM
* **Network Security Group (NSG):**

  * SSH (Port 22) — nur bei Bedarf IP-beschränkt
  * HTTP (80), HTTPS (443) — für Webzugriff
* **Linux-VM:** Ubuntu 24.04 LTS
* **Benutzer:** `secadmin`
* **Authentifizierung:** ausschließlich SSH-Key (keine Passwörter)
* **Managed Identity:** aktiviert für spätere Integrationen
* **Öffentliche IP:** für Zugriff auf Webanwendung

**SSH-Key Handling:**

* SSH-Key lokal mit `ssh-keygen -t ed25519` erstellt.
* Nur der Public Key wurde an Terraform übergeben.
* Passwort-Authentifizierung ist vollständig deaktiviert.

**Automatisiertes Hardening via cloud-init:**
Beim Deployment wurde ein Skript eingebunden, das die grundlegenden Sicherheitsmaßnahmen automatisiert aktivierte:

* **SSH-Härtung:**

  * Root-Login deaktiviert
  * Passwort-Authentifizierung deaktiviert
  * Authentifizierungsversuche limitiert

* **Firewall (UFW):**

  * Default: inbound `deny`
  * Erlaubt: SSH, HTTP, HTTPS

* **Fail2Ban:**

  * Schutz vor Brute-Force-Angriffen auf SSH

* **Unattended-Upgrades:**

  * Automatische Installation sicherheitsrelevanter Updates

* **Auditd:**

  * Aktiv für Sicherheits- und Systemlogging

* **Nginx (Reverse Proxy):**

  * Installiert und minimal gehärtet
  * Grundlage für HTTPS, Proxy-Routing, CSP

---

### **3. Zugriff & Tests**

Nach Bereitstellung:

```bash
terraform output ssh_command
ssh -i ~/.ssh/id_ed25519 secadmin@172.161.18.141
```

**Prüfungen:**

* Firewall:

  ```bash
  sudo ufw status verbose
  ```

  → `active`, Ports 22/80/443 erlaubt.

* Fail2Ban:

  ```bash
  sudo fail2ban-client status sshd
  ```

  → aktiv, keine Sperrungen.

* Automatische Updates:

  ```bash
  systemctl status unattended-upgrades
  ```

  → läuft korrekt.

* Auditd:

  ```bash
  sudo auditctl -s
  ```

  → Audit-Framework aktiv.

---

### **4. Sicherheit & Gründe**

* **SSH-Keys statt Passwörter:** verhindert Brute-Force-Angriffe.
* **Firewall + NSG:** doppelte Netzsicherung (Azure + OS).
* **Fail2Ban:** dynamische Sperre bei wiederholten Login-Versuchen.
* **Unattended-Upgrades:** sichert aktuelle Patches ohne manuellen Aufwand.
* **Auditd:** volle Nachvollziehbarkeit sicherheitsrelevanter Ereignisse.
* **Nginx-Härtung:** minimierte Angriffsfläche.

---

### **5. Entwicklung der sicheren Webanwendung**

#### **Technologie**

* Framework: Flask (Python 3.12)
* Reverse Proxy: Nginx
* Application Server: Gunicorn (über systemd-Dienst)
* Datenbank: SQLite (lokal, verschlüsselt über Dateiberechtigungen)

#### **Funktionalität**

1. **Registrierung mit Passwort-Hashing:**

   * Speicherung von Passwörtern nur als bcrypt-Hash (mit Salt).
   * Mindestpasswortlänge: 8 Zeichen.

2. **Zwei-Faktor-Authentifizierung (2FA):**

   * Nach Registrierung wird automatisch ein TOTP-Secret generiert.
   * QR-Code für Authenticator-App (z. B. Google Authenticator) wird angezeigt.
   * Beim Login wird zusätzlich ein 6-stelliger Code abgefragt.

3. **Login mit Session Handling:**

   * Session-ID wird serverseitig gespeichert.
   * Login nur bei gültigem Passwort und gültigem 2FA-Code möglich.

4. **Account-Verwaltung:**

   * Eingeloggte Benutzer können ihren Account löschen (`/delete_account`).
   * Löschung entfernt Datensatz vollständig aus der DB und beendet Session.

5. **Geschützter Dashboard-Bereich:**

   * Nur für eingeloggte Benutzer sichtbar.
   * Anzeige eines Beispielbildes (`/static/dashboard.jpg`).
   * Übersichtliche Card-Struktur im Dark-Theme.

---

### **6. Design & Sicherheit auf Anwendungsebene**

#### **Visuelles Design**

* Einheitliches **Dark Theme** (CSS in `base.html` eingebettet).
* Konsistente Struktur über alle Seiten: Register, Login, QR-Setup, Dashboard, Unauthorized.
* CSP-konform ohne externe CSS/JS-Bibliotheken.
* Responsives Layout mit Fokus auf Lesbarkeit und Sicherheit.

#### **CSP (Content Security Policy)**

```nginx
add_header Content-Security-Policy \
"default-src 'self' data:; img-src 'self' data:; style-src 'self' 'unsafe-inline';" always;
```

* Nur lokale Ressourcen erlaubt (`'self'`).
* `data:`-URIs nur für QR-Codes.
* Inline-CSS ausdrücklich erlaubt, kein externes JS.
* Keine Skripte, keine Frames → Minimale Angriffsfläche.

#### **Weitere Härtung**

* **Gunicorn** läuft als systemd-Service, dauerhaft aktiv.
* **Nginx Proxy** bindet an HTTPS (Let's Encrypt-Zertifikat via Certbot).
* **Fail2Ban** schützt weiterhin gegen Angriffe auf Port 22.

---

### **7. Fehlerbehandlung & Benutzerführung**

* **Unauthorized-Zugriff (401):**

  * Eigene Seite `unauthorized.html` im Dark-Theme.
  * Zeigt strukturierte Fehlermeldung und sicheren Rücklink zu `/login`.
  * Keine technischen Details, keine sensiblen Daten in Fehlerausgabe.

* **Double Registration (Duplicate Email):**

  * Wird abgefangen, Nutzer bekommt Meldung „User existiert bereits“.

* **Ungültiger 2FA-Code:**

  * Fehlermeldung „2FA required or invalid“, kein Hinweis auf Passwortgültigkeit.

---

### **8. Lessons Learned**

* CSP muss exakt abgestimmt werden – zu restriktiv blockiert auch interne Styles.
* QR-Codes über Base64 `data:`-URIs funktionieren sicherer als temporäre Files.
* systemd-Integration von Gunicorn ist essenziell, damit App dauerhaft läuft.
* 2FA über `pyotp` ist leicht integrierbar, erhöht aber massiv die Sicherheit.
* Einheitliches CSS vereinfacht Sicherheit, reduziert Komplexität.
* Nginx als Reverse Proxy ist Pflicht für HTTPS, CSP und statische Auslieferung.

---

### **9. Fazit**

Das Projekt zeigt eine vollständige Umsetzung von **Systemsicherheit auf Infrastruktur- und Anwendungsebene**:

* **Infrastruktur:** automatisch gehärtet, sicher, wartungsarm.
* **Webapplikation:** modern, geschützt durch bcrypt + 2FA + sichere Sessions.
* **Sichtbarer Sicherheitsnachweis:** QR-Setup, Login mit Authenticator, gesperrte Bereiche.
* **Design:** konsistent, Dark-Theme, CSP-konform.
* **Betrieb:** stabil über systemd, überwacht durch Nginx und Firewall.

**Ergebnis:**
Ein vollständig gehärteter Linux-Webserver mit sicherer, ästhetischer und funktionaler Webanwendung, die moderne Authentifizierungsmechanismen umsetzt und dabei den Fokus auf reale Angriffsszenarien und Schutzmaßnahmen legt.
