## **Projektplanung — Systemsicherheit implementieren**

### 1. Projektdefinition

Thema:
Absicherung eines Linux-Servers mit sicherer Webanwendung (Registrierung, Login, Zwei-Faktor-Authentifizierung).

Projektziel:
Ein System entwickeln, das zeigt, wie Sicherheitsmaßnahmen sowohl auf Betriebssystem- als auch auf Anwendungsebene praktisch umgesetzt werden können.

Der Fokus liegt nicht auf der Komplexität der Anwendung, sondern auf der Integration sicherheitsrelevanter Mechanismen wie Systemhärtung, Authentifizierung, Verschlüsselung und Zugriffsschutz.

---

### 2. Theoretische Grundlage

#### 2.1. Sicherheitsprinzipien

Das Projekt basiert auf den fundamentalen Prinzipien der IT-Sicherheit:

* Vertraulichkeit (Confidentiality): Schutz von Daten vor unbefugtem Zugriff.
* Integrität (Integrity): Sicherstellen, dass Daten unverändert und authentisch bleiben.
* Verfügbarkeit (Availability): Systeme müssen trotz Angriffen oder Ausfällen erreichbar bleiben.

Diese drei Prinzipien bilden das sog. CIA-Triade-Modell (Quelle: ISO/IEC 27001:2022, Annex A).

---

### 3. Ressourcenplanung

#### 3.1. Cloud-Infrastruktur

Ziel: Bereitstellung einer kontrollierten, realistischen Umgebung für Sicherheitsmaßnahmen.
Theorie:

* Azure Virtual Machines bieten reproduzierbare, skalierbare Umgebungen mit dedizierter Netzwerk- und Sicherheitskonfiguration.
* Infrastructure as Code (IaC) mit Terraform ermöglicht konsistente Bereitstellung, Wiederholbarkeit und Versionierung der Infrastruktur (Quelle: HashiCorp Terraform Documentation, 2024).
* Linux (Ubuntu LTS) wird eingesetzt, da es eine stabile und sicherheitsfokussierte Serverplattform mit Langzeit-Support bietet.

Sicherheitsaspekte:

* SSH-Authentifizierung ausschließlich über Public Key (asymmetrische Kryptographie, RFC 4251).
* Netzwerksicherheitsgruppen (NSG) zur Einschränkung von eingehendem Verkehr (Firewall auf Azure-Ebene).
* Unattended Upgrades für automatische Sicherheitspatches auf Betriebssystemebene.

---

#### 3.2. Betriebssystem- und Netzwerksicherheit

Ziel: Minimierung der Angriffsfläche des Servers.

Theorie:

* Systemhärtung (Hardening): Entfernen unnötiger Dienste, Einschränkung von Zugriffsrechten, Logging und Intrusion Detection (Quelle: CIS Benchmarks — Ubuntu Linux 22.04/24.04).
* Firewall (UFW): Implementierung des “default deny” Prinzips: Alles blockieren, nur notwendige Ports erlauben.
* Fail2Ban: Schutz gegen Brute-Force-Angriffe durch IP-Blocking nach wiederholtem Fehlversuch (Quelle: fail2ban.readthedocs.io).
* Auditd: Logt sicherheitsrelevante Systemereignisse (Dateiänderungen, sudo, Authentifizierungen).

Diese Maßnahmen dienen dazu, Schutz in Tiefe (Defense in Depth) umzusetzen — also mehrere Sicherheitsebenen, die sich gegenseitig absichern.

---

#### 3.3. Webserver & Reverse Proxy

Ziel: Sicherer Zugriff auf die Webapplikation über HTTPS.

Theorie:

* Nginx fungiert als Reverse Proxy zwischen Internet und Anwendung.

  * Filtert eingehenden Verkehr.
  * Terminiert TLS (Transport Layer Security).
  * Erzwingt HTTPS-Verbindungen (Redirect von Port 80 auf 443).
  * TLS-Zertifikate über Let’s Encrypt (Certbot) stellen eine kostenlose, automatisierte und sichere HTTPS-Verschlüsselung bereit.
  * Content Security Policy (CSP): Steuert, von welchen Quellen Skripte, Bilder und Styles geladen werden dürfen – Schutz gegen XSS (Cross-Site Scripting).

  * Beispielrichtlinie:

    ```nginx
    add_header Content-Security-Policy "default-src 'self' data:; style-src 'self' 'unsafe-inline'; img-src 'self' data:;" always;
    ```

  (Quelle: Mozilla Web Security Guidelines, CSP Level 3).

---

#### 3.4. Anwendungssicherheit

Ziel: Aufbau einer sicheren Authentifizierungsarchitektur.

Theorie:
Die Anwendung soll zeigen, wie Benutzerverwaltung und Schutz auf Anwendungsebene umgesetzt werden:

| Sicherheitskomponente                | Beschreibung                                                                                           | Theoretische Grundlage               |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------ |
| **bcrypt Hashing**                   | Passwörter werden vor der Speicherung mit einem Salt gehasht, um Rainbow Table-Angriffe zu verhindern. | NIST SP 800-63B §5.1.1.2             |
| **Session Handling**                 | Serverseitige Speicherung der User-ID nach erfolgreichem Login; Cookie mit Secure-Flag.                | OWASP Session Management Cheat Sheet |
| **2-Faktor-Authentifizierung (2FA)** | Nutzung von TOTP (Time-based One-Time Password) per Authenticator-App.                                 | RFC 6238 (TOTP Algorithm)            |
| **Rate Limiting**                    | Begrenzung von Requests pro Minute gegen Brute-Force-Angriffe.                                         | OWASP API Security Top 10 – A7:2023  |
| **CSRF-Schutz**                      | Jeder POST-Request enthält Token gegen Cross-Site Request Forgery.                                     | OWASP CSRF Prevention Cheat Sheet    |

