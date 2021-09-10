from pathlib import Path

# environment settings
base_dir = Path(__file__).resolve().parent.parent
key = 'b!forq1npj!x0fk&4(=@hz0kq(_7r(v(d!l19k&-1+9c+q8ij9'

databases = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': base_dir / 'data/cotabest.sqlite3',
    }
}
