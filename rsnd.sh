#!/bin/bash
if [[ $1 == "local" || $1 == "l" ]] 
    then rsync -avz --exclude-from="rsnd-exclude.txt" . erik@shampooserve:/home/erik/fabric/
    ssh erik@shampooserve "cd fabric/ ; python $2"
    rsync -avz erik@shampooserve:/home/erik/fabric/renders/ renders/
elif [[ $1 == "remote" || $1 == "r" ]]
    then rsync -avz --exclude-from="rsnd-exclude.txt" . erik@shampoo.bonusroom.org:/home/erik/fabric/
    ssh erik@shampoo.bonusroom.org "cd fabric/ ; python $2" 
    rsync -avz erik@shampoo.bonusroom.org:/home/erik/fabric/renders/ renders/ 
elif [[ $1 == "sync" || $1 == "s" ]]
    then if [[ $2 == "local" || $2 == "l" ]]
        then rsync -avz erik@shampooserve:/home/erik/fabric/renders/ renders/
    elif [[ $2 == "remote" || $2 == "r"  || $2 == "" ]]
        then rsync -avz erik@shampoo.bonusroom.org:/home/erik/fabric/renders/ renders/ 
    fi
fi
