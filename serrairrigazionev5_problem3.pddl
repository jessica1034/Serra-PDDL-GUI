(define (problem istanza2) (:domain serrairrigazionev5)
(:objects 
lattuga - pianta 
pomodori - pianta
carote - pianta

irrigatore-lattuga - irrigatore
irrigatore-pomodori - irrigatore
irrigatore-carote - irrigatore
)

(:init

(collega-irrigatore-pianta lattuga irrigatore-lattuga)
(collega-irrigatore-pianta pomodori irrigatore-pomodori)
(collega-irrigatore-pianta carote irrigatore-carote)
    (lunedi-giorno)
    (mattina-momento)


(umidita-basso lattuga)
(umidita-basso pomodori)
(umidita-alto carote)

(=(quantita-acqua-pianta lattuga)1)
(=(quantita-acqua-pianta pomodori)2)
(=(quantita-acqua-pianta carote)3)

(=(utilizzi-irrigatore irrigatore-lattuga)0)
(=(utilizzi-irrigatore irrigatore-pomodori)0)
(=(utilizzi-irrigatore irrigatore-carote)0)

(=(livello-serbatoio)4)

(in-uso irrigatore-lattuga)
(in-uso irrigatore-pomodori)
(in-uso irrigatore-carote)

(=(effettuato-degrado-giorno pomodori)0)
(=(effettuato-degrado-giorno lattuga)0)
(=(effettuato-degrado-giorno carote)0)


)

(:goal (and (umidita-alto pomodori) (umidita-alto lattuga) (umidita-alto carote) (not (umidita-medio pomodori)) (not (umidita-basso pomodori)) (not (umidita-medio carote)) (not(umidita-basso carote))
(not (umidita-medio lattuga)) (not (umidita-basso lattuga))

(in-uso irrigatore-lattuga)
(in-uso irrigatore-pomodori)
(in-uso irrigatore-carote)

(=(effettuato-degrado-giorno pomodori)6)
(=(effettuato-degrado-giorno lattuga)6)
(=(effettuato-degrado-giorno carote)6)



 (domenica-giorno) (sera-momento)

))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
