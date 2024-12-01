# Alternative Filament Swap Plugin for Ultimaker Cura

An [Ultimaker Cura](https://ultimaker.com/software/ultimaker-cura) plugin to play music and pause the printer between layers or at a given height. 

Specifically, this is for printers that do not yet support the `M600` (pause and <b>wait</b>) Marlin GCODE command.

This script tells the printer to play a tune at a given height/layer, then "dwell" for a while before continuing. 

During this "dwelling" period, you can use your printer's on-screen Pause feature to wait between layers, letting you change filament or affect your print before resuming. Certainly M600 is preferable to this solution, so pester your printer's vendor about implementing it ASAP! :^)

# HOW TO USE

* Download the `PauseAtHeightOptions.py` and save it into your `$HOME\AppData\Roaming\cura\$VERSION\scripts` directory.
* Open (or restart) Cura
* Click "Extensions" &gt; "Post Processing" &gt; Modify G-Code
* The "Post Processing Plugin" dialog appears &gt; Click "Add a script"
* In the list click "Pause At Height Alternative"
* From here, each option should have its own documentation (e.g. "pause at a certain height - e.g. 5mm up" or "pause at layer - e.g. pause at layer 25").

# Sources

Notably this was originally written as "AnycubicI3MegaPauseAtHeight.py" by [julijanz](https://www.thingiverse.com/julijanz/designs) on [Thingiverse](https://www.thingiverse.com/thing:3353615/) and later updated by [ModernHobbyist](https://www.thingiverse.com/modernhobbyist/designs) on [Thingiverse](https://www.thingiverse.com/thing:4160010). 

# Why use THIS version? 

This version just tries to fix a few minor bugs in the previous iterations.

1. The script had an issue that made it unusable if your "Resume" button didn't (accidentally/erroneously) set your positioning to absolute before it exited. In this case, the print nozzle would instead wander to the max X,Y coordinates and jitter and panic there whilst dumping plastic. 
2. The script had another invalid relative position bug in which it attempted to move Z but did so using the wrong command.
3. The script harmlessly used `G1` (move while extruding) instead of `G0` (move)... so I fixed that.