Frameworks und Libraries:

* Flask (Python Web Framework)
* Flask-Limiter (Request Throttling)
* PyOTP (TOTP-Algorithmus)
* bcrypt (Passworthashing)

Diese Komponenten ermöglichen eine praxisnahe Demonstration von Secure Authentication & Access Control gemäß OWASP Application Security Verification Standard (ASVS) Level 1–2.

---

#### 3.5. Design & User Experience

Ziel: Einheitliches, sicheres und nachvollziehbares Benutzerinterface.

Theorie:

* Minimalismus in UI = weniger Angriffsfläche (keine externen Ressourcen, kein JavaScript von Drittanbietern).
* Dark Theme Design: Fokus auf Lesbarkeit und Sicherheit.
* Einheitliches Layout (Card-System) für Login, Registrierung, Dashboard, Fehlerseiten.
* CSP-konformes Inline-CSS (lokal eingebettet, keine CDN-Abhängigkeiten).

(Quelle: OWASP Secure Design Principles, 2023).

---

#### 3.6. Logging & Monitoring

Ziel: Nachvollziehbarkeit von sicherheitsrelevanten Ereignissen.

Theorie:

* Auditd: Systemüberwachung auf Root-Ebene.
* Gunicorn Logging: Application-Level Logs für Requests und Fehler.
* Nginx Access Logs: Nachvollziehbarkeit von Zugriffen über HTTPS.
* Fail2Ban Logs: dokumentiert geblockte IPs und Zeitpunkte.

Damit lässt sich im Projekt zeigen, wie unterschiedliche Ebenen von Logging zusammenwirken, um Angriffsversuche sichtbar zu machen (Security Observability).

---

### 4. Zeit- und Ablaufplanung

| Phase                             | Beschreibung                                              | Zeitrahmen | Ergebnis                             |
| --------------------------------- | --------------------------------------------------------- | ---------- | ------------------------------------ |
| **1. Planung & Konzept**          | Definition von Zielen, Architektur, Sicherheitsprinzipien | Woche 1    | Theoriekonzept (diese Dokumentation) |
| **2. Infrastrukturaufbau**        | Terraform-Skripte, Azure-VM, SSH-Setup, Firewall          | Woche 2    | Gehärtete Linux-VM                   |
| **3. Serverhärtung & Monitoring** | Fail2Ban, Auditd, unattended-upgrades                     | Woche 3    | Stabiler, abgesicherter Server       |
| **4. Webserver & HTTPS**          | Nginx-Konfiguration, TLS-Zertifikate, CSP                 | Woche 4    | HTTPS-Zugriff aktiv                  |
| **5. App-Entwicklung & Auth**     | Registrierung, Login, 2FA, Sessions                       | Woche 5    | Funktionale, sichere Web-App         |
| **6. Design & Benutzerführung**   | Einheitliches UI, Dashboard, Fehlerseiten                 | Woche 6    | Benutzerfreundliches Interface       |
| **7. Test & Dokumentation**       | Funktionstests, Sicherheitsüberprüfung, Bericht           | Woche 7    | Vollständige Projektdokumentation    |

---

### 5. Quellenverzeichnis

Allgemeine Sicherheit & Theorie:

* ISO/IEC 27001:2022 – Information Security Management
* OWASP Foundation: [https://owasp.org/](https://owasp.org/)
* NIST SP 800-63B: Digital Identity Guidelines
* CIS Benchmarks – Ubuntu Linux 22.04/24.04
* Mozilla Developer Network (MDN): CSP Reference
* HashiCorp Terraform Docs – Infrastructure as Code
* Microsoft Azure Security Baseline for Linux VMs

Technische Frameworks:

* Flask Framework: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* Gunicorn: [https://gunicorn.org/](https://gunicorn.org/)
* Nginx Docs: [https://nginx.org/](https://nginx.org/)
* PyOTP (RFC 6238 Implementation): [https://pyauth.github.io/pyotp/](https://pyauth.github.io/pyotp/)
* bcrypt Python: [https://pypi.org/project/bcrypt/](https://pypi.org/project/bcrypt/)
* Fail2Ban Documentation: [https://fail2ban.readthedocs.io](https://fail2ban.readthedocs.io)

---

### 6. Zusammenfassung

Die Projektplanung definiert den theoretischen Rahmen für die Umsetzung einer sicheren, gehärteten und nachvollziehbar geschützten Systemarchitektur.
Sie zeigt, welche Sicherheitsmechanismen warum eingesetzt werden und auf welchen Standards diese basieren.

Die praktische Umsetzung in späteren Phasen folgt exakt dieser Planung und validiert, dass theoretisch bekannte Schutzmechanismen (SSH-Härtung, TLS, bcrypt, TOTP, CSP) in der Praxis erfolgreich und reproduzierbar implementiert werden können.
