# ProjektnaNaloga
##Za Uvod v programiranje

###User guide:
mapo Projektna naloga shranimo v virtualnem okolju, potrebne knjižnjice instaliramo
```bash
pip3 install -r requirements.txt
```

in ustvarimo databazo z vsemi modeli

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Django ima ugrajeno admin funkcionalnost, ki omogoča dober pregled nad dataabazo v zavihku /admin. Za dostop pa je potreben administrativni profil, ki ga je najlažje narediti kar v terminalu

```bash
python3 manage.py createsuperuser
```

ko ustvarimo profil, poženemo developement server tako:

```bash
python3 manage.py runserver
```

na http://127.0.0.1:8000/admin nas pozdravi nekaj takega:
<img width="1512" alt="image" src="https://github.com/user-attachments/assets/4a1f7063-1a35-4769-8c6a-6ffca80c325b">

Ker smo ustvarili superuserja iz terminala, v databazi manjka vnos v tabelo Uporabnik, pod razdelkom Uporabniks, ki ima OnetoOne odnos z osnovnim Django User modelom, kjer sta shranjena podatka o kategoriji in lokaciji, kjer bi uporabnik opravljal glavno vožnjo. To lahko popravimo tako, da dodamo uporabnik objekt, izberemo svoj profil (ki bi za zdaj moral biti edina izbira, saj je samo en User profil shranjen), ter kategorijo in lokacijo. Zaradi demonstrativne narave je najbolj priporočljivo, da se izbere Ljubljano kot lokacijo in A ali B kot kategorijo, za katere vemo da so datumi razpisani. V nekaterih krajih namreč ni terminov za naprimer kategorijo D, zato se obveščevanje po mailu ne pokaže. Več o tem kasneje.

s tem v mislih lahko zdaj obiščemo domačo stran na http://127.0.0.1:8000/, kjer imamo nekaj povezav na voljo
1. Home - domača stran, link je tu zato, ker Django omogoča pisanje .html datotek po nekakšni hierearhični ureditvi, kjer je base.html osnova, na kateri nato gradimo ostale zavihke - da se koda ne ponavlja
2. Execute - stran z gumbom, ki požene program periodično.py v root directoryju projekta, ki izvede dejansko delo scrapanja spletne strani uprave in databazo napolni z najdenimi termini
3. Atributi - samo prikaže našo izbiro kategorije in lokacije. Lahko bi se dodal obrazec, kjer lahko to spremenimo, ampak se mi ni zdelo smiselno za tako spletno stran
4. Termini - prikaže tabelo s termini za našo izbiro, prikaže kategorijo, lokacijo, datum in čas ter število mest

###Dokumentacija programov scraper.py, periodicno.py in preverjalnik.py
1. scraper.py
  1.knjižnice requests in BeautifulSoup so uporabljene za funkcionalnost praskanja terminov iz spletne strani uprave. Ta se sicer posodablja dinamično po izbiri filtrov, url se ne spremeni, ampak sem po pregledu prometa videl, da to dela preko neke singelton.html strani, točno kako ne vem, ampak je url naslov generičen in sem po nekaj spremembah filtrov izčrpal informacije o lokacijah in številkah, ki jih uporablja za različne lokacije in kategorije. Sicer je še ena spremenljivka na uradni spletni strani, Območje, ki pa samo omeji izbor lokacij. Da bi omejil obseg naloge sem si zato izbral eno lokacijo iz vsakega območja in za to spremenljivko naredil slovar, ki avtomatsko izbere območje glede na izbrano lokacijo. Program deluje tako, da za izbrano kombinacijo kategorije in lokacije izlušči informacije o terminih in jih shrani v tuple. Na uradni spletni strani za vsak termin tudi piše, da je samo eno prosto mesto, se pa zgodi, da se termini ponavljajo. Zato sem z zadnjo for zanko število tuple objektov zmanjšal tako, da sem preveril ponovitve. Ker ponovitve na uradni spletni strani nastopijo ena za drugo, je moja implementacija v resnici zelo osnovna, za vsak termin pogleda, če je ta datum in začetek že v seznamu condensed - če ni, ga dodam seznamu condensed, in seznamu st?ponovitev dodam na konec 1. Če pa je, bo to zadnji v condensed in samo prištejem ena zadnjemu elementu v st_ponovitev, in na koncu vse skupaj spravim v en seznam tuplov, ki vsebujejo tuple datuma in ure, ter število ponovitev.
  2. createtermin in deletetermin sta funkciji, ki sprejmeta lokacijo in kategorijo, createtermin pa še datum in čas ter število mest. Deletetermin izbriše vse termine za dano lokacijo in kategorijo, ker se z vsako uporabo funkcije main databaza ponovno napolni s termini, in je lažje vse izbrisati in ponovno ustvariti termine, kot preverjati, če kak objekt z istimi atributi že obstaja. Za te funkcije je tudi nujna knjižnica os in django, ker omogoča ustvarjanje in brisanje objektov v databazi
