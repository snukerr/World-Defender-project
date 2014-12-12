World-Defender-project
Projekti koodirepositoorium/MTAT.03.100

Projekt aine 'Programmeerimine' jaoks

Idee: luua mängu 'Space Invaders' kloon ehk kahemõõtmeline arkaadmäng
Loodud Pythoni ja Pygame'i mooduli abil

Projekti tulemuseks on failid definitions.py ja FINAL.py
Esimeses on mängu elementide definitsioonid:
 - class Player - Aleksander Linnik
 - class Enemy - Konstantin Notberg
 - class Bullet - Madis Müil
 - class Enemy_bullet - Madis Müil
 - class Text - Aleksander Linnik
 - lisaks erinevate elementide muutujad
 - igal class'il on vastavele mänguelemendile vajalikud funktsioonid
Teises on põhiprogrammi kirjeldav class App
 - põhiprogrammis kutsutakse ülaltoodud class'id vajalikus kohas välja ning defineeritakse funktsioonid, mis kirjendavad
   nende omavahelist käitumist
 - lisaks on põhiprogrammis kirjeldatud mängu erinevad olekud(start menüü, mäng ise, gameover menüü)
   - gameStart
   - gameOver
   - beginGame
   - resetGame

