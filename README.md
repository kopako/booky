🚧 This is under construction 🚧
# Real Estate Vagabond
A booking-like REST API application based on [Django](https://www.djangoproject.com/)

## 📦 Pre-installation

### ⚠️ Create `.env` file following `.env.local` template.


- IF .env.USE_REMOTE_DB=True then Prepare the Database
```commandline
bash create_secrets_for_docker.sh
docker compose -f docker-compose.yaml up -d db
```
- Prepare the Application
```commandline
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## 🔧 Postinstall
```commandline
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
## 🚀 Run
```commandline
python manage.py runserver
```
## 🏄🏼‍♂️ Usage
Navigate to application:  
[DJANGO admin panel](http://localhost:8000/admin/)  
[OpenAPI with SWAGGER](http://localhost:8000/swagger/)  
[OpenAPI with REDOC](http://localhost:8000/redoc/)  


  