import mysql.connector
import string
import decimal
import time
from faker import Faker
import random
pablodb = mysql.connector.connect(
 #Database connection
)

cursor = pablodb.cursor()
fak = Faker("it_IT")
cot = []

tecniconum = 50
attestato = 50
avvocato = 50
clientenum = 50 
coinvolgim = 50 
collaboraz = 50
collaboratore = 50
contatto = 50
documentaz = 50
fase = 50
fatture = 50
file = 50
impegno = 50
lavoro = 50
normaliz = 50
partecip = 50
persona = 50
prestaz = 50
propieta = 50
rappresentanza = 50
strutturenum = 50

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y/%m/%d', prop)

sql = ""
values = []
codici_tecnici = []

for i in range(0, tecniconum):
    sql = "INSERT INTO Tecnico (CF, Nome, Cognome, PartitaIVA) VALUES (%s, %s, %s, %s);"
    codici_tecnici.append(fak.ssn())
    values.append((codici_tecnici[-1], fak.first_name(), fak.last_name(), fak.company_vat().split('T')[1]))

cursor.executemany(sql, values)

lavori_inseriti = []
lavori_certificati = []
lavori_progettazione = []
for i in range(0, lavoro):
    print(f"Lavoro {i}")
    sql = "INSERT INTO Lavoro (Denominazione, Tipo, Descrizione, DataInizio, DataConclusione, Supervisore,TotFat, TotInc,ValoreStim, Scadenza) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    Tipo = random.choice(['PER','CERAI','CEREN','CERAC',"PROV","PROVR","PRON","COTU","COTP", "PROV", "PROV", "PROV" , "PROV" , "PROV" , "PRON" , "PROV" , "PROV" , "PROV" , "PROV" , "PROV" , "PROV"  ])
    Denominazione = fak.company().split(" ")[0] + fak.text(10) 
    Descrizione = fak.text(500)
    DataInizio = random_date("2005/01/01", "2020/01/01", random.random())
    DataConclusione = random.choice([None, random_date(DataInizio, "2021/01/01", random.random())])
    Supervisore = random.choice(codici_tecnici)
    TotFat = 0 
    TotInc = 0
    #print('prova')
    print(Tipo)
    if Tipo == "PER":
        ValoreStim = random.choice([None, decimal.Decimal(random.randrange(10000))/100])
    else:
        ValoreStim = None
    if Tipo in ["CERAI","CERAC","CAREN"] :
        Scadenza = random.choice([None, random_date(DataInizio, "2021/01/01", random.random())])
        values = (Denominazione, Tipo, Descrizione, DataInizio, DataConclusione, Supervisore, TotFat, TotInc, ValoreStim, Scadenza)
        print("certi")
        lavori_certificati.append(values)
    else:
        Scadenza = None
        values = (Denominazione, Tipo, Descrizione, DataInizio, DataConclusione, Supervisore, TotFat, TotInc, ValoreStim, Scadenza)
    try:
        cursor.execute(sql, values)
        lavori_inseriti.append(values)
    except Exception as err:
        print(err)
        continue
    if "PRO" in Tipo:
        print("prog")
        sql = "INSERT INTO Progetto(PRDenominazione, PRTipo, InizioAccessi, FineAccessi, InizioSopralluoghi, FineSopralluoghi, InizioComputo, FineComputo,"\
                "IncFirmato, IncInviato, DirLavori, Direttore, InizioLavori, FineLavori) VALUES ("\
                "%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        PRDenom = Denominazione
        PRTipo = Tipo
        InizioAccessi = random_date("1910/01/01", "2020/01/01", random.random())
        FineAccessi =   random_date(InizioAccessi, "2020/01/01", random.random())
        InizioSopr  =   random_date(FineAccessi, "2020/01/01", random.random())
        FineSopr    =   random_date(InizioSopr, "2020/01/01", random.random())
        InizioCompu =   random_date(FineSopr, "2020/01/01", random.random())
        FineCompu   =   random_date(InizioCompu, "2020/01/01", random.random())
        IncInv      =   random.choice([False, True])
        if IncInv:
            IncFirm     =   random.choice([False, True])
        else:
            IncFirm = None
        DirLav      =   random.choice([False, True])
        if DirLav:
            Dirett   =   random.choice(codici_tecnici)
        else:
            Dirett =   None
        InizioLavori=   random_date("2010/01/01", "2018/01/01", random.random())
        FineLavori  =   random_date("2018/01/01", "2020/01/01", random.random())
        try:
            values= (PRDenom, PRTipo, InizioAccessi, FineAccessi, InizioSopr, FineSopr, InizioCompu, FineCompu, IncFirm, IncInv, DirLav, Dirett, InizioLavori, FineLavori )
            cursor.execute(sql, values)
            lavori_progettazione.append(values)
        except Exception as err:
            print(err)
    if "COTU" in Tipo or "COTP" in Tipo:
        cot.append(values)

