import sqlite3
import header

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    ENDC = '\033[0m'

def test_db_connection():
    b_succ = True
    db_intern = 'instance/cisdb.db'
    db_extern = 'instance/dbext.db'
    try:
        sqlite3.connect('file:instance/cisdb.db?mode=rw', uri=True) 
        sqlite3.connect('file:instance/dbext.db?mode=rw', uri=True)
    except sqlite3.OperationalError:
        b_succ = False
        print(colors.RED + "test_db_connection failure" + colors.ENDC)

    return b_succ

def test_mb_gehalt():
    b_succ = True
    b_succ &= ( True
        #Diese Werte sind anhand der Standartwerte ermittelt, und müssen ggf. bei erweiterung der Beispieldaten ergänzt werden.
        #Testdaten ergänze ich noch, einfach in den Beispieldaten. Diese Tests sind ja nur für die Entwicklung.
        & (header.mitarbeiter_beruf_dif(0) == 35.5)
        & (header.mitarbeiter_beruf_dif(1) == 100)
        & (header.mitarbeiter_beruf_dif(2) == 10.5)
        & (header.mitarbeiter_beruf_dif(3) == 100)
        #Alle sind 0, da wir nur testen ob der Mitarbeiter mehr als andere mit dem gleichen beruf verdienen, wir aber nur ein Bsp. pro beruf haben.
        & (header.mitarbeiter_dif(0) == 0)
        & (header.mitarbeiter_dif(1) == 0)
        & (header.mitarbeiter_dif(2) == 0)
        & (header.mitarbeiter_dif(3) == 0)
        )
    # print("mitarbeiter_beruf_dif(0) = " + str(header.mitarbeiter_beruf_dif(0)))
    # print("mitarbeiter_beruf_dif(1) = " + str(header.mitarbeiter_beruf_dif(1)))
    # print("mitarbeiter_beruf_dif(2) = " + str(header.mitarbeiter_beruf_dif(2)))
    # print("mitarbeiter_beruf_dif(3) = " + str(header.mitarbeiter_beruf_dif(3)))
    # print("mitarbeiter_dif(0) = " + str(header.mitarbeiter_dif(0)))
    # print("mitarbeiter_dif(1) = " + str(header.mitarbeiter_dif(1)))
    # print("mitarbeiter_dif(2) = " + str(header.mitarbeiter_dif(2)))
    # print("mitarbeiter_dif(3) = " + str(header.mitarbeiter_dif(3)))
    return b_succ

def test_all():
    b_succ = True
    #begin list of tests
    b_succ &= test_db_connection()
    b_succ &= test_mb_gehalt()
    #end list of tests

    print(colors.GREEN + "ALL TESTS WERE SUCCESSFUL" + colors.ENDC if b_succ else colors.RED + "SOME TESTS FAILED" + colors.ENDC)

########

#hosting the login, just to have an app to run the database commands
@header.app.route("/")
def home():
    header.mitarbeiter_beruf_dif(0)
    test_all()
    return header.render_template("login.html")

if __name__ == '__main__':
    header.app.run(debug=True)


# Wir programmieren die Funktionen zur Korruptionsprüfung 
# SQL Abfragen für die Korruptionsprüfungen werden in der header.py definiert und dann in der tets.py getestet & dann un der korruptionspruefung.py genutzt
# JG: Projekt
# TB: Mitarbeiter Gehalt
# TB: Wir gucken in der Tabelle Beruf, wo der Beruf gleich ist, gucken ob das Gehalt extrem unterschiedlich ist. Ab wie viel Prozentgehaltsunterschied ist es komisch. 
# RC: Vetternwirtschaft
# JB: Geldfluß 

# Überprüfen ob das Fahrzeug (z.B. Boot -> Boot -> Wert) mit dem Gehalt des Fahrzeugbesitzers übereinstimmen kann.