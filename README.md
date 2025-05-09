REQUISITI:
- Python 3.x
- Pygame: Libreria per la grafica.
- Java: Necessario per eseguire ENHSP.
- ENHSP: File enhsp.jar e i file PDDL devono essere nella stessa directory.


STEP DA SEGUIRE PER LA VISUALIZZAZIONE DELLA GUI: 
1. Scaricare tutto il contenuto della repository in unica cartella.
2. Nella medesima cartella deve essere contenuto il planner enhsp.jar
3. Aprire la cartella da prompt dei comandi e in seguito digitare 'Serragui.py'
4. Verrà chiesto di inserire il nome del problemfile (con .pddl) e il nome della modalità di ENSHP ('opt-hrmax' o 'sat-hadd') da prompt dei comandi
5. Segue l'apertura della gui con l'esecuzione del problem selezionato.

STEP DA SEGUIRE PER LA VISUALIZZAZIONE DEL PLAN DA PROMPT DEI COMANDI: 
1. Scaricare tutto il contenuto della repository in unica cartella.
2. Nella medesima cartella deve essere contenuto il planner enhsp.jar
3. Digitare:
   
     java -jar enhsp.jar -o serrairrigazionev5_domain.pddl -f serrairrigazionev5_problem1.pddl –planner opt-hrmax; PROBLEM 1 - OPTIMAL
     java -jar enhsp.jar -o serrairrigazionev5_domain.pddl -f serrairrigazionev5_problem1.pddl –planner sat-hadd; PROBLEM 1 - SUBOPTIMAL

     java -jar enhsp.jar -o serrairrigazionev5_domain.pddl -f serrairrigazionev5_problem2.pddl –planner opt-hrmax; PROBLEM 2 - OPTIMAL
     java -jar enhsp.jar -o serrairrigazionev5_domain.pddl -f serrairrigazionev5_problem2.pddl –planner sat-hadd; PROBLEM 2 - SUBOPTIMAL

     java -jar enhsp.jar -o serrairrigazionev5_domain.pddl -f serrairrigazionev5_problem3.pddl –planner opt-hrmax; PROBLEM 3 - OPTIMAL
     java -jar enhsp.jar -o serrairrigazionev5_domain.pddl -f serrairrigazionev5_problem3.pddl –planner sat-hadd; PROBLEM 3 - SUBOPTIMAL


ATTENZIONE:    
Con il terzo problema (serrairrigazionev5_problem3) potrebbero esserci dei rallentamenti nel caricamento della gui, sarà necessario attendere qualche istante.

Per ulteriori informazioni verificare la sezione "Navigazione piano" della documentazione.
