import requests
import pytest
import fieldsValidation

valid_cedula   = "1713175071"
invalid_cedula = "171317507A"

valid_email   = "test@myemail.com"
invalid_email = "test.myemail.com"

valid_date   = "01-01-2020"
invalid_date = "45-45-1990"

valid_name   = "nombre"
invalid_name = "nom7"

valid_phone   = "0911111111"
invalid_phone = "091111111A"

valid_Vax_Name   = "Pfizer"
invalid_Vax_Name = "Sinovac"

valid_field   = valid_name
invalid_field = invalid_name



#FIELDS tests
def test_valid_id():
    assert fieldsValidation.id(valid_cedula) == True

def test_invalid_id():
    assert fieldsValidation.id(invalid_cedula) == False

def test_valid_mail():
    assert fieldsValidation.mail(valid_email) == True

def test_invalid_mail():
    assert fieldsValidation.mail(invalid_email) == False

def test_valid_date():
    assert fieldsValidation.date(valid_date)[0] == True

def test_invalid_date():
    assert fieldsValidation.date(invalid_date) == False

def test_valid_name():
    assert fieldsValidation.name(valid_name) == True

def test_invalid_name():
    assert fieldsValidation.name(invalid_name) == False

def test_valid_phone():
    assert fieldsValidation.phone(valid_phone) == True

def test_invalid_phone():
    assert fieldsValidation.phone(invalid_phone) == False

def test_valid_vax():
    assert fieldsValidation.vax(valid_Vax_Name) == True

def test_invalid_vax():
    assert fieldsValidation.vax(invalid_Vax_Name) == False


#POST USER tests
def test_post_user_check_status_code_equals_415():
    api_url = "http://localhost:5000/newuser"
    todo = "Not a JSON value"
    response = requests.post(api_url, data=todo)
    assert response.status_code == 415

def test_post_user_check_status_code_equals_400():
    api_url = "http://localhost:5000/newuser"
    todo = {"nombre":"TestName","apellido":"TestLastName","cedula":invalid_cedula,"correo":"test@myemail.com"}
    response = requests.post(api_url, json=todo)
    assert response.status_code == 400

def test_post_user_check_status_code_equals_200():
    api_url = "http://localhost:5000/newuser"
    todo = {"nombre":"TestName","apellido":"TestLastName","cedula":valid_cedula,"correo":"test@myemail.com"}
    response = requests.post(api_url, json=todo)
    assert response.status_code == 200

#POST VACCINE tests
def test_post_vaccine_check_status_code_equals_415():
    api_url = "http://localhost:5000/vaccine"
    todo = "Not a JSON value"
    response = requests.post(api_url, data=todo)
    assert response.status_code == 415

def test_post_vaccine_check_status_code_equals_400():
    api_url = "http://localhost:5000/vaccine"
    todo = {"cedula":"170602994A","vacuna":invalid_Vax_Name,"fecha":"05-05-2021"}
    response = requests.post(api_url, json=todo)
    assert response.status_code == 400

def test_post_vaccine_check_status_code_equals_201():
    api_url = "http://localhost:5000/vaccine"
    todo = {"cedula":"1706029947","vacuna":valid_Vax_Name,"fecha":"05-05-2021"}
    response = requests.post(api_url, json=todo)
    assert response.status_code == 201

#GET tests
def test_get_user_check_status_code_equals_400():
    api_url = "http://localhost:5000/user?cedula="+invalid_cedula+"&"+valid_field+"=1"
    response = requests.get(api_url)
    assert response.status_code == 400

def test_get_user_check_status_code_equals_404():
    api_url = "http://localhost:5000/user?cedula="+valid_cedula+"&"+invalid_field+"=1"
    response = requests.get(api_url)
    assert response.status_code == 404

def test_get_user_check_status_code_equals_200():
    api_url = "http://localhost:5000/user?cedula="+valid_cedula+"&"+valid_field+"=1"
    response = requests.get(api_url)
    assert response.status_code == 200

#GET FILTER tests
def test_get_filter_check_status_code_equals_404():
    api_url = "http://localhost:5000/getdata?vacu"
    response = requests.get(api_url)
    assert response.status_code == 404

def test_get_filter_check_status_code_equals_200():
    api_url = "http://localhost:5000/getdata?vacuna"
    response = requests.get(api_url)
    assert response.status_code == 200

#PUT tests
def test_put_user_check_status_code_equals_415():
    api_url = "http://localhost:5000/update"
    todo = "Not a JSON value"
    response = requests.put(api_url, data=todo)
    assert response.status_code == 415

def test_put_user_check_status_code_equals_400():
    api_url = "http://localhost:5000/update"
    todo = {"cedula":invalid_cedula,"domicilio":"Anywhere","nacimiento":"01-11-1990"}
    response = requests.put(api_url, json=todo)
    assert response.status_code == 400

def test_put_user_check_status_code_equals_201():
    api_url = "http://localhost:5000/update"
    todo = {"cedula":valid_cedula,"domicilio":"Anywhere","nacimiento":"01-11-1990"}
    response = requests.put(api_url, json=todo)
    assert response.status_code == 201

#DELETE tests
def test_delete_user_check_status_code_equals_400():
    api_url = "http://localhost:5000/delete?cedula="+invalid_cedula
    response = requests.get(api_url)
    assert response.status_code == 400

def test_delete_user_check_status_code_equals_200():
    api_url = "http://localhost:5000/delete?cedula="+valid_cedula
    response = requests.get(api_url)
    assert response.status_code == 201

def test_delete_user_check_status_code_equals_404():
    api_url = "http://localhost:5000/delete?cedula="+valid_cedula
    response = requests.get(api_url)
    assert response.status_code == 404

