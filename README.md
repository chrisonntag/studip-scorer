# studip-scorer (aka Klaus)
## Install

Rename ```credentials_sample.cfg``` to ```credentials.cfg``` and fill in your own username password combination separated by the ```\n``` char.

After that setup a cronjob pointing at the ```start.sh``` script. Also make sure that this file is executable.

```bash
0,15,30,45 * * * * ~/cronjobs/studip-scorer/start.sh
MAILTO="<youraddress@yourdomain.yourtld"
```

Have fun and rule your local Stud.IP university ranking. According to the Stud.IP source code you can reach following levels of prestige: 

```
Unbeschriebenes Blatt
Neuling
Greenhorn
Anfänger 
Einsteiger
Beginner 
Novize
Fortgeschrittener
Kenner
Könner 
Profi
Experte
Meister
Großmeister
Idol
Guru
Lichtgestalt
Halbgott
Gott
```

and you can become (presumably) one of the following kings: 

```
King of ...

hochgeladene Dateien
Forums-Beiträge
Wiki-Beiträge
abgegebene Stimmen
bekommene Stimmen
eingestellte Ankündigungen
```


