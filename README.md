Create virtual environment and run
pip install -r requirements.txt

then from folder app/db run
init_db.py
then from folder app run
uvicorn main:app --reload

optional you can run script seed_db.py
don't forget create .env file and configure db connection