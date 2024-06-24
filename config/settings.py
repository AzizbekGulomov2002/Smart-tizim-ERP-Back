"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b=b(o4xn-1^#+c2$om3t77tic3jlmu+$%huu8b80tzd0+bcod*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "django.contrib.staticfiles",

    'apps.app',
    'apps.products',
    'apps.users',
    'apps.trade',
    'apps.finance',

    'rest_framework.authtoken',
    "rest_framework",
    "corsheaders",
    "django_filters",

    # "rest_framework_simplejwt",
    "drf_yasg",
    # "rest_framework_simplejwt.token_blacklist",
    "debug_toolbar",

]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:5173",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

INTERNAL_IPS = [
    "127.0.0.1",
]

# LOGGING = {
#     'version':1,
#     'handlers':{
#          'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log'
#         },
#         'console':{'class':'logging.StreamHandler'}
#     },
#     'loggers':{
#         'django.db.backends':{
#             'handlers':['file'],
#             'level':'DEBUG'
#                     }
#                }
# }   #  mobodo debug tulbar ishlamasa


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'config.urls'
AUTH_USER_MODEL = "users.User"


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
     'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
     'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
     ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# REST_FRAMEWORK = {
#     # This is for JSON
#     # "DEFAULT_RENDERER_CLASSES": (
#     #     "config.custom_renderers.CustomRenderer",
#     #     "rest_framework.renderers.JSONRenderer",
#     # ),
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         'rest_framework.authentication.BasicAuthentication',
#         # 'rest_authtoken.auth.AuthTokenAuthentication',
#         # "rest_framework.authentication.SessionAuthentication",
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     # 'DEFAULT_PERMISSION_CLASSES': (
#     #     'rest_framework.permissions.AllowAny',
#     # ),
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.IsAuthenticated",
#     ],
#     "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
#     # "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'uz-uz'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': False,
    'body_small_text': False,
    'brand_small_text': False,
    'brand_colour': 'navbar-primary',
    'accent': 'accent-navy',
    'navbar': 'navbar-light',
    'no_navbar_border': False,
    'navbar_fixed': True,
    'layout_boxed': False,
    'footer_fixed': False,
    'sidebar_fixed': True,
    'sidebar': 'sidebar-dark-primary',
    'sidebar_nav_small_text': False,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': True,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': False,
    'app_name': 'Your App Name',
    'usermenu_hide': False,
    'usermenu_collapsed': False,
}

JAZZMIN_SETTINGS = {
    "site_title": "Smart-tizim ERP",
    "site_header": "Smart-tizim ERP",
    "site_brand": "Smart-tizim ERP",
    "site_logo": "books/img/logo.png",
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome to the Smart-tizim ERP",
    "copyright": "Acme Smart-tizim ERP Ltd",
    "search_model": ["auth.User", "auth.Group"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://t.me/AzizbekGulomov", "new_window": True},
        {"model": "auth.User"},
        {"app": "books"},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "https://t.me/AzizbekGulomov", "new_window": True},
        {"model": "auth.user"}
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],
    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },
    'site_title': 'Admin Panel',
    'site_header': 'Admin Panel',
    'site_logo': 'path/to/logo.png',
    'welcome_sign': 'Welcome to the Smart tizim ERP superadmin panel',
    'search_model': 'auth.User',
    'show_sidebar': True,
    'navigation_expanded': False,
    'hide_apps': [],
    # icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        "app.Worker": "fa fa-address-book",
        "app.Position": "fa fa-user-secret",

        "products.Product": "fa fa-cubes",
        "products.Storage": "fa fa-trash",
        "products.StorageProduct": "fa fa-shopping-basket",
        "products.Category": "fa fa-tags",
        "products.Format": "fa fa-th-list",
        "products.Supplier": "fa fa-id-card",
        "products.StorageProductOff": "fa fa-trash",

        "finance.FinanceOutcome": "fa fa-suitcase",
        "finance.Payments": "fa fa-credit-card",
        "finance.Transaction": "fa fa-align-center",

        "trade.Addition_service": "fa fa-cogs",
        "trade.ServiceType": "fa fa-cog",
        "trade.Client": "fa fa-users",
        "trade.Trade": "fa fa-cart-plus",
        "trade.TradeDetail": "fa fa-shopping-basket",


        "users.User": "fa fa-users",
        "users.Director": "fa fa-user",
        "users.Manager": "fa fa-user-circle",
        "users.Company": "fa fa-building",

        "users.CompanyPayments": "fa fa-credit-card",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
