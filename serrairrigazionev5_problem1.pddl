(define (problem istanza1) (:domain serrairrigazionev5)
(:objects 
lattuga - pianta 

irrigatore-lattuga - irrigatore

serbatoio1-serbatoio
)

(:init

(collega-irrigatore-pianta lattuga irrigatore-lattuga)

    (lunedi-giorno)
    (mattina-momento)


(umidita-basso lattuga)


(=(quantita-acqua-pianta lattuga)1)


(=(utilizzi-irrigatore irrigatore-lattuga)0)

(=(livello-serbatoio)5)

(in-uso irrigatore-lattuga)



(=(effettuato-degrado-giorno lattuga)0)



)

(:goal (and (umidita-alto lattuga) (not (umidita-medio lattuga)) (not (umidita-basso lattuga))

(in-uso irrigatore-lattuga)



(=(effettuato-degrado-giorno lattuga)6)




 (domenica-giorno) (sera-momento)

))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
