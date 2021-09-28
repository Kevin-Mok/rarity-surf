#! /usr/bin/fish

cd ~/coding/rarity-sniper > /dev/null
set revealed (python reveal.py | tail -n1)
echo (date)
echo $revealed
if test $revealed = "True"
    notify-send "Hearts revealed"
end
