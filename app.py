import sqlite3
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'quiz_pro_vibrant'

# --- CONFIGURARE ---
JOC_INCEPUT = False
intrebari_curente = []


def init_db():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS clasament (nume TEXT UNIQUE, scor INTEGER)')
        conn.commit()
        conn.close()
    except:
        pass


init_db()

# --- BAZA DE DATE ÎNTREBĂRI ---
pool_categorii = {
    "Geografie": [
        {"text": "Care este, oficial, cel mai înalt vârf muntos de pe suprafața Pământului?",
         "optiuni": ["K2", "Mont Blanc", "Everest", "Kilimanjaro"], "corect": "Everest"},
        {"text": "Care este capitala Australiei (atenție, nu este cel mai mare oraș)?",
         "optiuni": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "corect": "Canberra"},
        {"text": "Ce fluviu important traversează capitala Marii Britanii, Londra?",
         "optiuni": ["Sena", "Tamisa", "Dunărea", "Rinul"], "corect": "Tamisa"},
        {"text": "Care este cel mai mic stat independent din lume, situat în interiorul Romei?",
         "optiuni": ["Monaco", "San Marino", "Liechtenstein", "Vatican"], "corect": "Vatican"},
        {"text": "În ce țară din America de Sud se află celebrele ruine incașe de la Machu Picchu?",
         "optiuni": ["Peru", "Mexic", "Brazilia", "Chile"], "corect": "Peru"},
        {"text": "Care este cel mai întins ocean de pe planeta noastră?",
         "optiuni": ["Oceanul Atlantic", "Oceanul Indian", "Oceanul Pacific", "Oceanul Arctic"],
         "corect": "Oceanul Pacific"},
        {"text": "Ce țară europeană este recunoscută ușor pe hartă datorită formei sale de cizmă?",
         "optiuni": ["Spania", "Italia", "Grecia", "Portugalia"], "corect": "Italia"},
        {"text": "Care este cel mai mare deșert fierbinte din lume?",
         "optiuni": ["Gobi", "Sahara", "Kalahari", "Atacama"], "corect": "Sahara"},
        {"text": "Câte continente există conform modelului geografic predat în școlile din România?",
         "optiuni": ["5", "6", "7", "8"], "corect": "7"},
        {"text": "Care este capitala administrativă a Turciei?", "optiuni": ["Istanbul", "Ankara", "Antalya", "Izmir"],
         "corect": "Ankara"},
        {"text": "În ce țară africană se pot vizita Marile Piramide din Giza?",
         "optiuni": ["Egipt", "Maroc", "Tunisia", "Africa de Sud"], "corect": "Egipt"},
        {"text": "Care este cel mai lung fluviu care curge pe teritoriul Europei?",
         "optiuni": ["Dunărea", "Volga", "Rin", "Sena"], "corect": "Volga"},
        {"text": "Ce națiune asiatică este supranumită 'Țara Soarelui Răsare'?",
         "optiuni": ["China", "Japonia", "Coreea de Sud", "Thailanda"], "corect": "Japonia"},
        {"text": "Care este orașul capitală al Statelor Unite ale Americii?",
         "optiuni": ["New York", "Los Angeles", "Washington D.C.", "Miami"], "corect": "Washington D.C."},
        {"text": "În ce metropolă europeană se află celebrul Turn Eiffel?",
         "optiuni": ["Londra", "Berlin", "Paris", "Madrid"], "corect": "Paris"}
    ],
    "Istorie": [
        {"text": "În ce an a izbucnit Primul Război Mondial?", "optiuni": ["1939", "1914", "1918", "1900"],
         "corect": "1914"},
        {"text": "Cine a fost primul președinte din istoria Statelor Unite ale Americii?",
         "optiuni": ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "J.F. Kennedy"],
         "corect": "George Washington"},
        {"text": "În ce an a avut loc Marea Unire de la Alba Iulia?", "optiuni": ["1859", "1918", "1989", "1877"],
         "corect": "1918"},
        {"text": "Ce prim-ministru britanic a fost supranumit 'Doamna de Fier'?",
         "optiuni": ["Regina Elisabeta", "Margaret Thatcher", "Angela Merkel", "Theresa May"],
         "corect": "Margaret Thatcher"},
        {"text": "În ce an a căzut Zidul Berlinului, simbolizând sfârșitul Războiului Rece?",
         "optiuni": ["1991", "1961", "1989", "1945"], "corect": "1989"},
        {"text": "Care domnitor a realizat prima unire politică a țărilor române în anul 1600?",
         "optiuni": ["Ștefan cel Mare", "Alexandru Ioan Cuza", "Mihai Viteazul", "Vlad Țepeș"],
         "corect": "Mihai Viteazul"},
        {"text": "Ce mare imperiu al antichității a fost condus de Iulius Cezar?",
         "optiuni": ["Imperiul Otoman", "Imperiul Britanic", "Republica Romană", "Imperiul Mongol"],
         "corect": "Republica Romană"},
        {"text": "Cine este navigatorul creditat cu descoperirea Americii în anul 1492?",
         "optiuni": ["Amerigo Vespucci", "Cristofor Columb", "Ferdinand Magellan", "Vasco da Gama"],
         "corect": "Cristofor Columb"},
        {"text": "În ce an s-a scufundat celebrul pachebot Titanic?", "optiuni": ["1900", "1912", "1920", "1997"],
         "corect": "1912"},
        {"text": "Cine a fost primul om care a pășit pe suprafața Lunii?",
         "optiuni": ["Yuri Gagarin", "Buzz Aldrin", "Neil Armstrong", "Michael Collins"], "corect": "Neil Armstrong"},
        {"text": "Cine a fost liderul militar și politic francez care s-a autoîncoronat Împărat?",
         "optiuni": ["Ludovic al XIV-lea", "Napoleon Bonaparte", "Charles de Gaulle", "Emmanuel Macron"],
         "corect": "Napoleon Bonaparte"},
        {"text": "În ce an a avut loc Revoluția care a dus la căderea regimului comunist în România?",
         "optiuni": ["1945", "1977", "1989", "1991"], "corect": "1989"},
        {"text": "Ce artist renascentist a pictat tavanul Capelei Sixtine?",
         "optiuni": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"], "corect": "Michelangelo"},
        {"text": "Ce civilizație antică este faimoasă pentru construirea piramidelor?",
         "optiuni": ["Romanii", "Grecii", "Egiptenii", "Vikingii"], "corect": "Egiptenii"},
        {"text": "În ce an a început cel de-al Doilea Război Mondial?", "optiuni": ["1914", "1939", "1945", "1920"],
         "corect": "1939"}
    ],
    "Divertisment": [
        {"text": "Cine este autoarea celebrei serii de romane fantastice 'Harry Potter'?",
         "optiuni": ["J.R.R. Tolkien", "Stephen King", "J.K. Rowling", "George R.R. Martin"], "corect": "J.K. Rowling"},
        {"text": "Care este numărul de cod al agentului secret James Bond?", "optiuni": ["007", "001", "911", "404"],
         "corect": "007"},
        {"text": "Ce trupă britanică a lansat legendara piesă 'Bohemian Rhapsody'?",
         "optiuni": ["The Beatles", "Queen", "Rolling Stones", "AC/DC"], "corect": "Queen"},
        {"text": "Cum se numește regatul african fictiv condus de supereroul Black Panther?",
         "optiuni": ["Zamunda", "Wakanda", "Asgard", "Genovia"], "corect": "Wakanda"},
        {"text": "Ce artist american a fost supranumit 'Regele muzicii Pop'?",
         "optiuni": ["Elvis Presley", "Prince", "Michael Jackson", "Freddie Mercury"], "corect": "Michael Jackson"},
        {"text": "Câte sezoane are serialul de comedie 'Friends'?", "optiuni": ["8", "10", "12", "15"], "corect": "10"},
        {"text": "Ce actor a interpretat rolul principal (Jack Dawson) în filmul 'Titanic'?",
         "optiuni": ["Brad Pitt", "Leonardo DiCaprio", "Johnny Depp", "Tom Cruise"], "corect": "Leonardo DiCaprio"},
        {"text": "Din ce oraș industrial britanic provine trupa The Beatles?",
         "optiuni": ["Londra", "Manchester", "Liverpool", "Birmingham"], "corect": "Liverpool"},
        {"text": "Ce culoare are pastila pe care o alege Neo în filmul 'Matrix' pentru a afla adevărul?",
         "optiuni": ["Albastră", "Roșie", "Verde", "Neagră"], "corect": "Roșie"},
        {"text": "Cine este creatorul și regizorul universului 'Star Wars'?",
         "optiuni": ["Steven Spielberg", "James Cameron", "George Lucas", "Quentin Tarantino"],
         "corect": "George Lucas"},
        {"text": "Care este identitatea secretă a supereroului Iron Man?",
         "optiuni": ["Steve Rogers", "Bruce Banner", "Tony Stark", "Peter Parker"], "corect": "Tony Stark"},
        {"text": "Care este filmul cu cele mai mari încasări din istoria cinematografiei?",
         "optiuni": ["Titanic", "Avatar", "Avengers: Endgame", "Star Wars"], "corect": "Avatar"},
        {"text": "Ce cântăreață britanică interpretează hitul 'Hello'?",
         "optiuni": ["Rihanna", "Beyonce", "Adele", "Shakira"], "corect": "Adele"},
        {"text": "Ce specie de animal este Simba din 'Regele Leu'?", "optiuni": ["Tigru", "Leu", "Leopard", "Panteră"],
         "corect": "Leu"},
        {"text": "Cum se numește dragonul din seria 'Hobbitul'?", "optiuni": ["Smaug", "Drogon", "Spyro", "Toothless"],
         "corect": "Smaug"}
    ],
    "Sport": [
        {"text": "Ce echipă națională a câștigat Campionatul Mondial de Fotbal din 2022?",
         "optiuni": ["Franța", "Brazilia", "Argentina", "Germania"], "corect": "Argentina"},
        {"text": "La ce aparat a obținut Nadia Comăneci prima notă de 10 din istoria gimnasticii?",
         "optiuni": ["Bârnă", "Paralele inegale", "Sol", "Sărituri"], "corect": "Paralele inegale"},
        {"text": "Câți jucători are o echipă de fotbal pe teren în timpul jocului?", "optiuni": ["7", "10", "11", "15"],
         "corect": "11"},
        {"text": "În ce sport se folosește termenul 'Grand Slam' pentru cele 4 turnee majore?",
         "optiuni": ["Tenis", "Fotbal", "Formula 1", "Baschet"], "corect": "Tenis"},
        {"text": "Cine deține recordul pentru cele mai multe Baloane de Aur câștigate (până în 2023)?",
         "optiuni": ["Cristiano Ronaldo", "Lionel Messi", "Pelé", "Maradona"], "corect": "Lionel Messi"},
        {"text": "Cât durează timpul regulamentar al unui meci de rugby?",
         "optiuni": ["60 minute", "80 minute", "90 minute", "100 minute"], "corect": "80 minute"},
        {"text": "În ce oraș au avut loc primele Jocuri Olimpice moderne din anul 1896?",
         "optiuni": ["Paris", "Londra", "Atena", "Roma"], "corect": "Atena"},
        {"text": "Ce sport practică marea campioană româncă Simona Halep?",
         "optiuni": ["Gimnastică", "Handbal", "Tenis de câmp", "Înot"], "corect": "Tenis de câmp"},
        {"text": "Care este distanța oficială a unui maraton?", "optiuni": ["40 km", "42,195 km", "21 km", "50 km"],
         "corect": "42,195 km"},
        {"text": "Michael Jordan este considerat o legendă a welui sport?",
         "optiuni": ["Fotbal American", "Baschet", "Baseball", "Golf"], "corect": "Baschet"},
        {"text": "Câte cercuri sunt prezente pe steagul olimpic?", "optiuni": ["4", "5", "6", "7"], "corect": "5"},
        {"text": "Cine este tenismenul supranumit 'Regele Zgurii'?",
         "optiuni": ["Roger Federer", "Novak Djokovic", "Rafael Nadal", "Andy Murray"], "corect": "Rafael Nadal"},
        {"text": "Care este considerat sportul național în Japonia?", "optiuni": ["Karate", "Sumo", "Judo", "Baseball"],
         "corect": "Sumo"},
        {"text": "În ce sport se folosește un puc în loc de minge?",
         "optiuni": ["Fotbal", "Hochei pe gheață", "Golf", "Polo"], "corect": "Hochei pe gheață"},
        {"text": "Ce echipă de fotbal spaniolă este cunoscută sub numele de 'Galacticii'?",
         "optiuni": ["FC Barcelona", "Real Madrid", "AC Milan", "Manchester United"], "corect": "Real Madrid"}
    ],
    "Stiinta": [
        {"text": "Care este formula chimică universal cunoscută pentru apă?", "optiuni": ["CO2", "NaCl", "H2O", "O2"],
         "corect": "H2O"},
        {"text": "Care este planeta din sistemul nostru solar situată cel mai aproape de Soare?",
         "optiuni": ["Venus", "Pământ", "Mercur", "Marte"], "corect": "Mercur"},
        {"text": "Aproximativ câte oase are scheletul unui om adult?", "optiuni": ["105", "206", "300", "500"],
         "corect": "206"},
        {"text": "Care este cel mai dur material natural cunoscut pe Pământ?",
         "optiuni": ["Aurul", "Oțelul", "Diamantul", "Granitul"], "corect": "Diamant"},
        {"text": "Ce gaz absorb plantele din atmosferă în timpul procesului de fotosinteză?",
         "optiuni": ["Oxigen", "Dioxid de carbon", "Azot", "Hidrogen"], "corect": "Dioxid de carbon"},
        {"text": "Care este cel mai mare mamifer care trăiește în prezent pe Terra?",
         "optiuni": ["Elefantul African", "Balena Albastră", "Girafa", "Rechinul Alb"], "corect": "Balena Albastră"},
        {"text": "Cine este fizicianul care a formulat celebra teorie a relativității?",
         "optiuni": ["Isaac Newton", "Albert Einstein", "Nikola Tesla", "Charles Darwin"], "corect": "Albert Einstein"},
        {"text": "La ce temperatură fierbe apa la nivelul mării?", "optiuni": ["50°C", "90°C", "100°C", "110°C"],
         "corect": "100°C"},
        {"text": "Care este organul vital responsabil cu pomparea sângelui în corp?",
         "optiuni": ["Plămânii", "Ficatul", "Inima", "Creierul"], "corect": "Inima"},
        {"text": "Care este viteza aproximativă a luminii în vid?",
         "optiuni": ["1.000 km/h", "300.000 km/s", "340 m/s", "100.000 km/s"], "corect": "300.000 km/s"},
        {"text": "Ce planetă este faimoasă pentru inelele sale spectaculoase?",
         "optiuni": ["Marte", "Jupiter", "Saturn", "Venus"], "corect": "Saturn"},
        {"text": "Care este simbolul chimic pentru elementul Aur?", "optiuni": ["Au", "Ag", "Fe", "Cu"],
         "corect": "Au"},
        {"text": "Cine este savantul care a descoperit legea gravitației universale?",
         "optiuni": ["Einstein", "Isaac Newton", "Galileo Galilei", "Stephen Hawking"], "corect": "Isaac Newton"},
        {"text": "Din punct de vedere astronomic, ce este Soarele?",
         "optiuni": ["O planetă", "Un satelit", "O stea", "Un meteorit"], "corect": "O stea"},
        {"text": "Câte grade are un unghi drept?", "optiuni": ["45 grade", "90 grade", "180 grade", "360 grade"],
         "corect": "90 grade"}
    ]
}


