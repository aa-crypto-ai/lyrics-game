F:

cd Alvin\notebooks\multichat
set PYTHONPATH=%PYTHONPATH%;.
set DJANGO_SETTINGS_MODULE=multichat.settings
call workon lyrics_game_new
python manage.py runserver 0.0.0.0:80