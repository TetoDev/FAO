BEGIN PGM Capto MM
;postprocesse  le 25/03/2026
BLK FORM 0.1 Z X-30 Y-30 Z-50
BLK FORM 0.2 X30 Y30 Z0
;
FN 18: SYSREAD Q30 = ID230 NR3 IDX3
L ZQ30 R0 FMAX M91
M129
PLANE RESET TURN FMAX
TOOL CALL 108 Z S10000 F1400
TOOL CALL S10000
M3 M8
M126
L X0 Y-105 R0 FMAX ;Mettre ici les coordonnées X et Y du premier point
L B-90 C103.959 F1400 ;Mettre ici les coordonnées B et C du premier point
M114
L XpremierPoint YpremierPoint ZpremierPoint BpremierPoint CpremierPoint
.
.
.
Mettre ici les différentes coordonnées des points de passage (une ligne par poit)
.
.
.
M127 M115 ;retrait fonction M126
M9
L M140 MB MAX ;degagement outil suivant son axe
M5
M129
L Y225 FMAX M92;degagement outil en Y
PLANE RESET TURN FMAX ;remise a B0 CO
L X-200 FMAX M92;deplacement piece devant operateur
M10 M15 ;blocage axes rotatifs
M2
END PGM 