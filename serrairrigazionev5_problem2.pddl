(define (problem istanza2) (:domain serrairrigazionev5)
(:objects 
lattuga - pianta 
pomodori - pianta

irrigatore-lattuga - irrigatore
irrigatore-pomodori - irrigatore
)

(:init

(collega-irrigatore-pianta lattuga irrigatore-lattuga)
(collega-irrigatore-pianta pomodori irrigatore-pomodori)
    (lunedi-giorno)
    (mattina-momento)


(umidita-basso lattuga)
(umidita-alto pomodori)

(=(quantita-acqua-pianta lattuga)3)
(=(quantita-acqua-pianta pomodori)3)

(=(utilizzi-irrigatore irrigatore-lattuga)0)
(=(utilizzi-irrigatore irrigatore-pomodori)0)


(=(livello-serbatoio)4)

(in-uso irrigatore-lattuga)
(in-uso irrigatore-pomodori)

(=(effettuato-degrado-giorno pomodori)0)
(=(effettuato-degrado-giorno lattuga)0)



)

(:goal (and (umidita-alto pomodori) (umidita-alto lattuga) (not (umidita-medio pomodori)) (not (umidita-basso pomodori)) 
(not (umidita-medio lattuga)) (not (umidita-basso lattuga))

(in-uso irrigatore-lattuga)
(in-uso irrigatore-pomodori)

(=(effettuato-degrado-giorno pomodori)6)
(=(effettuato-degrado-giorno lattuga)6)




 (domenica-giorno) (sera-momento)

))

)
