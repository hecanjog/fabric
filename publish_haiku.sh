#!/bin/zsh
rm renders/haiku*
python haiku.py

for f in renders/haiku*; do
    fm=${f/renders\///};
    sox -S $f -C 320 $m/he.can.jog/haiku/${fm/.wav/.mp3} norm
    scp $m/he.can.jog/haiku/${fm/.wav/.mp3} hecanjog@hecanjog.com:~/sounds.hecanjog.com/haiku/
done
