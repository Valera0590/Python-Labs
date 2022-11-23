
from avitoParser import ParseDiffFullAndShortDescriptionToFile, ParsePriceAndDescriptionToFile
from fileOperations import RemoveExistingFile

# global variables
DIRFILEDESCRIPTIONADS = "Lab_7\\data\\bt_speakers_jbl_avito.txt"  #bt_speakers_hopestar_avito.txt" #
REGION = "permskiy_kray"
CATEGORY = "audio_i_video/akustika_kolonki_sabvufery"
CATCHINGOBJECT = "jbl+charge+5"  #"hopestar" #

# main
if __name__ == "__main__":
    RemoveExistingFile(DIRFILEDESCRIPTIONADS)
    ParsePriceAndDescriptionToFile(REGION, CATEGORY, CATCHINGOBJECT, DIRFILEDESCRIPTIONADS)
    # ParseDiffFullAndShortDescriptionToFile(REGION, CATEGORY, CATCHINGOBJECT, DIRFILEDESCRIPTIONADS)