@app.route('/')
def index():
    if JOC_INCEPUT:
        return "⚠️ Jocul este în desfășurare! Te rugăm să aștepți runda următoare."
    return render_template('index.html')


@app.route('/inregistrare', methods=['POST'])
def inregistrare():
    nume = request.form.get('username')
    session['username'] = nume
    session['score'] = 0
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO clasament (nume, scor) VALUES (?, 0)", (nume,))
        conn.commit()
        conn.close()
    except:
        pass
    return redirect(url_for('waiting_room'))


@app.route('/waiting_room')
def waiting_room():
    if JOC_INCEPUT:
        return redirect(url_for('quiz', id_intrebare=0))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT nume FROM clasament")
    jucatori = c.fetchall()
    conn.close()
    return render_template('waiting.html', jucatori=jucatori)


@app.route('/admin_start', methods=['POST'])
def admin_start():
    global JOC_INCEPUT, intrebari_curente, pool_categorii
    domeniu_ales = request.form.get('domeniu')
    lista_de_extras = []

    if domeniu_ales == "Mix":
        for cat in pool_categorii:
            lista_de_extras.extend(pool_categorii[cat])
    else:
        lista_de_extras = pool_categorii.get(domeniu_ales, [])

    nr_intrebari = min(15, len(lista_de_extras))
    selectie = random.sample(lista_de_extras, nr_intrebari)

    intrebari_curente = []
    for i in range(len(selectie)):
        q_noua = selectie[i].copy()
        q_noua['id'] = i

        # --- AICI ESTE PARTEA NOUĂ PENTRU AMESTECAREA RĂSPUNSURILOR ---
        # Facem o copie a listei de opțiuni și o amestecăm
        q_noua['optiuni'] = q_noua['optiuni'].copy()
        random.shuffle(q_noua['optiuni'])
        # -------------------------------------------------------------

        intrebari_curente.append(q_noua)

    JOC_INCEPUT = True
    return redirect(url_for('waiting_room'))


