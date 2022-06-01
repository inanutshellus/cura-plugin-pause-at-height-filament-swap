# cura-plugin-pause-at-height-filament-swap

An [Ultimaker Cura](https://ultimaker.com/software/ultimaker-cura) plugin to pause the printer between layers or at a given height. 

Specifically, this is for printers that do not yet support the `M600` (pause and wait) Marlin GCODE command.

This script tells the printer to make a noise at a given height/layer, then "dwell" for a few seconds before continuing. During this "dwelling" period, you can use your printer's on-screen Pause feature to stop between layers, letting you change filament or affect your print before resuming. Certainly M600 is preferable to this solution, so pester your printer's vendor about implementing it ASAP! :^)

Notably this was originally written as "AnycubicI3MegaPauseAtHeight.py" by [julijanz](https://www.thingiverse.com/julijanz/designs) on [Thingiverse](https://www.thingiverse.com/thing:3353615/) and later updated by [ModernHobbyist](https://www.thingiverse.com/modernhobbyist/designs) on [Thingiverse](https://www.thingiverse.com/thing:4160010). 

This version just tries to fix a few minor bugs in the previous iterations.

1. The script had an issue that made it unusable if your "Resume" button didn't (accidentally/erroneously) set your positioning to absolute before it exited. In this case, the print nozzle would instead wander to the max X,Y coordinates and jitter and panic there whilst dumping plastic. 
2. The script had an invalid relative position bug
3. The script harmlessly used `G1` instead of `G0` (extrude while moving)... so I fixed that.
