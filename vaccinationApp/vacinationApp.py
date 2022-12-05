from crud import Crud
from configparser import ConfigParser
import fieldsValidation as isValid
import json

ColumnNames = ('nombre','apellido','correo','nacimiento','telefono','domicilio','numvacunas')
ColumVax = ('cedula','vacuna','fecha')
primaryKey = "cedula"

def config(filename, section):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

class Company():
    def __init__(self, params):
        # read connection parameters and connect
        self.db = Crud(**params)
        
    def createEmployee(self, name, lastname, id, email, num):
        self.db.insert(nombre=name, apellido=lastname, cedula=id, correo=email, numvacunas=num)

    def deleteEmployee(self, primaryKey_value):
        self.db.delete(primaryKey_value)

    def updateEmployee(self, column, colum_value, primaryKey_value):
        self.db.update(column, colum_value, primaryKey_value)

    def updateVaxCount(self, primaryKey_value):
        self.db.update_count("numvacunas", primaryKey_value)
        
    def addVaccine(self, auxcedula, auxvacuna, auxfecha):
        self.db.insert(cedula=auxcedula, vacuna=auxvacuna, fecha=auxfecha)

    def selectData(self, colname, id):
        query = self.db.select(columns = [colname], primaryKey_value = id)
        if query == []:
            return 0
        
        return {colname: query[0][0]}
        
    def selectAllData(self, auxid):
        return self.db.select_all(primaryKey_value = auxid)

    def queryFilterData(self, columFilter):
        query = self.db.filterData(columFilter)
        if query == []:
            return 0
        
        return query

    def isAllDataValid(self, name, lastname, id, email):
        if isValid.name(name) and \
           isValid.name(lastname) and \
           isValid.id(id) and \
           isValid.mail(email):
            return True
        return False

    def isDataValid(self, colum, val):
        ret = False

        if colum == "cedula":
            ret = isValid.id(val)
        elif colum == "nombre" or \
             colum == "apellido":
            ret = isValid.name(val)
        elif colum == "correo":
            ret = isValid.mail(val)
        elif colum == "nacimiento" or \
             colum == "fecha":
            ret = isValid.date(val)
        elif colum == "telefono":
            ret = isValid.phone(val)
        elif colum == "vacuna":
            ret = isValid.vax(val)
        elif colum == "domicilio":
            ret = True;
            
        return ret
