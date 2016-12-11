#
# Directed graph - in-degree Distribution. G(4039, 88234). 1314 (0.3253) nodes with in-deg > avg deg (43.7), 597 (0.1478) with >2*avg.deg (Sat Dec 10 21:11:02 2016)
#

set title "Directed graph - in-degree Distribution. G(4039, 88234). 1314 (0.3253) nodes with in-deg > avg deg (43.7), 597 (0.1478) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "In-degree"
set ylabel "Count"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'inDeg.example.png'
plot 	"inDeg.example.tab" using 1:2 title "" with linespoints pt 6
