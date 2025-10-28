# Projektarbeit: Systemsicherheit implementieren

## Thema
Absicherung eines Linux-Servers mit einer sicheren Webanwendung (Registrierung, Login, Zwei-Faktor-Authentifizierung).

## Beschreibung
Im Rahmen unserer Projektarbeit möchten wir einen Linux-Server härten und darauf eine Web-App implementieren, die grundlegende Sicherheitsfunktionen enthält.  
Ziel ist es, zu zeigen, wie auf Betriebssystem- und Anwendungsebene Massnahmen zur Systemsicherheit umgesetzt werden können.  

## Vorgehen

### 1. Server-Härtung
- Installation eines Linux-Servers  
- Durchführung von Sicherheitsmassnahmen:  
  - Regelmässige Updates und Patches  
  - Absicherung des SSH-Zugangs  
  - Einrichtung einer Firewall
  - Einsatz von Fail2Ban gegen Brute-Force-Angriffe  
  - Aktivierung von Logging & Monitoring  

### 2. Entwicklung der Web-App
- Umsetzung einer einfachen Webanwendung mit folgenden Funktionen:  
  - Benutzerregistrierung mit sicherem Passwort-Hashing (bcrypt)  
  - Login mit Session-Handling und sicheren Cookies  
  - Zwei-Faktor-Authentifizierung

## Fokus
Der Schwerpunkt der Projektarbeit liegt auf folgenden Aspekten:  
- Praktische Umsetzung von Systemsicherheit
- Nachweisbare Verbesserung der Sicherheit durch konkrete Massnahmen  
- Darstellung typischer Sicherheitslücken und deren Absicherung  
- Anschauliche Demonstration durch Vorher-/Nachher-Vergleich  

## Erwartetes Ergebnis
Am Ende soll ein gehärteter Linux-Server mit einer sicheren Web-App entstehen, die gegen grundlegende Angriffe geschützt ist und moderne Authentifizierungsmechanismen wie Zwei-Faktor-Authentifizierung einsetzt.
