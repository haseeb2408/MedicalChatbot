import os 
from pathlib import Path
import logging


#setting up logging

logging.basicConfig(level=logging.INFO , format = '[%(asctime)s]: %(message)s:')


list_of_files = [
    "src/__init__.py",
    "src/helper.py" , 
    "requirements.txt",
    "setup.py",
    "app.py" , 
    "research/trials.ipynb"
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir , file_name = os.path.split(filepath)


    if filedir !='':
        os.makedirs(filedir , exist_ok=True)
        logging.info(f"Creating Director : {filedir} for the file : {file_name}")


    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath , 'w'):
            pass
        logging.info(f'Creating empty file : {filepath}')
    else:
        logging.info(f'{file_name} Already exists')