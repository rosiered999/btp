#!/bin/bash

CMD1="python conn_comp2.py"
CMD2="python affine.py rand_"
for i in 11 23
do
    ext=".PNG"
    fol="/"
    st2=$i$fol
    st=$i$ext
    echo $st, $ext
    $CMD1 $st
    $CMD2$st2
done















#problems for 6 22 32 35 - first layer
# problems for 2 3 4 5 7 8 9 13 14 15 16 21 25 26 27 29 30 34 36
# -merge them if very close
# width or height is twice normal then divide

#### NO PROBLEMS - 1 10 11 12 17 18 19 20 23 24 28 31 33

## DEMO PROBLEMS 11, 23,
