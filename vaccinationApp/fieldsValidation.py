# Taken from https://micro.recursospython.com/recursos/como-validar-una-direccion-de-correo-electronico.html
import re
import string
from dateutil.parser import parse

body_regex = re.compile('''
    ^(?!\.)                            # name may not begin with a dot
    (
      [-a-z0-9!\#$%&'*+/=?^_`{|}~]     # all legal characters except dot
      |
      (?<!\.)\.                        # single dots only
    )+
    (?<!\.)$                            # name may not end with a dot
''', re.VERBOSE | re.IGNORECASE)
domain_regex = re.compile('''
    (
      localhost
      |
      (
        [a-z0-9]
            # [sub]domain begins with alphanumeric
        (
          [-\w]*                         # alphanumeric, underscore, dot, hyphen
          [a-z0-9]                       # ending alphanumeric
        )?
      \.                               # ending dot
      )+
      [a-z]{2,}                        # TLD alpha-only
   )$
''', re.VERBOSE | re.IGNORECASE)

space_punct_dict = dict((ord(punct), ' ') for punct in string.punctuation)

def mail(email):
    if not isinstance(email, str) or not email or '@' not in email:
        return False
    
    body, domain = email.rsplit('@', 1)

    match_body = body_regex.match(body)
    match_domain = domain_regex.match(domain)

    if not match_domain:
        # check for Internationalized Domain Names
        # see https://docs.python.org/2/library/codecs.html#module-encodings.idna
        try:
            domain_encoded = domain.encode('idna').decode('ascii')
        except UnicodeError:
            return False
        match_domain = domain_regex.match(domain_encoded)

    return (match_body is not None) and (match_domain is not None)

# Taken from https://fecyman10.wordpress.com/2014/05/01/validar-cedula-y-ruc-ecuatorianos-en-python/
# 01	Azuay
# 02	Bolivar
# 03	Cañar
# 04	Carchi
# 05	Cotopaxi
# 06	Chimborazo
# 07	El Oro
# 08	Esmeraldas
# 09	Guayas
# 10	Imbabura
# 11	Loja
# 12	Los Ríos
# 13	Manabí
# 14	Morona Santiago
# 15	Napo
# 16	Pastaza
# 17	Pichincha
# 18	Tungurahua
# 19	Zamora Chinchipe
# 20	Galápagos
# 21	Sucumbíos
# 22	Orellana
# 23	Santo Domingo de los Tsáchilas
# 24	Santa Elena

def id (nro):
    ret = False
    l = len(nro)
    if nro.isdigit() and l == 10: # verify logitude
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 24: # check province code
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6 : # number between 0 & 6
                ret = __validar_ced(nro)
    return ret

def __validar_ced(nro):
    total = 0
    base = 10
    d_ver = int(nro[9])
    multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)

    for i in range(0,len(multip)):
        p = int(nro[i]) * multip[i]
        total+=p if p < 10 else int(str(p)[0])+int(str(p)[1])

    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver
    
def date (val):
    if val:
        try:
            val = val.translate(space_punct_dict)
            new_date = str(parse(val))[:10]
            year = new_date[:4]
            month = new_date[5:7]
            day = new_date[8:]
            return True, year, month, day
        except:
            return False
    return False

def name (val):
    return val.isalpha()
    
def phone (val):
    return val.isdigit()
    
def vax (val):
    vaxList = {"Sputnik", "AstraZeneca", "Pfizer", "Jhonson&Jhonson"}
    return val in vaxList