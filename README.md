Create virtual environment and run
pip install -r requirements.txt

then from folder app/db run
init_db.py

to upply migrations
alembic upgrade head

then run
uvicorn main:app --reload

optional you can run script seed_db.py
don't forget create .env file and configure db connection