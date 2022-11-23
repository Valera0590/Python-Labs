from exportBibl import ExportDataFromBiblio, ObjectBiblToListParameters, FormattingOutputObjectBibl

listBiblioObjects = ExportDataFromBiblio()
for bibl in listBiblioObjects:
    # print(bibl)
    dictParams = ObjectBiblToListParameters(bibl)
    FormattingOutputObjectBibl(dictParams)