2. preverjalnik.py
  1.obvesti je funkcija, ki sprejme seznam emailov in jim pošlje nek generičen mail, ki obvešča uporabnika o novih terminih, za obveščanje oz ne obveščanje pa se odloči naslednji program. Trenutno se uporablja console email backend, ki mail izpiše v termial. Da se to izvesti dejansko prek SMTP backenda, ki je tudi vključen v Django, ampak je za potrebe te naloge to nesmiselno postavljati
3.periodicno.py
  1. tako se imenuje, ker je ideja, da bi se program izvajal periodično, kar je sicer možno, če bi se hecal še s knjižnjico celery, ampak je popolnoma zadosten cron job in Django management command, vendar se mi ni zdelo potrebno dodajati kompleksnosti nalogi.
  2. Uporablja funkcijo main iz scraper.py in obvescevalec iz preverjalnik.py, ponovno potrebuje knjižnico django in os za ustvarjanje objekta Casovnica, to pa je tabela, ki obstaja samo zato, da shrani informacijo o oddaljenosti najbljižjega termina (časovno), saj se na podlagi informacij o novih terminih oziroma o oddaljenosti le-teh odloči, ali uporabi funkcijo obvescevalec, ki obvesti uporabnike o novih terminih zgolj v primeru, da se pojavi kak izreden datum, ki je časovno manj oddaljen kot prejšnji najbližji. Na dnu je še funkcija za_view, ki pa obstaja samo zato, ker jo uporabi funkcija periodicno_view v views.py, ki se uporabi pri zavihku execute, ko ročno poženemo program.

###Specifike Django frameworka
Na kratko, Django je framework za postavljanje spletnih strani, ki omogoča enostaven pregled nad ddatabazami, ponuja mnogo avtentikacijskih backendov, obveščevalnih backendov in predvsem Django templatin engine, ki je zelo prijazen za pisanje .html datotek, saj omogoča vključevanje logike, ki je zgolj s HTML nemogoča, ta logika pa je tudi zelo podobna pythonovi (for zanke in if trditve v mojem primeru).
Za ustvarjanje tabel databaze se v Djangotu ustvari "aplikacija", ki ustvari nekaj datotek, pomembne za razumeti so models.py, urls.py, views.py in admin.py
1. models.py: datoteka, kjer ustvarimo "modele", ki v resnici predstavljajo tabele v databazi. V tej projektni nalogi sta dve aplikaciji, userdata in datumi. ločitev je narejena zaradi večje preglednosti in izogibanja konfliktov (ne tako uporabno, ko je en sam razvijalec, ampak je bolj kot ne navada da tako delam). V aplikaciji userdata je en sam model, Uporabnik, ki ima, kot že prej omenjeno OnetoOne odnos z Djangotovim osnovnim User modelom, zato da lahko na zelo preprost način "dodam" atribute uporabniku. Bolj zakompliciran in v tem primeru odveč način je tako imenovan AbstractUser, ki nudi več prilagodljivosti, ampak za dodajanje dveh atributov je popolnoma zadostna moja implementacija. V resnici ima model 3 atribute, še območje, ki pa se zapolni avtomatsko na podlagi slovarja, ki je definiran v metodi save(), ki je tu nujna, saj pri kreaciji novega vnosa polje območje ne sme biti prazno, zato je potreben override osnovne save metode, da se pred shranitvijo vrine še podatek o območju. Shranjen je kot Integerfield, ker je to potrebno za scraper.py, ki na podlagi tega izpolni URL naslov, katerega praska. V modelu Uporaabnik (kot pa tudi termin in časovnica) pa sta zraven še slovarja za kategorijo in lokacijo, kjer so določene možne izbire za ta dva atributa. Slovar ima na eni strani številko, ki se shrani v databazi in ki predstavlja del naslova, ki ga praska program, na drugi strani pa verbose ime, ki se vidi npr. v admin/ zavihku in na atributi/. V aplikaciji datumi pa sta dva modela, Termin in Casovnica. Termin je tabela, ki shranjuje termine, torej kategorijo, lokacijo, datum in čas ter število mest. To tabelo spreminja in dopolnjuje funkcija main() v scraper.py, in iz tu se nadaljno črpa podatek timedelta za tabelo Casovnica. Poleg tega ima časovnica še atributa kategorija in lokacija, obviously.
2. views.py: je datoteka, kjer definiramo django views - v glavnem funkcije, ki se kličejo ob obisku nekega zavihka spletne strani. Notri lahko torej napišemo nek algoritem oziroma potegnemo podatke iz databaze, ki so potem spremenljivke za dejanski render spletne strani. Na primer v userdata/views.py atributi_view izčrpamo podatke o uporabniku, ki jih z argumentom v funkciji render() predamo naprej v .html datoteko, kjer so te spremenljivke zapisani v dvojnih zavitih oklepajih, ki se naložijo na koncu kot pravilni podatki iz databaze.
3. urls.py je datoteka, kjer definiramo poti in hierarhije zavihkov, torej podamo path (prvi argument funkcije path()), view - torej funkcijo, ki predela podatko in vrne pravilen html, in ime, ki je praktičen pri naprimer povezavah, recimo tiste v base.html, kjer je za link podano zgolj ime poti za določen view.
