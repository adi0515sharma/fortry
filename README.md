# expound-backend
## Getting started

Steps:

1. Clone/pull/download this repository
2. Create a virtualenv with `virtualenv venv` and install dependencies with `pip install -r requirements.txt`
3. Run the following commands for linting:
    - ```bash 
        cp pre-commit ./.git/hooks/
        chmod +x ./.git/hooks/pre-commit

        ```
4. Navigate into your project with `python manage.py runserver`

Superuser:

- [x] Username: admin Password: admin