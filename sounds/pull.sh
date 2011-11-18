#!/usr/bin/env bash

######################################
# Pulls sounds from magic.hecanjog.com
######################################

##
# Computer Music With Voices interlude for Eric & Magill
rsync -avz somagical@magic.hecanjog.com:fabric/sounds/magill_interlude/ magill_interlude/
