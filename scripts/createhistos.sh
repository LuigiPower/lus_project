OUTPUT=$1
TRAIN=$2

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python3 $DIR/create_histograms.py $TRAIN $OUTPUT.word.txt $OUTPUT.conc.txt $OUTPUT.gen1.txt $OUTPUT.gen2.txt $OUTPUT.gen3.txt

sort -k2 -n -r $OUTPUT.word.txt > $OUTPUT.word.sorted.txt
sort -k2 -n -r $OUTPUT.conc.txt > $OUTPUT.conc.sorted.txt
sort -k2 -n -r $OUTPUT.gen1.txt > $OUTPUT.gen1.sorted.txt
sort -k2 -n -r $OUTPUT.gen2.txt > $OUTPUT.gen2.sorted.txt
sort -k2 -n -r $OUTPUT.gen3.txt > $OUTPUT.gen3.sorted.txt
