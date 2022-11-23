import glob, os, re

# ------- глобальные переменные ----- #
# каталог текстовых файлов
PATH = 'Lab_5\\data'
# паттерн поиска файлов по расширению
PATTERN = '*.bib'
globPath = os.path.join(PATH, PATTERN)
listFiles = glob.glob(globPath)
# ----- словарь разаделителей ------- #
PARAMTOSEPARATORDICTIONARY = {
    "russian": {
        "Author": " ",
        "Title": " . ",
        "Booktitle": " . ",
        "Type": " : ",
        "Journal": " // ",
        "Number": " : ",
        "Address": " .- ",
        "Publisher": " : ",
        "School": " : ",
        "Year": " .- ",
        "Volume": " .-Вып. ",
        "Pages": " .-С. ",
        "Numpages": " .- ",
        "Nite": " .- "
        # "File": " .- "
        },
    "english": {
        "Author": " ",
        "Title": " . ",
        "Booktitle": " . ",
        "Type": " : ",
        "Journal": " // ",
        "Number": " : ",
        "Address": " .- ",
        "Publisher": " : ",
        "School": " : ",
        "Year": " .- ",
        "Volume": " .-Vol. ",
        "Pages": " .-P. ",
        "Numpages": " .- ",
        "Nite": " .- "
        # "File": " .- "
    }
}
# ----------------------------------- #

def ToString(file):
    result = ""
    with open(file, 'r', encoding='utf-8') as fileReader:
        result = fileReader.read()
    return result

def NameRows(elementBibl):
    result = []
    listNameRows = re.findall(r'[a-zA-Z]+ {3,}', elementBibl)
    for el in listNameRows:
        result.append(el.strip())
    return result

def ValueRows(elementBibl):
    result = []
    listValueRows = re.findall(r'{[a-zA-Zа-яА-Я0-9 üöäё\._\+\-\─\–\—()\\\|\/?!#№«»\$\^;:\'\"`,\{\}\[\]\n\•]*}', elementBibl)
    for el in listValueRows:
        result.append(el.replace("{","").replace("}","").replace("\n"," ").strip())
    return result

def FindParamWithSeparator(dictParams, strParam, paramSeparator):
    try:
        return paramSeparator + dictParams[strParam]
    except:
        return ""

def FindParam(dictParams, strParam):
    try:
        return dictParams[strParam]
    except:
        return ""

def ObjectBiblToListParameters(elementBibl):
    result = {}
    listNameRows = NameRows(elementBibl)
    listValueRows = ValueRows(elementBibl)
    i = 0
    for rowName in listNameRows:
        if (rowName != "Author"):
            result[rowName] = listValueRows[i]
        else:
            result[rowName] = listValueRows[i].replace(" and"," ,").replace(",and",",")
        i+=1
    return result

def FormattingOutputObjectBibl(dictParams):
    resultString = ""
    language = ""
    try:
        language = dictParams["Language"]
    except:
        language = "english"

    for param in PARAMTOSEPARATORDICTIONARY[language].items():
        resultString += FindParamWithSeparator(dictParams, param[0], param[1])
        
    print(resultString)
    print()

def ExportDataFromBiblio():
    listBiblioObjects = re.findall(r'@[a-zA-Z0-9а-яА-Я üöäё\._+=\-\─\–\—()\\\|\/?!#№«»\$\^;:\'\"`,\{\}\[\]\n\•]*', ToString(listFiles[0]))
    return listBiblioObjects