# Toy Factory Project

This project is a toy factory management system.

## How to Run
1. Install Docker and Docker Compose.
2. Run the command: `docker-compose up -d --build`
3. The website will be available at: http://localhost:8000/

## Accounts
- Admin: you can create your superuser using: `docker-compose exec web python3 manage.py createsuperuser`, than you must to enter username: `your_username`, date of birth: `yyyy-mm-dd` (only 18+), and finally enter your password twice: `your_password`
- Client: go to admin panel at: http://localhost:8000/admin/, than create at least one city model, after you can create Client exact at admin panel, or register at http://localhost:8000/accounts/register/
- Employee: create in admin panel at: http://localhost:8000/admin/

## Features
- Integration with the News API and Random Fox API.
- Test coverage ~ 87%.