@app.route('/reset')
def reset():
    global JOC_INCEPUT
    JOC_INCEPUT = False
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM clasament")
        conn.commit()
        conn.close()
    except:
        pass
    return redirect(url_for('index'))


@app.route('/quiz/<int:id_intrebare>', methods=['GET', 'POST'])
def quiz(id_intrebare):
    if request.method == 'POST':
        raspuns_ales = request.form.get('answer')
        corect = False
        if id_intrebare > 0:
            intrebare_anterioara = intrebari_curente[id_intrebare - 1]
            if raspuns_ales == intrebare_anterioara['corect']:
                corect = True
                session['score'] += 10
                try:
                    nume = session.get('username')
                    conn = sqlite3.connect('database.db')
                    c = conn.cursor()
                    c.execute("UPDATE clasament SET scor = scor + 10 WHERE nume = ?", (nume,))
                    conn.commit()
                    conn.close()
                except:
                    pass
        return redirect(url_for('intermediate', id_curent=id_intrebare,
                                rezultat=('Bravo, răspuns corect!' if corect else 'Din păcate, răspuns greșit...')))

    if id_intrebare < len(intrebari_curente):
        return render_template('quiz.html', q=intrebari_curente[id_intrebare], nr=id_intrebare,
                               total=len(intrebari_curente))
    else:
        return redirect(url_for('result'))


@app.route('/intermediate/<int:id_curent>/<rezultat>')
def intermediate(id_curent, rezultat):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT nume, scor FROM clasament ORDER BY scor DESC LIMIT 10")
    top_jucatori = c.fetchall()
    conn.close()

    urmatoarea = id_curent
    return render_template('intermediate.html', status=rezultat, clasament=top_jucatori, next_id=urmatoarea,
                           is_final=(urmatoarea >= len(intrebari_curente)))


@app.route('/result')
def result():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT nume, scor FROM clasament ORDER BY scor DESC LIMIT 10")
    top_jucatori = c.fetchall()

    castigator = top_jucatori[0] if top_jucatori else None

    conn.close()
    return render_template('result.html', winner=castigator, clasament=top_jucatori)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)