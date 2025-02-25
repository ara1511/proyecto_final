import os
from dotenv import load_dotenv
from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

load_dotenv()

STRCNX_local="sqlite:///dbfinal.db"

ENGINE=os.getenv('ENGINE')
HOST=os.getenv('HOST')
USER=os.getenv('USER')
PWDS=os.getenv('PWDS')
DBA=os.getenv('DBA')
PORTDB=os.getenv('PORTDB')

STRCNX_prod = f"{ENGINE}://{USER}:{PWDS}@{HOST}:{PORTDB}/{DBA}"

if os.getenv('ENVIROMENT') == 'local':
    SQLALCHEMY_DATABASE_URI=STRCNX_local
else:
    SQLALCHEMY_DATABASE_URI=STRCNX_prod
    
security = HTTPBasic()