clienti = [] 
persona = []
IMP = []
CON = []
#Clienti
for i in range(1, clientenum):
    print(f"cliente {i}")
    sql = "INSERT INTO Cliente (PartitaIVA, CF, Tipo, Denominazione, Comune, NumeroCiv, Citta, CAP, Indirizzo, Provincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    PartitaIVA = random.choice(["00000000000", fak.company_vat().split('T')[1]])
    Tipo = random.choice(["PER", "IMP", "CON"])
    if Tipo == "PER":
        Denominazione = None
    else:
        Denominazione = fak.text(30)
    if Tipo == "IMP":
        CF = random.choice([fak.ssn(), "00000000000"])
    else:
        CF = fak.ssn()
    sql2 = ""
    values2 = None
    Comune = fak.administrative_unit()
    NumCiv = fak.building_number()
    Citta = random.choice([Comune, fak.city(), fak.city()])
    CAP = fak.postcode()
    Indirizzo = fak.street_name()
    Provincia = fak.state()
    try:
        values = (PartitaIVA, CF, Tipo, Denominazione, Comune, NumCiv, Citta, CAP, Indirizzo, Provincia)
        if "PER" in Tipo:
            sql2 = "INSERT INTO Persona(PartitaIVA, CF, Tipo, Nome, Cognome, DataNascita, Citta, Comune, Provincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            Nome = fak.first_name()
            Cognome = fak.last_name()
            DataNascita =  random_date("1950/01/01", "2002/01/01", random.random())
            values2 = (PartitaIVA, CF, "PER", Nome, Cognome, DataNascita, Citta, Comune, Provincia)
            persona.append(values2)
        if "IMP" in Tipo:
            IMP.append(values)
        if "CON" in Tipo:
            CON.append(values)
        cursor.execute(sql, values)
        if "PER" in Tipo:
            cursor.execute(sql2, values2)
        clienti.append(values) 
    except Exception as err:
        print(err)





strutture = []
for i in range(0, strutturenum):
    print(f"strutture {i}")
    sql = "INSERT INTO Struttura (CAP, Indirizzo, NumCiv, Provincia, Citta, Comune, DataCostruzione, ComuneCatastale, Foglio, Particella, Subalterno, Scala, Piano, Sezione, Tipo)"\
            " VALUES  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    CAP = fak.postcode()
    Indirizzo = fak.street_name()
    NumCiv = fak.building_number()
    Provincia = fak.state()
    Citta = fak.city()
    Comune = fak.state()
    DataCostruzione = random_date("1910/01/01", "2020/01/01", random.random())
    ComuneCatastale = fak.state()
    Foglio = random.randint(1, 999)
    Particella = random.randint(1, 999)
    Subalterno = random.randint(1,999)
    Scala = random.randint(1, 99)
    Piano = random.randint(1, 99)
    Sezione = random.randint(1,999)
    Tipo = fak.text(10)
    try:
        values = (CAP, Indirizzo, NumCiv, Provincia, Citta, Comune, DataCostruzione, ComuneCatastale, Foglio, Particella, Subalterno, Scala, Piano, Sezione, Tipo)
        strutture.append(values)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

