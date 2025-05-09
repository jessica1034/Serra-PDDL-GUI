;;ricarica a manutenzione esguite solo 1 volta
(define (domain serrairrigazionev5)

(:requirements :strips :fluents :durative-actions :timed-initial-literals :typing :conditional-effects :negative-preconditions :duration-inequalities :equality :disjunctive-preconditions)

(:types 
    pianta
    irrigatore

    

)

(:predicates 
(umidita-basso ?p - pianta)
(umidita-medio ?p - pianta)
(umidita-alto ?p - pianta)
(in-uso ?i - irrigatore)
(manutenzione-terminata ?i - irrigatore)
(collega-irrigatore-pianta ?p-pianta ?i - irrigatore)
    (lunedi-giorno)
    (martedi-giorno)
    (mercoledi-giorno)
    (giovedi-giorno)
    (venerdi-giorno)
    (sabato-giorno)
    (domenica-giorno)

    (mattina-momento)
    (pomeriggio-momento)
    (sera-momento)

    (degrado-completato ?p - pianta)

)



(:functions 
(quantita-acqua-pianta ?p - pianta) ;; per passare a umidità alta
(livello-serbatoio)
(utilizzi-irrigatore ?i - irrigatore)
(effettuato-degrado-giorno ?p)


)

;;collega irrigatore pianta: associa 1 irrigatore a 1 pianta 

(:action irrigazione
    :parameters (?p - pianta ?i - irrigatore) ;; solo quando è umidità bassa
    :precondition (and  (collega-irrigatore-pianta ?p ?i) (umidita-basso ?p) (in-uso ?i) (<(utilizzi-irrigatore ?i)1) (>(livello-serbatoio)(quantita-acqua-pianta ?p)) (mattina-momento) (not (pomeriggio-momento)) (not (sera-momento)))  ;;è mattina
    :effect (and (umidita-alto ?p) (not (umidita-basso ?p)) (not (umidita-medio ?p)) 
    (decrease (livello-serbatoio) (quantita-acqua-pianta ?p))
    (increase (utilizzi-irrigatore ?i) 1)
  
))



(:action ricarica-serbatoio
    :parameters ()
    :precondition (<=(livello-serbatoio) 1)
    :effect (and(assign (livello-serbatoio) 4))
)


(:action esegui-manutenzione
  :parameters (?i - irrigatore)
  :precondition (and (=(utilizzi-irrigatore ?i) 1)(pomeriggio-momento) (not(mattina-momento)) (not(sera-momento)))
  :effect (and
  (assign (utilizzi-irrigatore ?i) 0)
  (not (in-uso ?i))
    (manutenzione-terminata ?i)
   
  )
)

(:action manutenzione-finita
    :parameters (?i - irrigatore)
    :precondition (manutenzione-terminata ?i)
    :effect (and (in-uso ?i) )
    
)



;; Avanzamento giorni
(:action martedi-mattina
  :parameters ()
  :precondition (and (lunedi-giorno) (sera-momento))
  :effect (and (not (lunedi-giorno)) (not(sera-momento)) (martedi-giorno) (mattina-momento))
)

(:action mercoledi-mattina
  :parameters ()
  :precondition (and (martedi-giorno) (sera-momento))
  :effect (and (not (martedi-giorno)) (not(sera-momento))(mercoledi-giorno) (mattina-momento))
)

(:action giovedi-mattina
  :parameters ()
  :precondition (and (mercoledi-giorno) (sera-momento))
  :effect (and (not (mercoledi-giorno))(not(sera-momento)) (giovedi-giorno) (mattina-momento))
)

(:action venerdi-mattina
  :parameters ()
  :precondition (and (giovedi-giorno) (sera-momento))
  :effect (and (not (giovedi-giorno)) (not(sera-momento))(venerdi-giorno) (mattina-momento))
)

(:action sabato-mattina
  :parameters ()
  :precondition (and (venerdi-giorno) (sera-momento))
  :effect (and (not (venerdi-giorno)) (not(sera-momento))(sabato-giorno) (mattina-momento))
)

(:action domenica-mattina
  :parameters ()
  :precondition (and (sabato-giorno) (sera-momento))
  :effect (and (not (sabato-giorno))(not(sera-momento)) (domenica-giorno) (mattina-momento))
)

;; Azioni per il passaggio tra i momenti del giorno

;; POMERIGGIO
(:action pomeriggio
  :parameters ()
  :precondition (and (mattina-momento) )
  :effect (and (not (mattina-momento)) (pomeriggio-momento))
)

;; SERA
(:action sera
  :parameters ()
  :precondition (and (pomeriggio-momento) )
  :effect (and (not (pomeriggio-momento)) (sera-momento))
)


;; dire che o una o l'altra
(:action umidita-media
    :parameters (?p - pianta)
    :precondition (and (not(degrado-completato ?p)) (sera-momento) (not (mattina-momento)) (not (pomeriggio-momento)) (umidita-alto ?p) (not (umidita-medio ?p)) (not (umidita-basso ?p)))
    :effect (and (umidita-medio ?p) (not(umidita-alto ?p))(not (umidita-basso ?p))(degrado-completato ?p)
    (increase (effettuato-degrado-giorno ?p) 1))
)
(:action umidita-bassa
    :parameters    (?p - pianta)
    :precondition (and (not(degrado-completato ?p)) (sera-momento) (not (mattina-momento)) (not (pomeriggio-momento)) (umidita-medio ?p) (not (umidita-alto ?p)) (not (umidita-basso ?p)))
    :effect (and (umidita-basso ?p) (not(umidita-alto ?p))(not (umidita-medio ?p))(degrado-completato ?p)
    (increase (effettuato-degrado-giorno ?p) 1))
)

(:action resetta-umidita
  :parameters (?p - pianta )
  :precondition (pomeriggio-momento)
  :effect (not(degrado-completato ?p)) 
)
)
