(define (problem istanza1) (:domain serrairrigazionev5)
(:objects 
lattuga - pianta 
irrigatore-lattuga - irrigatore
)

(:init
(collega-irrigatore-pianta lattuga irrigatore-lattuga)

(lunedi-giorno)
(mattina-momento)

(umidita-basso lattuga)

(in-uso irrigatore-lattuga)

(=(quantita-acqua-pianta lattuga)1)

(=(utilizzi-irrigatore irrigatore-lattuga)0)

(=(livello-serbatoio)4)

(=(effettuato-degrado-giorno lattuga)0)
)

(:goal (and (umidita-alto lattuga) (not (umidita-medio lattuga)) (not (umidita-basso lattuga))

(in-uso irrigatore-lattuga)

(=(effettuato-degrado-giorno lattuga)6)

(domenica-giorno) (sera-momento)

))
)
