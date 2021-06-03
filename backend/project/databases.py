import os

# DEFAULT SQLITE EXAMPLE #
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', 5432),
        'NAME': os.getenv('DB_NAME', 'ambassador_db'),
        'USER': os.getenv('DB_USER', 'ambassador_user'),
        'PASSWORD': os.getenv('DB_PASS', 'ambassador_pass')
    }
}
