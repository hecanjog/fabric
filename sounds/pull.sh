#!/usr/bin/env bash

######################################
# Pulls sounds from magic.hecanjog.com
######################################


##
# Vorms remix for Collections of Colonies of Bees
rsync -avz somagical@magic.hecanjog.com:fabric/sounds/vorms/ vorms/ 

##
# 1of by Rough Weather
rsync -avz somagical@magic.hecanjog.com:fabric/sounds/1of/ 1of/

##
# Computer Music With Voices interlude for Eric & Magill
#rsync -avz somagical@magic.hecanjog.com:fabric/sounds/magill_interlude/ magill_interlude/