for i in range(0, coinvolgim):
    print(f"coinvolgimenti {i}")
    sql = "INSERT INTO Coinvolgim(Denominazione, Tipo, CAP, Indirizzo, NumCiv)"\
                        " VALUES  (%s, %s, %s, %s, %s)"
    try:
        l = random.choice(lavori_inseriti)
        s = random.choice(strutture)
        Denominazione = l[0]
        Tipo = l[1]
        CAP = s[0]
        Indirizzo = s[1]
        NumCiv = s[2]
        values = (Denominazione, Tipo, CAP, Indirizzo, NumCiv)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

for i in range(0, propieta):
    print(f"propietà {i}")
    sql = "INSERT INTO Proprieta(PartitaIVA, CF, Tipo, CAP, Indirizzo, NumCiv, DataInizioProp, DataFineProp)"\
                        " VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        c = random.choice(clienti)
        s = random.choice(strutture)
        PartitaIVA = c[0]
        CF = c[1]
        CAP = s[0]
        Tipo = c[2]
        Indirizzo = s[1]
        NumCiv = s[2]
        DataInizio = random_date("1910/01/01", "2020/01/01", random.random())
        DataFine = random_date(DataInizio, "2021/01/01", random.random())
        values = (PartitaIVA, CF, Tipo, CAP, Indirizzo, NumCiv, DataInizio, DataFine)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

files = []
for i in range(0, file):
    print(f"file {i}")
    sql = "INSERT INTO FileLavoro(Directory, Descrizione, Tipo)"\
          " VALUES  (%s, %s, %s)"
    try:
        Directory = ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 30))
        Descrizione = fak.text(50)
        Tipo = random.choice(['jpg', 'png', 'pdf', 'xml', 'opt'])
        values = (Directory, Descrizione, Tipo)
        files.append(values)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)


for i in range(0, documentaz):
    print(f"documentaz {i}")
    sql = "INSERT INTO Documentaz(FileDir, DenomLavoro, TipoLavoro)"\
          " VALUES  (%s, %s, %s)"
    try:
        f = random.choice(files)
        l = random.choice(lavori_inseriti)
        Directory = f[0]
        DenomLavoro = l[0]
        TipoLavoro = l[1]
        values = (Directory, DenomLavoro, TipoLavoro)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

for i in range(0, normaliz):
    print(f"normaliz {i}")
    sql = "INSERT INTO Normaliz(DenomCertificato, TipoCertificato, DenomProgetto, TipoProgetto)"\
          " VALUES  (%s, %s, %s, %s)"
    try:
        
        c = random.choice(lavori_certificati)
        print("qua")
        p = random.choice(lavori_progettazione)
        denomcertificato = c[0]
        TipoCertificato = c[1]
        DenomProgetto = p[0]
        TipoProgetto = p[1]
        values = (denomcertificato, TipoCertificato, DenomProgetto, TipoProgetto)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)


for i in range(0, fase):
    print(f"Fase {i}")
    sql = "INSERT INTO Fase(Denominazione, Tipo, DataFase, Descrizione)"\
          " VALUES  (%s, %s, %s, %s)"
    try: 
        p = random.choice(lavori_progettazione)
        DataInizio = random_date("1910/01/01", "2020/01/01", random.random())
        DenomProgetto = p[0]
        Descrizione = fak.text(10)
        values = (DenomProgetto, p[1], DataInizio, Descrizione)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

for i in range(0, attestato):
    print(f"Attestato {i}")
    sql = "INSERT INTO Attestato(ID, Tipo, Tecnico)"\
          " VALUES  (%s, %s, %s)"
    try:
        
        p = random.randint(0, len(codici_tecnici))
        tecnico = codici_tecnici[p]
        ID = ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
        Tipo = random.choice(["CERAI", "CEREN", "ING", "CERAC", "GEO"])
        values = (ID, Tipo, tecnico)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

