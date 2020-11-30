import pandas as pd
import requests
import time
#import server
try:
    url = 'https://orienteerumine.ee/eteenused/kood_sime.php'
    myfile = requests.get(url)
    open('eoljooksjad.txt', 'wb').write(myfile.content)
except: pass

def oigeSi(others,kas_si):
    if kas_si == False:
        uus_si = input(others["Eesnimi"]+", kui sa kasutad " + str(others["Si"]) + " pulka, vajuta Enter, muul juhul pulga number: ")
        global fail
        if uus_si != "":
            return int(uus_si)
        elif uus_si == "vale":
            fail = True
            return 0
        else:
            return others["Si"]
    else: return others["Si"]



def kasLaps(eol, aasta=None):
    if eol < 49999 and eol >= 2:
        aasta, kuu, paev = vanused[str(eol)].split("-")
        if int(aasta) >= 2001:
            laps = "1"
        else:
            laps = 0
    else:
        if int(aasta) >= 2001:
            laps = "1"
        else:
            laps = 0
    if laps == "1":
        return 1
    else:
        return 0


def uusEOL(nimi,sunna,sugu,maakond,klubi="",epost =""):
    fa = open("uuedKoodid.txt", "a", encoding="iso-8859-15")
    #Input
    eesnimi, perekonnanimi = nimi.rsplit(" ", 1)
    lause = eesnimi + ";" + perekonnanimi + ";" + sunna + ";" + sugu + ";" + maakond + ";" + klubi + ";" + epost + "\n"
    fa.write(lause)
    fa.close()
    aasta,kuu,paev = sunna.split("-")
    return aasta


jooksjad = pd.read_table("eoljooksjad.txt", sep=";", index_col=0, encoding="iso-8859-15", header=0,
                         names=["Si", "Eesnimi", "Perekonnanimi", "Klubi", "Sugu"])
jooksjad.index.name = "Kood"

jooksjad.Si = jooksjad.Si.fillna(0)
jooksjad.Si = jooksjad.Si.astype("int64")
vanusedFile = open("vanused.txt", "r")
vanused = {}
mitmes = 1
for i in vanusedFile:
    try:
        koode, aasta = i.rstrip().split(";")
        vanused[koode] = aasta
    except:
        pass

def nimega(nimi):
    eol = 0
    eesnimi, perekonnanimi = nimi.rsplit(" ", 1)
    perekonnanimi = perekonnanimi.title()
    eesnimi = eesnimi.title()
    essa = jooksjad.loc[jooksjad["Perekonnanimi"] == perekonnanimi]
    teine = essa.loc[essa["Eesnimi"] == eesnimi]
    return teine


"""
def teinekontroll(teine):
    if not teine.empty:
        if teine.shape[0] > 1:
            print(teine.to_html())

            print("\n")
            if eol.isdigit(): eol = int(eol)


        if teine.shape[0] == 1:
            for eol, others in teine.iterrows(): pass

    if eol != 0:
        print(eesnimi + ", Sinu EOL kood on " + str(eol) + "! Jäta see endale meelde palun.")
        test = input("Vajuta Enter, et jätkata").lower()
        if test == "puudub":
            eol = 0
        elif test == "vale":
            fail = True

    if eol == 0:
        return (eesnimi,perekonnanimi)
    else:
        return eol
"""
def otsi_si(eol):
    try:
        si = jooksjad.loc[eol]["Si"].array[0]
    except:
        si = jooksjad.loc[eol]["Si"]
    return si


def arvuta(eol, si, eesnimi, perekonnanimi, kas_laps):
    global jooksjad, vanused, mitmes


    aasta = None
    fail = False
    if type(eol) == type(1) and eol != 0 and not fail:
        try:
            jooksja = jooksjad.loc[eol]
            if type(jooksja) != type(pd.Series()):
                try:
                    jooksja.iloc[0][0]
                    jooksja = jooksja.iloc[0]
                except:
                    jooksja = jooksjad.loc[eol]
            eesnimi = jooksja["Eesnimi"]
            perekonnanimi = jooksja["Perekonnanimi"]
            klubi = jooksja["Klubi"]
            sugu = jooksja["Sugu"]
            if si == "":
                si = jooksja["Si"]
            jooksjad = jooksjad.drop(eol)
            jooksjad = jooksjad.append(pd.Series(data = {"Si":si, "Eesnimi":eesnimi, "Perekonnanimi":perekonnanimi,"Klubi":klubi, "Sugu":sugu}, name = eol), ignore_index=False)
        except:
            fail = True
    elif not fail:
        eol = jooksjad.index.max() + 1
        if eol < 50000:
            eol = 50000
        jooksjad.loc[eol] = [si, eesnimi, perekonnanimi, "Eemalda", "M"]
    if not fail:
        # def kinnita():
        if kas_laps == 'Jah':
            lapsed = jooksjad.loc[eol].to_frame().transpose()
            lapsed.to_csv("lasteLoos.txt", mode="a", sep=";", header=False, encoding="iso-8859-15")
        jooksjad.loc[eol].to_frame().transpose().to_csv("Metsas.txt", mode="a", sep=";", header=False,
                                                        encoding="iso-8859-15")

        muuda = jooksjad.loc[eol].to_frame().transpose()
        muuda["Koht"] = mitmes
        mitmes += 1
        muuda.to_csv("koikOsalejad.txt", mode="a", sep=";", header=False, encoding="iso-8859-15")
        jooksjad.to_csv("eoljooksjad.txt", sep=";", header=False, encoding="iso-8859-15")
        print('valmis')

def info(eol,si):
    global jooksjad
    jooksja = jooksjad.loc[eol]
    print(eol,si)
    if type(jooksja) != type(pd.Series()):
        try:
            jooksja.iloc[0][4]
            jooksja = jooksja.iloc[0]
        except:
            jooksja = jooksjad.loc[eol]
    print(jooksja)
    enimi = jooksja["Eesnimi"]
    pnimi = jooksja["Perekonnanimi"]
    klubi = jooksja["Klubi"]
    if si == '':
        si = jooksja['Si']
    data = pd.Series(data={"Si": si, "Eesnimi": enimi, "Perekonnanimi": pnimi, "Klubi": klubi}) #, ignore_index=False
    print(jooksjad.loc[eol])
    return data

if __name__ == "__main__":
    pass


"""
    if eol_v_nimi == "korraldaja":
        eol,si,ees,pere,klubi,sugu = input("eol;si;ees;pere;klubi;sugu: ").split(";")
        jooksjad.loc[eol] = [si, ees, pere, klubi, sugu]
        jooksjad.loc[eol].to_frame().transpose().to_csv("Metsas.txt", mode="a", sep=";", header=False,
                                                            encoding="iso-8859-15")
"""