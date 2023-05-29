# sunblock

Rasperry pi service om betalen voor terugleven te voorkomen.  Leest de energietarieven (hourly day ahead) op `mijn.easyenergy.com`.  Als het teruglevertarief onder 0 uitkomt wordt pin 8 hoog.  Geen idee hoe lang easyenergy deze service blijft verlenen maar zo lang het duurt kun je deze code inzetten om te voorkomen dat je betaald voor terugleveren

# installeren
Zo moeten werken op elke Pi een redelijk recent OS. 
gebruik de volgende commando's om te installeren:  

```
git clone git@github.com:wdeleeuw/sunblock
cd sunblock
sudo install
```


Controleren of het werkt: 

```
systemctl status sunblock 
```

Eenmaal geinstalleerd wordt de service automatisch gestart als de Pi opnieuw wordt opgestart.  


Uitzeteen van de service
 * `systemctl stop sunblock   `  : stop de service.  
 * `systemctl disable --now sunblock` : stoppen en niet opnieuw opstarten als systeem start  


signal pin is pin 8 (board)/14(BCM) 
 *  laag : energieprijs is positief
 *  high : energieprijs is negatief
