import matplotlib.pyplot as plt
import numpy as np
from exportDataFromFile import (FIRSTCOLUMN, SECONDCOLUMN, listFiles, ExportDataFromFiles, ExportValueR)

def Draw():
    """
    функция построения графиков по одному в окне
    :return: пусто
    """
    if listFiles:
        halfCountList = int(len(listFiles)/2)
        # создание двумерного списка со значениями R и psi_max
        listMaximum = [[], []]
        # шаг для получения списка с данными первого и второго файлов
        step = 2
        for fileNumber in range(halfCountList):
            resL = ExportDataFromFiles(fileNumber)
            if resL:
                resultList = resL
            else:
                try:
                    raise Exception("Функция ExportDataFromFiles вернула пустой список!")
                except Exception as e:
                    print(f"Exception: {e}")
                    return

            r = int(ExportValueR(fileNumber))
            listMaximum[0].append(r)
            # нахождение максимального значения psi, взятого по второй половине данных из файла psi2_
            # и добавление к списку
            listMaximum[1].append(max(resultList[SECONDCOLUMN+step][int(len(resultList[SECONDCOLUMN+step])/2):]))
            # сортировка по возрастанию значений из первого столбца файлов
            xAxis1 = resultList[FIRSTCOLUMN]
            xAxisArg1 = np.argsort(np.array(xAxis1))
            xAxis1.sort()
            yAxis1 = np.array(resultList[SECONDCOLUMN])[xAxisArg1]
            xAxis2 = resultList[FIRSTCOLUMN+step]
            xAxisArg2 = np.argsort(np.array(xAxis2))
            xAxis2.sort()
            yAxis2 = np.array(resultList[SECONDCOLUMN+step])[xAxisArg2]
            # построение двух графиков в одном окне
            x1 = xAxis1
            y1 = yAxis1
            x2 = xAxis2
            y2 = yAxis2
            plt.grid()
            plt.xlabel(r"$t$", fontsize=14)
            plt.ylabel(r"$\mathcal{Ψ}$", fontsize=16)
            plt.title(f'R = {r}')
            plt.plot(x1, y1, "b-", label=r"$Psi_{loc}$")
            plt.plot(x2, y2, "k--", label=r"$\mathcal{Ψ}_{max}$")
            plt.legend(loc='upper left', fontsize=13, frameon=True)
            plt.subplots_adjust(left=0.15, right=0.97, top=0.92, bottom=0.1)
            plt.show()

        # построение графика, отображающего зависимости максимального значения psi,
        # взятого по второй половине данных из файла psi2_ , от R
        x = listMaximum[0]
        y = listMaximum[1]
        plt.grid()
        plt.xlabel(r"$R$", fontsize=14)
        plt.ylabel(r"$\mathcal{Ψ}$", fontsize=16)
        plt.plot(x, y, "bo-", label=r"$\mathcal{Ψ}_{max}$")
        plt.legend(loc='upper right', fontsize=13, frameon=True)
        plt.subplots_adjust(left=0.125, right=0.97, top=0.95, bottom=0.1)
        plt.show()
    else:
        print("Список с файлами в указанной директории оказался пуст!")
        return


def DrawOnePlot():
    """
    функция построения всех графиков в одном окне
    :return:
    """
    if listFiles:
        halfCountList = int(len(listFiles)/2)
        # создание двумерного списка со значениями R и psi_max
        listMaximum = [[], []]
        # шаг для получения списка с данными первого и второго файлов
        step = 2
        for fileNumber in range(halfCountList):
            resL = ExportDataFromFiles(fileNumber)
            if resL:
                resultList = resL
            else:
                try:
                    raise Exception("Функция ExportDataFromFiles вернула пустой список!")
                except Exception as e:
                    print(f"Exception: {e}")
                    return

            r = int(ExportValueR(fileNumber))
            listMaximum[0].append(r)
            # нахождение максимального значения psi, взятого по второй половине данных из файла psi2_
            # и добавление к списку
            listMaximum[1].append(max(resultList[SECONDCOLUMN+step][int(len(resultList[SECONDCOLUMN+step])/2):]))
            # сортировка по возрастанию значений из первого столбца файлов
            xAxis1 = resultList[FIRSTCOLUMN]
            xAxisArg1 = np.argsort(np.array(xAxis1))
            xAxis1.sort()
            yAxis1 = np.array(resultList[SECONDCOLUMN])[xAxisArg1]
            xAxis2 = resultList[FIRSTCOLUMN+step]
            xAxisArg2 = np.argsort(np.array(xAxis2))
            xAxis2.sort()
            yAxis2 = np.array(resultList[SECONDCOLUMN+step])[xAxisArg2]
            # построение двух графиков в одном окне
            x1 = xAxis1
            y1 = yAxis1
            x2 = xAxis2
            y2 = yAxis2
            plt.grid()
            plt.xlabel(r"$t$", fontsize=14)
            plt.ylabel(r"$\mathcal{Ψ}$", fontsize=16)
            plt.title(f'R = {r}')
            plt.plot(x1, y1, "b-", label=r"$Psi_{loc}$")
            plt.plot(x2, y2, "k--", label=r"$\mathcal{Ψ}_{max}$")
            plt.legend(loc='upper left', fontsize=13, frameon=True)

        # построение графика, отображающего зависимости максимального значения psi,
        # взятого по второй половине данных из файла psi2_ , от R
        x = listMaximum[0]
        y = listMaximum[1]
        plt.subplot(3, 3, halfCountList + 1)
        plt.grid()
        plt.xlabel(r"$R$", fontsize=14)
        plt.ylabel(r"$\mathcal{Ψ}$", fontsize=16)
        plt.plot(x, y, "bo-", label=r"$\mathcal{Ψ}_{max}$")
        plt.legend(loc='upper right', frameon=True)
        plt.subplots_adjust(left=0.15, right=0.97, top=0.92, bottom=0.1)
        plt.show()

    else:
        print("Список с файлами в указанной директории оказался пуст!")
        return

