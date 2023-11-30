import sqlite3

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
    
def test_all():
    b_succ = True
#begin list of tests
    b_succ &= test_db_connection()
#end list of tests
    print(colors.GREEN + "ALL TESTS WERE SUCCESSFUL" + colors.ENDC if b_succ else colors.RED + "SOME TESTS FAILED" + colors.ENDC)
########
test_all()



# Wir programmieren die Funktionen zur Korruptionsprüfung 
# SQL Abfragen für die Korruptionsprüfungen werden in der header.py definiert und dann in der tets.py getestet & dann un der korruptionspruefung.py genutzt
# JG: Projekt
# TOM: Mitarbeiter Gehalt
# TOM: Wir gucken in der Tabelle Beruf, wo der Beruf gleich ist, gucken ob das Gehalt extrem unterschiedlich ist. 
# TOM: -> Ab wie viel Prozentgehaltsunterschied ist es komisch. 
# RObbin: Vetternwirtschaft
# JONAS: Geldfluß 

# Überprüfen ob das Fahrzeug (z.B. Boot -> Boot -> Wert) mit dem Gehalt des Fahrzeugbesitzers übereinstimmen kann.