avvocati = []
for i in range(0, avvocato):
    print(f"Avvocato {i}")
    sql = "INSERT INTO Avvocato(Nome, Cognome, Studio)"\
          " VALUES  (%s, %s, %s)"
    try:
        nome = fak.first_name() 
        last = fak.last_name()
        studio = fak.text(10)
        values = (nome, last, studio)
        avvocati.append(values)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

for i in range(0, impegno):
    print(f"Impegno {i}")
    sql = "INSERT INTO Impegno(Denominazione, Tipo, Nome, Cognome, Studio)"\
          " VALUES  (%s, %s, %s, %s, %s)"
    try:
        r = random.choice(cot)
        a = random.choice(avvocati)
        denom = r[0]
        tipo = r[1]
        nome = a[0]
        last = a[1]
        studio = a[2]
        values = (denom, tipo, nome, last, studio)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

collab = [] 
for i in range(0, collaboratore):
    print(f"Collaboratore {i}")
    sql = "INSERT INTO Collaboratore(PartitaIVA, CF, Provincia, CAP, Comune, Citta, Indirizzo)"\
          " VALUES  (%s, %s, %s, %s, %s, %s, %s)"
    try:

        PartitaIVA = random.choice(["00000000000", fak.company_vat().split('T')[1]])
        CF = fak.ssn()
        Comune = fak.administrative_unit()
        Citta = random.choice([Comune, fak.city(), fak.city()])
        CAP = fak.postcode()
        Indirizzo = fak.street_name()
        Provincia = fak.state()
        values = (PartitaIVA, CF, Provincia, CAP, Comune, Citta, Indirizzo)
        collab.append(values)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

for i in range(0, collaboraz):
    print(f"Collaorazione {i}")
    sql = "INSERT INTO Collaboraz(Denominazione, Tipo, PartitaIVA, CF, LavoroSvolto)"\
          " VALUES  (%s, %s, %s, %s, %s)"
    try:
        l = random.choice(lavori_inseriti)
        c = random.choice(collab)
        Denom = l[0]
        Tipo = l[1]
        PartitaIVA = c[0]
        IDAlbo = c[-1]
        CF = c[1]
        LavoroSvolto = fak.text(100)
        values = (Denom, Tipo, PartitaIVA, CF, LavoroSvolto)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

for i in range(0, rappresentanza):
    print(f"Rappresentanza {i}")
    sql = "INSERT INTO Rappresent(PartitaIVACliente, CFCliente, TipoCliente, PartitaIVAPersona, CFPersona, DataInserimento, TipoPersona)"\
          " VALUES  (%s, %s, %s, %s, %s, %s, %s)"
    try:
        c = random.choice(CON)
        i = random.choice(IMP)
        p = random.choice(persona)
        r = random.choice([i, c])
        PartitaIVACliente = r[0]
        CFR = r[1]
        TipoCliente = r[2]
        PartitaIVAP = p[0]
        CFP = p[1]
        TipoPersona = "PER"
        DataInizio = random_date("1910/01/01", "2020/01/01", random.random())
        values = (PartitaIVACliente, CFR, TipoCliente, PartitaIVAP, CFP, DataInizio, TipoPersona)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)



for i in range(0,prestaz):
    print(f"Prestazione {i}")
    sql = "INSERT INTO Prestaz(Denominazione, Tipo,TipoCliente, PartitaIVA, CF)"\
          " VALUES  (%s, %s, %s, %s, %s)"
    try:
        c = random.randint(0, len(clienti))
        l = random.randint(0, len(lavori_inseriti))
        Denom = lavori_inseriti[l][0]
        Tipo = lavori_inseriti[l][1]
        PartitaIVA = clienti[c][0]
        CF = clienti[c][1]
        values = (Denom, Tipo, clienti[c][2], PartitaIVA, CF)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

