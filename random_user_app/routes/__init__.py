from fastapi.templating import Jinja2Templates
from jinja2 import Environment, PackageLoader, select_autoescape
jinja_env = Environment(
    loader=PackageLoader("random_user_app"),
    autoescape=select_autoescape()
)

templates = Jinja2Templates(directory='random_user_app/templates')