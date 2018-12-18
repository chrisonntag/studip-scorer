# studip-scorer (aka Klaus)
## Install

Rename ```config_sample.cfg``` to ```config.cfg``` and fill in your own username password combination and all other required fields. You can simply copy the course id out of your browsers address field.

After that, setup a cronjob pointing at the ```start.sh``` script. Also make sure that this file is executable.

```bash
0,15,30,45 * * * * ~/cronjobs/studip-scorer/start.sh
MAILTO="<youraddress@yourdomain.yourtld"
```

Have fun and rule your local Stud.IP university ranking. According to the Stud.IP source code you can reach following levels of prestige where the point limits are all power of 2s: 

```
Unbeschriebenes Blatt: 1-4
Neuling: 8
Greenhorn: 16
Anfänger: 32
Einsteiger: 64
Beginner: 128
Novize: 256
Fortgeschrittener: 512
Kenner: 1024
Könner: 2048
Profi: 4096
Experte: 8192
Meister: 16.384
Großmeister: 32.768
Idol: 65.536
Guru: 131.072
Lichtgestalt: 262.144
Halbgott: 262144
Gott: 524288
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