for i in range(0, fatture):
    print(f"Fattura {i}")
    sql = "INSERT INTO Fattura(NumeroFat, DenomLavoro, TipoLavoro, PartitaIVA, CF, Tipo,  Tipologia, Modalita, Imponibile, CostiEsentiIVA, RitenutaAcc, RitenutaRistr, DataFaT, DataPreFat, DataInc)"\
          " VALUES  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        l = random.choice(lavori_inseriti)
        c = random.choice(clienti)

        numfat = random.randint(1111111, 99999999) 
        denom = l[0]
        tipo = l[1]
        pariva = c[0]
        cf = c[1]
        tipocliente = c[2]

        tipologia       = "tipo"
        modlita         = "modalita"
        imponibile      = random.randint(10000, 1000000)
        costiesentiiva  = random.randint(100, imponibile-1000)
        ritenutaacc     = random.randint(100, imponibile-1000)
        ritenutarist    = random.randint(100, imponibile - 1000)
        dataemprefat    = random_date("2005/01/01", "2020/01/01", random.random())
        dataemfat       = random_date(dataemprefat, "2020/01/01", random.random())
        datainc         = random_date(dataemfat, "2020/01/01", random.random())
        values = (numfat, denom, tipo, pariva, cf,tipocliente, tipologia, modlita, imponibile, costiesentiiva, ritenutaacc, ritenutarist, dataemfat, dataemprefat, datainc)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)
pablodb.commit()

for i in range(0,partecip):
    print(f"Partecip {i}")
    sql = "INSERT INTO Partecip(DenomLavoro, PTipo, PTecnico)"\
          " VALUES  (%s, %s, %s)"
    try:
        d = random.choice(lavori_inseriti)
        t = random.choice(codici_tecnici) 
        values = (d[0], d[1], t)
        cursor.execute(sql, values)
    except Exception as err:
        print(err)

pablodb.commit()

contatti = [] 
#Contatti
for i in range(1,contatto):
    print(f"contatto {i}")
    sql = "INSERT INTO Contatto (Titolo, Dato, Tipo, TipoCliente,PartitaIVACliente, CFCliente, PartitaIVACollab, CFCollab, NomeAVV, CognmomeAvv, StudioAvv, CFTecnico)"\
                        "VALUES (%s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s)"
    Tipo = random.choice(["cell", "tel", "email", "whapp", "pec"])
    assoc_clienti = clienti
    if Tipo != "Email":
        Dato = fak.phone_number()
    else:
        Dato = fak.email()
    Titolo = fak.text(20) 
   
    PartitaIVACliente = None
    CFCliente = None
    TipoCliente = None
    PartitaIVACollab = None 
    CFCollab = None 
    NomeAvv = None  
    CognomeAvv = None 
    StudioAvv = None 
    CFTecnico = None

    c = random.choice([1,2,3,4])
    if c == 1: #cliente
        cl = random.choice(clienti)
        PartitaIVACliente = cl[0]
        CFCliente = cl[1]
        TipoCliente = cl[2]
    elif c == 2:
        cl = random.choice(collab)
        PartitaIVACollab = cl[0] 
        CFCollab = cl[1] 
    elif c == 3:
        cl = random.choice(avvocati)
        NomeAvv = cl[0]  
        CognomeAvv = cl[1] 
        StudioAvv = cl[2] 
    else:
        cl = random.choice(codici_tecnici)
        CFTecnico = cl 

    try:
        values = (Titolo, Dato, Tipo, TipoCliente, PartitaIVACliente, CFCliente, PartitaIVACollab, CFCollab, NomeAvv, CognomeAvv, StudioAvv, CFTecnico)
        cursor.execute(sql, values) 
        contatti.append(values)
    except Exception as err:
        print(values)
        print(err)
pablodb.commit()
