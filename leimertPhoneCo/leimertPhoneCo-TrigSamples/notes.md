## notes

### autostart

Put the following in a file called `autostart.sh`

```bash
#!/bin/bash
export PATH=/usr/local/bin:$PATH
export DISPLAY=:0.0
sleep 5 # can be lower (5) for rpi3
#sh ~/.jackdrc & sleep 3 # I used to have to do this but now I don't?

printf "\n\nSTARTING SC!!!!!!!!!\n\n"

sclang /home/sound/leimertPhoneCo-TrigSamples/samplePlayer.scd &

sleep 3

printf "\n\nSTARTING PYTHON!!!!!!!!!\n\n"

python3 /home/sound/leimertPhoneCo-TrigSamples/buttonController.py &

sleep 3

printf "\n\nGO!!!!!!!!!\n\n"

```
