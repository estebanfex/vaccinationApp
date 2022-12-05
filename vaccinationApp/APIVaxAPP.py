from configparser import ConfigParser
from flask import Flask, request, render_template
from jsonmerge import merge
import json

import vacinationApp as vaxDB

app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


@app.get('/user')
def get_userdata():
    args = request.args
    cedula = args.get(vaxDB.primaryKey)
    jdata = {vaxDB.primaryKey:cedula}
    table = vaxDB.Company( vaxDB.config('DataBase.ini', 'employesql') )
    if cedula is None or not table.isDataValid(vaxDB.primaryKey, cedula):
        return  {"Error": "Invalid data supplied"}, 400
        
    table.db.connect()
    isFound = False
    for column in vaxDB.ColumnNames:
        data = args.get(column)
        if data is not None:
            dbData = table.selectData(column,cedula)
            if not dbData:
                table.db.close()
                return  {"Error": "Data not found"}, 404

            jdata   = merge(jdata, dbData)
            isFound = True
    table.db.close()
    if not isFound:
        return  {"Error": "Data not found"}, 404
        
    return jdata, 200

@app.post("/newuser")
def add_user():
    if not request.is_json:
        return {"Error": "Request must be JSON"}, 415

    user = request.get_json()
    table = vaxDB.Company( vaxDB.config('DataBase.ini', 'postgresql') )
    if not table.isAllDataValid(user["nombre"], user["apellido"], user["cedula"], user["correo"]):
        return {"Error": "Invalid data supplied"}, 400
        
    table.db.connect()
    table.createEmployee(user["nombre"], user["apellido"], user["cedula"], user["correo"], 0)
    table.db.close("commit")
    return user, 200

@app.post("/vaccine")
def add_vaccine():
    if not request.is_json:
        return {"Error": "Request must be JSON"}, 415

    user = request.get_json()

    table = vaxDB.Company( vaxDB.config('DataBase.ini', 'postgresql') )

    for column in vaxDB.ColumVax:
        if column in user:
            data = user[column]
            if not table.isDataValid(column,data):
                print(column)
                return {"Error": "Invalid data supplied"}, 400
    
    table.db.connect()
    cedula = user["cedula"]
    idExist = table.selectData('cedula', cedula)
    table.db.close()
    if not idExist:
        return  {"Error": "Invalid data supplied"}, 400
    
    vaccine = user["vacuna"]
    date    = user["fecha"]
    vax = vaxDB.Company( vaxDB.config('DataBase.ini', 'postgresqlvax') )
    vax.db.connect()
    
    vax.addVaccine(cedula,vaccine, date)
    vax.db.close("commit")
    
    table.db.connect()
    table.updateVaxCount(cedula)
    table.db.close("commit")
    return user, 201

@app.put("/update")
def update_user():
    if not request.is_json:
        return {"Error": "Request must be JSON"}, 415

    user = request.get_json()
    cedula = user["cedula"]
    table = vaxDB.Company( vaxDB.config('DataBase.ini', 'postgresql') )
    if cedula is None or not table.isDataValid('cedula', cedula):
        return  {"Error": "Invalid data supplied"}, 400
  
    table.db.connect()
    for column in vaxDB.ColumnNames:
        if column in user:
            data = user[column]
            if not table.isDataValid(column,data):
                table.db.close()
                return {"Error": "Invalid data supplied"}, 400

            table.updateEmployee(column,data,cedula)
    table.db.close("commit")
    return user, 201

@app.get("/delete")
def delete_user():
    args = request.args
    cedula = args.get('cedula')

    table = vaxDB.Company( vaxDB.config('DataBase.ini', 'postgresql') )
    if cedula is None or not table.isDataValid('cedula', cedula):
        return  {"Error": "Invalid data supplied"}, 400

    table.db.connect()
    if not table.selectData('cedula',cedula):
        table.db.close()
        return  {"Error": "User not found"}, 404

    table.deleteEmployee(cedula)
    table.db.close("commit")
    
    vax = vaxDB.Company( vaxDB.config('DataBase.ini', 'postgresqlvax') )
    vax.db.connect()
    vax.deleteEmployee(cedula)
    vax.db.close("commit")
    return   {"Accept": "User deleted"}, 201


#Filters
@app.get("/getdata")
def get_vaxdata():
    args = request.args
    table = vaxDB.Company( vaxDB.config('DataBase.ini', 'postgresqlvax') )
    table.db.connect()

    for column in vaxDB.ColumVax:
        data = args.get(column)
        if data is not None:
            dbData = table.queryFilterData(column)
            print(dbData)
            if not dbData:
                break
            return json.dumps(dbData, default=str), 200
            
    table.db.close()
    return  {"Error": "Data not found"}, 404


if __name__ == '__main__':
    app.run(debug=True)