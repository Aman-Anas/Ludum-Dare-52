import bge.logic
from ast import literal_eval
from textwrap import wrap

COLORS = {
    "WHITE": (1, 1, 1, 1),
    "RED": (1, 0, 0, 1),
    "GREEN": (0, 1, 0, 1),
    "BLUE": (0, 0, 1, 1),
    "YELLOW": (1, 1, 0, 1),
    "PURPLE": (1, 0, 1, 1),
    "CYAN": (0, 1, 1, 1),
    "BLACK": (0, 0, 0, 1)
}


# Rough correction for the way BGE stretches text
# between viewport and the game
# let me know if there's a better way
SCALEFACTOR = 5.8/7.0


def LD(cont):
    own = cont.owner
    player = bge.logic.getSceneList()["Scene"].objects["Player"]
    own["textFromScript"] = "x" + str(player["fruits"])


def main(cont):
    own = cont.owner

    if not "initialSet" in own:
        own["initialSet"] = False

    # Name your always sensor UpdateText!
    always = cont.sensors["UpdateText"]

    if "Run" in own:
        targetText = str(own["Run"])

        # Tries to eval reference from string
        try:
            own["Text"] = str(eval(targetText))

        # Set text to error if cannot eval string
        except:
            own["Text"] = "Error! Text failed to evaluate"
            print(own["Text"])

    # Initial setup, runs once
    if (own["initialSet"] == False):

        if "Update" in own:
            if (own["Update"] > 0):
                always.usePosPulseMode = True
                always.skippedTicks = int(
                    bge.logic.getLogicTicRate()/int(own["Update"]) - 1)

            else:
                always.usePosPulseMode = False
                always.skippedTicks = 0
        else:
            always.usePosPulseMode = False
            always.skippedTicks = 0

        # Reset the reveal at the beginning unless specified
        if "Reveal" in own:
            own["OriginalText"] = own["Text"]
            if not "ResetReveal" in own:
                own["ResetReveal"] = True

        if (not "Wrap" in own) and ("reveal" in own):
            own["Wrap"] = 99999
            own["Align"] = "left"

        if "Wrap" in own:
            own["unWrapped"] = own["Text"]

        # Fix scaling by default
        own.localScale *= SCALEFACTOR
        own["initialScale"] = own.localScale.copy()

        # Set color to white by default
        if not "Color" in own:
            own.color = evalColor("WHITE")

        if not "Resolution" in own:
            own.resolution = 1.0

        if not "Align" in own:
            own["Align"] = "left"

        own["initialSet"] = True

    # Revealing
    if "Reveal" in own:
        if (own["ResetReveal"]):
            own["toReveal"] = own["OriginalText"]
            if not "Wrap" in own:
                own["Text"] = ""
            else:
                own["unWrapped"] = ""
            own["ResetReveal"] = False

        if (len(own["toReveal"]) > 0):
            if not "Wrap" in own:
                own["Text"] += own["toReveal"][0]
            else:
                own["unWrapped"] += own["toReveal"][0]
            own["toReveal"] = own["toReveal"][1:]

    # Scaling
    if "Scale" in own:
        own.localScale.x = own["initialScale"].x * own["Scale"]
        own.localScale.y = own["initialScale"].y * own["Scale"]
        own.localScale.z = own["initialScale"].z * own["Scale"]

    # Color
    if "Color" in own:
        own.color = evalColor(own["Color"])

    # Resolution
    if "Resolution" in own:
        own.resolution = own["Resolution"]

    #Wrap and align
    if "Wrap" in own:
        paragraphs = own["unWrapped"].split("\n\n")

        own["Text"] = ""

        for txt in paragraphs:

            a = wrap(txt, int(own["Wrap"]))

            aligned = ""

            # Align text

            for line in a:
                if (own["Align"].lower() == "center"):
                    line = line.center(int(own["Wrap"]))

                elif (own["Align"].lower() == "right"):
                    line = line.rjust(int(own["Wrap"]))

                aligned += line + "\n"

            own["Text"] += aligned + "\n"


# Completely taken from BGText
def evalColor(txtColor):
    try:
        # Try to get a literal color if string starts with [ or (
        if txtColor.startswith('[') or txtColor.startswith('('):

            # Tries to eval given literal RGBA
            txtColor = literal_eval(txtColor)

            # Ensures valid RGBA after eval
            if len(txtColor) != 4:
                raise Exception

        # Get color from colors table if exists
        elif txtColor.upper() in COLORS.keys():
            txtColor = COLORS[txtColor.upper()]

        # Defaults to white otherwise
        else:
            raise Exception

    # Defaults to white if could not eval color
    except:
        txtColor = COLORS["WHITE"]

    return txtColor
