import os

def RemoveExistingFile(directoryToFile):
    if os.path.exists(directoryToFile):
        os.remove(directoryToFile)

def WriteToFile(dirToFile, info):
    try:
        with open(dirToFile, 'a', encoding='utf-8') as fileAppend:
            fileAppend.write(info)
    except Exception as exceptionFile:
        print(f"Writting exception: {exceptionFile}")

