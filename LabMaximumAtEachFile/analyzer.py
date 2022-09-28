
import glob, os, re

# ------- глобальные переменные ----- #
# каталог текстовых файлов
PATH = 'files'
# паттерн поиска файлов по расширению
PATTERN = '*.dat'
globPath = os.path.join(PATH, PATTERN)
listFiles = glob.glob(globPath)
NUMBERCOLUMNTOFINDMAX = 1


# ----------- функции ---------- #

def ChangeLetterPow(str):
    '''
    функция конвертации к формату с двойной точностью python
    :param str: строка с числом формата Fortran
    :return: строка преобразованная к числу с двойной точностью формата Python
    '''
    return float(str.replace('D', 'E'))

def ErrorPrint(strError):
    '''
    функция вывода возникшей ошибки
    :param strError: строка с описанием ошибки
    :return: пусто
    '''
    print(strError)

def MaxInSecondColumnInFile(directoryToFile):
    '''
    функция поиска максимума во втором столбце файла
    :param directoryToFile: строка с директорией к файлу
    :return: максимум во втором столбце файла
    '''
    res = []
    with open(directoryToFile, 'r') as fileRead:
        data = fileRead.read()
        # разбиение файла на строки и вычленение чисел из второго столбца
        for line in data.splitlines():
            lineData = line.strip().replace('  ', ' ').split(' ')
            res.append(ChangeLetterPow(lineData[NUMBERCOLUMNTOFINDMAX]))
    fileRead.close()
    return max(res)

def WriteToFile(listMaximums, fileName):
    '''
    функция записи в файл информации о проанализированных файлах
    :param listMaximums: список кортежей (название файла, максимум во втором столбце, значение R)
    :param fileName: название файла для записи результата
    :return: пусто
    '''
    if listMaximums:
        # ---- индексы для записи в кортеж ----#
        fn, m, r = 0,1,2
        # ------------------------------------ #
        with open(fileName, 'w') as fileWrite:
            for elementList in listMaximums:
                fileWrite.write(f'\n--- {elementList[fn]}\tmax={elementList[m]}\tR={elementList[r]}\n')
    else:
        ErrorPrint("Список с максимумами пуст. Пожалуйста проверьте файлы с данными!")

def AnalyzeEachFile():
    '''
    функция анализа всех файлов в поддиректории PATH с целью поиска максимума во втором столбце каждого
    :return: пусто
    '''
    newFile = 'maximum_in_files.txt'
    resultList = []
    if listFiles:
        for fileName in listFiles:
            resultList.append((fileName, MaxInSecondColumnInFile(fileName), ChangeLetterPow(re.search(r'0.\d+D.\d+', fileName)[0])))
        WriteToFile(resultList, newFile)
    else:
        ErrorPrint("Список с файлами пуст. Пожалуйста проверьте на корректность путь, по которому вы разместили файлы с данными!")
