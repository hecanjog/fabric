#!/usr/bin/env bash

#####################################
# Pushes sounds to magic.hecanjog.com
#####################################


##
# Vorms remix for Collections of Colonies of Bees
rsync -avz vorms/ somagical@magic.hecanjog.com:fabric/sounds/vorms/ 

##
# 1of by Rough Weather
rsync -avz 1of/ somagical@magic.hecanjog.com:fabric/sounds/1of/ 

##
# Computer Music With Voices interlude for Eric & Magill
#rsync -avz magill_interlude/ somagical@magic.hecanjog.com:fabric/sounds/magill_interlude/ 
