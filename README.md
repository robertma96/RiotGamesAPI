# RiotGamesAPI
In desfasurare!
Un proiect in care un anumit jucator de League of Legends isi poate vedea statisticile contului, iar in baza acestora, va primi sugestii care au ca scop imbunatatirea gameplay-ului respectivului jucator.
Pentru a verifica funcionalitatea script-ului, trebuie sters continutul fisierelor "lista_meciuri.txt" si "lista_campioni_jucati.txt", apoi rulat riot.py, apoi test.py.

La prima rulare va dura ceva timp, din cauza limitarilor impuse de serverele celor de la Riot Games.


Pana in acest moment, doar creeaza o lista de liste, fiecare lista din interiorul listei mama contine 3 campuri: Id-ul unic al campionului, numarul de meciuri jucate pe acesta, numarul de meciuri castigate cu respectivul campion. 
Urmeaza sa adaug mai multe date pentru a putea crea statisticile pentru fiecare campion jucat de un anumit cont.
Exista un fisier text "lista_meciuri.txt". Am creat acest fisier pentru a nu mai face request-uri inutile la API-ul celor de la Riot, pentru a scurta timpul de executie. Practic se fac request-uri doar pentru meciurile jucat de la ultima rulare a programului. 

In viitor voi crea contul introdus ca fiind un obiect, iar fiecare campion jucat al respectivului cont sa fie la randul lui un obiect, pentru a le adauga intr-o baza de data (MySQL) si a nu mai folosi fisierul text.

Dupa colectarea datelor va urma partea de afisare pe o pagina web a acestora pe care o voi creea cu Django. 
Finalul proiectului va arata ceva aproximativ cu http://eune.op.gg/summoner/userName=jon%20snow
