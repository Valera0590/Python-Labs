import os, sys
import sqlite3 as sql
sys.path.insert(0, "Lab_5")
from exportBibl import ExportDataFromBiblio, FindParam, NameRows, ValueRows, PARAMTOSEPARATORDICTIONARY

# ------- Глобальные переменные --------- #
NAMEDB = 'sqlite_science_articles.db'
# --------------------------------------- #

def ObjectBiblToListParameters(elementBibl):
    result = {}
    listNameRows = NameRows(elementBibl)
    listValueRows = ValueRows(elementBibl)
    i = 0
    for rowName in listNameRows:
        if (rowName != "Author"):
            result[rowName] = listValueRows[i]
        else:
            result[rowName] = listValueRows[i].replace(","," ").replace(" and"," ;")
        i+=1
    return result

def CreateTable(name, fields):
    try:
        with sql.connect(NAMEDB) as db:
            cursor = db.cursor()
            sqlite_create_table_query = 'CREATE TABLE IF NOT EXISTS [{}] ({})'.format(name, ','.join(fields))
            cursor.execute(sqlite_create_table_query)
    except sql.Error as error:
        print("Ошибка при подключении к sqlite:", error)
    finally:
        if (db):
            db.close()
            # print("Соединение с SQLite закрыто")

def PrepareArticleForFillTables(bibl, idArticle):
    dictParams = ObjectBiblToListParameters(bibl)
    listAuthorsName = FindParam(dictParams, 'Author').split(";")
    authors = []
    for author in listAuthorsName:
        authors.append((author.strip(), idArticle))
    journal = FindParam(dictParams, 'Journal').strip()
    listArticle = []
    # listArticle.append(str(idArticle))
    year = ""
    for param in PARAMTOSEPARATORDICTIONARY["english"].keys():
        paramArticle = FindParam(dictParams, param)
        if (param == 'Author'):
            listArticle.append(paramArticle.replace(";","and").strip() if paramArticle != "" else "-")
        elif (param == 'Year'):
            listArticle.append(paramArticle.replace("Пермь. —", "").replace("Пермь.—", "").strip() if paramArticle != "" else "-")
            year = paramArticle.replace("Пермь. —", "").replace("Пермь.—", "")
        else:
            listArticle.append(paramArticle.strip() if paramArticle != "" else "-")
    article = tuple(listArticle)
    return authors, journal, year, article

def FillTables():
    listBiblioObjects = ExportDataFromBiblio()
    idArticle = 1
    for bibl in listBiblioObjects:
        # print(bibl)
        authors, journal, year, article = PrepareArticleForFillTables(bibl, idArticle)
        if (authors != [] and journal != "" and year != ""):
            try:
                with sql.connect(NAMEDB) as db:
                    cursor = db.cursor()
                    sqlite_insert_table_query = 'INSERT OR IGNORE INTO Authors(name, article_id) VALUES (?,?);'
                    cursor.executemany(sqlite_insert_table_query, authors)
                    sqlite_insert_table_query = 'INSERT OR IGNORE INTO Journals(name, article_id) VALUES (?,?);'
                    cursor.execute(sqlite_insert_table_query, (journal, idArticle))
                    sqlite_insert_table_query = '''INSERT OR IGNORE INTO Articles(author, title, booktitle, type, 
                                                    journal, number, address, publisher, school, year, volume, pages, 
                                                    numpages, nite) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
                    cursor.execute(sqlite_insert_table_query, article)
                    idArticle += 1
                    db.commit()
            except sql.Error as error:
                print("Ошибка sqlite:", error)
            finally:
                if (db):
                    db.close()

def SelectArticles(requiredAuthor, requiredYear, requiredJournal):
    try:
        with sql.connect(NAMEDB) as db:
            cursor = db.cursor()
            sqlite_select_table_query = '''SELECT id, author, title, booktitle, journal, year
                                            FROM Articles 
                                            JOIN Authors ON Authors.article_id = Articles.id
                                            JOIN Journals ON Journals.article_id = Articles.id
                                            AND Journals.article_id = Authors.article_id
                                            WHERE Authors.name = ?
                                            AND Journals.name = ?
                                            AND Articles.year = ?
                                            GROUP BY Articles.id;'''
            cursor.execute(sqlite_select_table_query, (requiredAuthor, requiredJournal, requiredYear,))
            for selected in cursor:
                print(selected)
    except sql.Error as error:
        print("Ошибка sqlite:", error)
    finally:
        if (db):
            db.close()


if (not os.path.isfile(NAMEDB)):
    CreateTable('Authors', ['[name] NVARCHAR(128) NOT NULL', '[article_id] INTEGER NOT NULL'])
    CreateTable('Journals', ['[name] NVARCHAR(128) NOT NULL', '[article_id] INTEGER NOT NULL'])
    CreateTable('Articles', ['[id] INTEGER PRIMARY KEY AUTOINCREMENT',
                            '[author] NVARCHAR(128) NOT NULL', '[title] NVARCHAR(128) NOT NULL',
                            '[booktitle] NVARCHAR(128) NOT NULL', '[type] NVARCHAR(128) NOT NULL',
                            '[journal] NVARCHAR(128) NOT NULL', '[number] NVARCHAR(128) NOT NULL',
                            '[address] NVARCHAR(128) NOT NULL', '[publisher] NVARCHAR(128) NOT NULL',
                            '[school] NVARCHAR(128) NOT NULL', '[year] NVARCHAR(128) NOT NULL',
                            '[volume] NVARCHAR(128) NOT NULL', '[pages] NVARCHAR(128) NOT NULL',
                            '[numpages] NVARCHAR(128) NOT NULL', '[nite] NVARCHAR(128) NOT NULL'])
    FillTables()
    print("Запрос к БД:")
    # SelectArticles("Черепанов  И. Н.", "2013", "XVIII Зимняя школа по механике сплошных сред, Пермь, 18-22 февраля 2013 г. Тезисы докладов. Пермь-Екатеринбург")
    SelectArticles("Ryskin  A.", "2003", "Magnitnaya Gidrodinamika")
else:
    print("Запрос к БД:")
    # SelectArticles("Черепанов  И. Н.", "2013", "XVIII Зимняя школа по механике сплошных сред, Пермь, 18-22 февраля 2013 г. Тезисы докладов. Пермь-Екатеринбург")
    SelectArticles("Ryskin  A.", "2003", "Magnitnaya Gidrodinamika")





