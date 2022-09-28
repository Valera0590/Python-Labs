import glob, os, re

# ------- глобальные переменные ----- #
# каталог текстовых файлов
PATH = 'data'
# паттерн поиска файлов по расширению
PATTERN = '*.dat'
globPath = os.path.join(PATH, PATTERN)
listFiles = glob.glob(globPath)
FIRSTCOLUMN = 0
SECONDCOLUMN = 1

# ----------- функции ---------- #

def ChangeLetterPow(str):
    """
    функция конвертации к формату с двойной точностью python
    принимает строку str
    возвращает строку преобразованную к числу с двойной точностью
    """
    return float(str.replace('D', 'E'))

def ExportValueR(fileNumber):
    """
    функция извлечения значения R из названия файла
    :param fileNumber: номер файла в списке для извлечения значения R
    :return: значение R
    """
    return ChangeLetterPow(re.search(r'0.\d+D.\d+', listFiles[fileNumber])[0])

def DataToArray(dirFileOne, dirFileTwo):
    """
    функция извлечения двух столбцов двух файлов с одинаковым значением R
    :param dirFileOne: директория расположения первого файла
    :param dirFileTwo: директория расположения второго файла
    :return: двумерный массив, где строки: 1-первый столбец первого файла,
            2-второй столбец первого файла, 3-первый столбец второго файла,
            4-второй столбец второго файла
    """
    # создание двумерного списка для хранения первого и второго столбцов обоих файлов
    res = [[],[],[],[]]
    # шаг для получения списка с данными первого и второго файлов
    step = 2
    try:
        with open(dirFileOne, 'r') as fileReadOne:
            try:
                with open(dirFileTwo, 'r') as fileReadTwo:
                    dataOne = fileReadOne.read()
                    dataTwo = fileReadTwo.read()
                    linesFileOne = dataOne.splitlines()
                    linesFileTwo = dataTwo.splitlines()
                    for lineNumber in range(len(linesFileOne)):
                        lineDataOne = linesFileOne[lineNumber].strip().replace('  ', ' ').split(' ')
                        lineDataTwo = linesFileTwo[lineNumber].strip().replace('  ', ' ').split(' ')
                        res[FIRSTCOLUMN].append(ChangeLetterPow(lineDataOne[FIRSTCOLUMN]))
                        res[SECONDCOLUMN].append(ChangeLetterPow(lineDataOne[SECONDCOLUMN]))
                        res[FIRSTCOLUMN+step].append(ChangeLetterPow(lineDataTwo[FIRSTCOLUMN]))
                        res[SECONDCOLUMN+step].append(ChangeLetterPow(lineDataTwo[SECONDCOLUMN]))
                fileReadOne.close()
                fileReadTwo.close()
            except Exception as e2:
                print(e2)
                fileReadOne.close()
            else:
                print(f"File {dirFileTwo} was readed")
    except Exception as e1:
        print(e1)
    else:
        print(f"File {dirFileOne} was readed")
    return res

def ExportDataFromFiles(fileNumber: int):
    """
    функция экспорта данных из двух файлов с одинаковым значением R
    :param fileNumber: номер файла в общем списке
    :return: двумерный список, где строки: 1-первый столбец первого файла,
            2-второй столбец первого файла, 3-первый столбец второго файла,
            4-второй столбец второго файла;
            в случае не нахождения второго файла со значением R или
            пустого списка файлов возвращает пустой список
    """
    if listFiles:
        for fileName in listFiles:
            if fileName != listFiles[fileNumber]:
                findIndex = fileName.find(str(re.search(r'0.\d+D.\d+', listFiles[fileNumber])[0]))
                if findIndex != -1:
                    if fileName.find('psi_G'):
                        return DataToArray(fileName, listFiles[fileNumber])
                    elif fileName.find('psi2_G'):
                        return DataToArray(listFiles[fileNumber], fileName)
                    else:
                        try:
                            raise Exception("Не удалось найти подстроку psi_G or psi2_G в названии очередного файла!")
                        except Exception as e:
                            print(f"Exception: {e}")
                            return []
    return []


