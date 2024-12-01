# Copyright (c) 2019 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from ..Script import Script

from UM.Application import Application #To get the current printer's settings.
from UM.Logger import Logger

from typing import List, Tuple

class PauseAtHeightOptions(Script):
    def __init__(self) -> None:
        super().__init__()

    def getSettingDataString(self) -> str:
        return """{
            "name": "Pause at Height with Options",
            "key": "PauseAtHeightOptions",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "pause_at":
                {
                    "label": "Pause at",
                    "description": "Whether to pause at a certain height or at a certain layer.",
                    "type": "enum",
                    "options": {"height": "Height", "layer_no": "Layer No."},
                    "default_value": "height"
                },
                "pause_height":
                {
                    "label": "Pause Height",
                    "description": "At what height should the pause occur?",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 5.0,
                    "minimum_value": "0",
                    "minimum_value_warning": "0.27",
                    "enabled": "pause_at == 'height'"
                },
                "pause_layer":
                {
                    "label": "Pause Layer",
                    "description": "At what layer should the pause occur?",
                    "type": "int",
                    "value": "math.floor((pause_height - 0.27) / 0.1) + 1",
                    "minimum_value": "0",
                    "minimum_value_warning": "1",
                    "enabled": "pause_at == 'layer_no'"
                },
                "play_extended_melody":
                {
                    "label": "Play longer melody? (Y/N)",
                    "description": "If you're in the same room as your printer the short melody is great. If you wander, try the longer song.",
                    "type": "str",
                    "default_value": "N"
                },
                "head_park_x":
                {
                    "label": "Park Print Head X",
                    "description": "What X location does the head move to when pausing.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "head_park_y":
                {
                    "label": "Park Print Head Y",
                    "description": "What Y location does the head move to when pausing.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "retraction_amount":
                {
                    "label": "Retraction",
                    "description": "How much filament must be retracted at pause.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "retraction_speed":
                {
                    "label": "Retraction Speed",
                    "description": "How fast to retract the filament.",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 25
                },
                "extrude_amount":
                {
                    "label": "Extrude Amount",
                    "description": "How much filament should be extruded after pause. This is needed when doing a material change on Ultimaker2's to compensate for the retraction after the change. In that case 128+ is recommended.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "extrude_speed":
                {
                    "label": "Extrude Speed",
                    "description": "How fast to extrude the material after pause.",
                    "unit": "mm/s",
                    "type": "float",
                    "default_value": 3.3333
                },
                "redo_layers":
                {
                    "label": "Redo Layers",
                    "description": "Redo a number of previous layers after a pause to increases adhesion.",
                    "unit": "layers",
                    "type": "int",
                    "default_value": 0
                },
                "standby_temperature":
                {
                    "label": "Standby Temperature",
                    "description": "Change the temperature during the pause. If you plan on doing a filament swap, this should not be zero.",
                    "unit": "°C",
                    "type": "int",
                    "default_value": 0
                },
                "wait_on_pause_click":
                {
                    "label": "Wait on Pause click",
                    "description": "How long in seconds the program should wait for the usr to click the on-screen 'Pause' button. After clicking on Pause, replace the filament or what-have-you. Then click the on-screen 'Continue' button. If you do not click on Pause in the time that you set here in seconds, the program will automatically continue printing.",
                    "unit": "sec",
                    "type": "int",
                    "default_value": 10
                },
                "display_text":
                {
                    "label": "Display Text",
                    "description": "Text that should appear on the display while paused. If left empty, there will not be any message.",
                    "type": "str",
                    "default_value": ""
                }
            }
        }"""

    ##  Get the X and Y values for a layer (will be used to get X and Y of the
    #   layer after the pause).
    def getNextXY(self, layer: str) -> Tuple[float, float]:
        lines = layer.split("\n")
        for line in lines:
            if self.getValue(line, "X") is not None and self.getValue(line, "Y") is not None:
                x = self.getValue(line, "X")
                y = self.getValue(line, "Y")
                return x, y
        return 0, 0

    def playShortMelody(self):
        prepend_gcode  = self.putValue(M = 300, S = 1318, P = 240) + "\n"
        prepend_gcode += self.putValue(M = 300, S = 0, P = 120) + "\n"
        prepend_gcode += self.putValue(M = 300, S = 1396, P = 120) + "\n"
        prepend_gcode += self.putValue(M = 300, S = 1567, P = 120) + "\n"
        prepend_gcode += self.putValue(M = 300, S = 0, P = 120) + "\n"
        prepend_gcode += self.putValue(M = 300, S = 2093, P = 720) + "\n"
        prepend_gcode += self.putValue(M = 300, S = 0, P = 180) + "\n"
        return prepend_gcode

    def playExtendedMelody(self):
        prepend_gcode  = "; Play a longer melody so it is easier to hear your printer\n"
        prepend_gcode += "; https://www.thingiverse.com/thing:446853\n"
        prepend_gcode += "; https://www.youtube.com/watch?v=qjwbaRhCCWA\n"
        prepend_gcode += "; You_Could_Be_Mine.g\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += "M117 You Could Be Mine\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 0, P = 200) + " ; \n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 330, P = 200) + " ; E4: 330\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 0, P = 200) + " ; \n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 0, P = 200) + " ; \n"
        prepend_gcode += self.putValue(M = 300, S = 524, P = 200) + " ; C5: 524\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 524, P = 200) + " ; C5: 524\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 524, P = 200) + " ; C5: 524\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 0, P = 200) + " ; \n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 330, P = 200) + " ; E4: 330\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 0, P = 200) + " ; \n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 0, P = 200) + " ; \n"
        prepend_gcode += self.putValue(M = 300, S = 524, P = 200) + " ; C5: 524\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 524, P = 200) + " ; C5: 524\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 524, P = 200) + " ; C5: 524\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 800) + " ; A4: 440\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += "M117 Finish!!\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += "; Sweet_Child_o_Mine.g\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += "M117 Sweet Child O Mine\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 294, P = 200) + " ; D4: 294\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 784, P = 200) + " ; G5: 784\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 740, P = 200) + " ; F#5: 740\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 294, P = 200) + " ; D4: 294\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 784, P = 200) + " ; G5: 784\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 740, P = 200) + " ; F#5: 740\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 330, P = 200) + " ; E4: 330\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 784, P = 200) + " ; G5: 784\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 740, P = 200) + " ; F#5: 740\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 330, P = 200) + " ; E4: 330\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 784, P = 200) + " ; G5: 784\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 740, P = 200) + " ; F#5: 740\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 784, P = 200) + " ; G5: 784\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 740, P = 200) + " ; F#5: 740\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 588, P = 200) + " ; D5: 588\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 392, P = 200) + " ; G4: 392\n"
        prepend_gcode += self.putValue(M = 300, S = 784, P = 200) + " ; G5: 784\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += self.putValue(M = 300, S = 740, P = 200) + " ; F#5: 740\n"
        prepend_gcode += self.putValue(M = 300, S = 440, P = 200) + " ; A4: 440\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += self.putValue(M = 300, S = 294, P = 800) + " ; D4: 294\n"
        prepend_gcode += "; ------------------------\n"
        prepend_gcode += "M117 Finish!!\n"
        prepend_gcode += "; ------------------------\n"
        return prepend_gcode


    ##  Inserts the pause commands.
    #   \param data: List of layers.
    #   \return New list of layers.
    def execute(self, data: List[str]) -> List[str]:
        pause_at = self.getSettingValueByKey("pause_at")
        wait_on_pause_click = self.getSettingValueByKey("wait_on_pause_click")
        pause_height = self.getSettingValueByKey("pause_height")
        pause_layer = self.getSettingValueByKey("pause_layer")
        retraction_amount = self.getSettingValueByKey("retraction_amount")
        retraction_speed = self.getSettingValueByKey("retraction_speed")
        extrude_amount = self.getSettingValueByKey("extrude_amount")
        extrude_speed = self.getSettingValueByKey("extrude_speed")
        park_x = self.getSettingValueByKey("head_park_x")
        park_y = self.getSettingValueByKey("head_park_y")
        layers_started = False
        redo_layers = self.getSettingValueByKey("redo_layers")
        standby_temperature = self.getSettingValueByKey("standby_temperature")
        firmware_retract = Application.getInstance().getGlobalContainerStack().getProperty("machine_firmware_retract", "value")
        control_temperatures = Application.getInstance().getGlobalContainerStack().getProperty("machine_nozzle_temp_enabled", "value")
        initial_layer_height = Application.getInstance().getGlobalContainerStack().getProperty("layer_height_0", "value")
        display_text = self.getSettingValueByKey("display_text")
        play_extended_melody = self.getSettingValueByKey("play_extended_melody") == "Y"

        is_griffin = False

        # T = ExtruderManager.getInstance().getActiveExtruderStack().getProperty("material_print_temperature", "value")

        # use offset to calculate the current height: <current_height> = <current_z> - <layer_0_z>
        layer_0_z = 0
        current_z = 0
        current_height = 0
        current_layer = 0
        current_extrusion_f = 0
        got_first_g_cmd_on_layer_0 = False
        current_t = 0 #Tracks the current extruder for tracking the target temperature.
        target_temperature = {} #Tracks the current target temperature for each extruder.

        nbr_negative_layers = 0

        for index, layer in enumerate(data):
            lines = layer.split("\n")

            # Scroll each line of instruction for each layer in the G-code
            for line in lines:
                if ";FLAVOR:Griffin" in line:
                    is_griffin = True
                # Fist positive layer reached
                if ";LAYER:0" in line:
                    layers_started = True
                # Count nbr of negative layers (raft)
                elif ";LAYER:-" in line:
                    nbr_negative_layers += 1

                #Track the latest printing temperature in order to resume at the correct temperature.
                if line.startswith("T"):
                    current_t = self.getValue(line, "T")

                m = self.getValue(line, "M")
                if m is not None and (m == 104 or m == 109) and self.getValue(line, "S") is not None:
                    extruder = current_t
                    if self.getValue(line, "T") is not None:
                        extruder = self.getValue(line, "T")
                    target_temperature[extruder] = self.getValue(line, "S")

                if not layers_started:
                    continue

                # Look for the feed rate of an extrusion instruction
                if self.getValue(line, "F") is not None and self.getValue(line, "E") is not None:
                    current_extrusion_f = self.getValue(line, "F")

                # If a Z instruction is in the line, read the current Z
                if self.getValue(line, "Z") is not None:
                    current_z = self.getValue(line, "Z")

                if pause_at == "height":
                    # Ignore if the line is not G1 or G0
                    if self.getValue(line, "G") != 1 and self.getValue(line, "G") != 0:
                        continue

                    # This block is executed once, the first time there is a G
                    # command, to get the z offset (z for first positive layer)
                    if not got_first_g_cmd_on_layer_0:
                        layer_0_z = current_z - initial_layer_height
                        got_first_g_cmd_on_layer_0 = True

                    current_height = current_z - layer_0_z
                    if current_height < pause_height:
                        break  # Try the next layer.

                # Pause at layer
                else:
                    if not line.startswith(";LAYER:"):
                        continue
                    current_layer = line[len(";LAYER:"):]
                    try:
                        current_layer = int(current_layer)

                    # Couldn't cast to int. Something is wrong with this
                    # g-code data
                    except ValueError:
                        continue
                    if current_layer < pause_layer - nbr_negative_layers:
                        continue

                # Get X and Y from the next layer (better position for
                # the nozzle)
                next_layer = data[index + 1]
                x, y = self.getNextXY(next_layer)

                prev_layer = data[index - 1]
                prev_lines = prev_layer.split("\n")
                current_e = 0.

                # Access last layer, browse it backwards to find
                # last extruder absolute position
                for prevLine in reversed(prev_lines):
                    current_e = self.getValue(prevLine, "E", -1)
                    if current_e >= 0:
                        break

                # include a number of previous layers
                for i in range(1, redo_layers + 1):
                    prev_layer = data[index - i]
                    layer = prev_layer + layer

                    # Get extruder's absolute position at the
                    # beginning of the first layer redone
                    # see https://github.com/nallath/PostProcessingPlugin/issues/55
                    if i == redo_layers:
                        # Get X and Y from the next layer (better position for
                        # the nozzle)
                        x, y = self.getNextXY(layer)
                        prev_lines = prev_layer.split("\n")
                        for lin in prev_lines:
                            new_e = self.getValue(lin, "E", current_e)
                            if new_e != current_e:
                                current_e = new_e
                                break

                prepend_gcode = ";TYPE:CUSTOM\n"
                prepend_gcode += ";added code by post processing\n"
                prepend_gcode += ";script: PauseAtHeightOptions.py\n"
                if pause_at == "height":
                    prepend_gcode += ";current z: {z}\n".format(z = current_z)
                    prepend_gcode += ";current height: {height}\n".format(height = current_height)
                else:
                    prepend_gcode += ";current layer: {layer}\n".format(layer = current_layer)

                if not is_griffin:
                    # Retraction
                    prepend_gcode += self.putValue(M = 83) + " ; switch to relative E values for any needed retraction\n"
                    if retraction_amount != 0:
                        if firmware_retract: #Can't set the distance directly to what the user wants. We have to choose ourselves.
                            retraction_count = 1 if control_temperatures else 3 #Retract more if we don't control the temperature.
                            for i in range(retraction_count):
                                prepend_gcode += self.putValue(G = 10) + "\n"
                        else:
                            prepend_gcode += self.putValue(G = 1, E = -retraction_amount, F = retraction_speed * 60) + "\n"

                    # Move the head up
                    prepend_gcode += self.putValue(G = 0, Z = current_z + 1, F = 300) + " ; move up a millimeter above current z (" + str(current_z) + ") to get the nozzle off of the print\n"

                    prepend_gcode += self.putValue(G = 0, X = park_x, Y = park_y, F = 9000) + " ; park nozzle at a safe place so we can purge new filament\n"

                    if current_z < 15:
                        prepend_gcode += self.putValue(G = 0, Z = 15, F = 300) + " ; too close to bed--move to at least 15mm\n"

                    if control_temperatures:
                        # Set extruder standby temperature
                        prepend_gcode += self.putValue(M = 104, S = standby_temperature) + " ; standby temperature\n"

                if display_text:
                    prepend_gcode += "M117 " + display_text + "\n"

                # Set relative position ON
                prepend_gcode += self.putValue(G = 91) + " ; switch to relative movement \n"

                # Z axis 15mm up
                prepend_gcode += self.putValue(G = 0, Z = 15.0) + " ; lift the head 15mm above whereever it was to make it easier to clean up extruded filament.\n"

                # Set relative position OFF
                prepend_gcode += self.putValue(G = 90) + " ; switch back to absolute movement \n"

                # Melody
                if play_extended_melody:
                    prepend_gcode += self.playExtendedMelody()
                else:
                    prepend_gcode += self.playShortMelody()

                # Wating for specified seconds, during this time you must click Pause on-screen,
                # otherwise the program will automatically resume printing.
                prepend_gcode += self.putValue(G = 4, S = wait_on_pause_click) + "\n"

                # Now you can change the filament or what-have-you.
                # To continue printing, click your Continue/resume button on-screen.
                prepend_gcode += self.playShortMelody()

                if not is_griffin:
                    if control_temperatures:
                        # Set extruder resume temperature
                        prepend_gcode += self.putValue(M = 109, S = int(target_temperature.get(current_t, 0))) + " ; resume temperature\n"

                    # Push the filament back
                    if retraction_amount != 0:
                        prepend_gcode += self.putValue(G = 1, E = retraction_amount, F = retraction_speed * 60) + " ; I think this is a bug? It pushes out filament, not retracts. Seems like we could use the retraction BEFORE the pause though, right?\n"

                    # Optionally extrude material
                    if extrude_amount != 0:
                        prepend_gcode += self.putValue(G = 1, E = extrude_amount, F = extrude_speed * 60) + " ; extrude the new filament \n"

                    # and retract again, the properly primes the nozzle
                    # when changing filament.
                    if retraction_amount != 0:
                        prepend_gcode += self.putValue(G = 1, E = -retraction_amount, F = retraction_speed * 60) + " ; retract again, this helps prevent spooging while in transit back to the print\n"

                    # Move the head back
                    if current_z < 15:
                        prepend_gcode += self.putValue(G = 0, Z = current_z + 1, F = 300) + " ; Move Z near print before moving X,Y\n"

                    prepend_gcode += self.putValue(G = 0, X = x, Y = y, F = 9000) + " ; return to the original X,Y\n"
                    prepend_gcode += self.putValue(G = 0, Z = current_z, F = 300) + " ; vertical move back down to original position\n"

                    if retraction_amount != 0:
                        if firmware_retract: #Can't set the distance directly to what the user wants. We have to choose ourselves.
                            retraction_count = 1 if control_temperatures else 3 #Retract more if we don't control the temperature.
                            for i in range(retraction_count):
                                prepend_gcode += self.putValue(G = 11) + "\n"
                        else:
                            prepend_gcode += self.putValue(G = 1, E = retraction_amount, F = retraction_speed * 60) + "\n"

                    if current_extrusion_f != 0:
                        prepend_gcode += self.putValue(G = 1, F = current_extrusion_f) + " ; restore extrusion feedrate\n"
                    else:
                        Logger.log("w", "No previous feedrate found in gcode, feedrate for next layer(s) might be incorrect")

                    prepend_gcode += self.putValue(M = 82) + " ; switch back to absolute E values\n"
                    prepend_gcode += self.putValue(G = 92, E = current_e) + " ; reset extrusion value to pre-pause value\n"

                layer = prepend_gcode + layer

                # Override the data of this layer with the
                # modified data
                data[index] = layer
                return data
        return data
