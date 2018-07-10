from aiohttp import web
from app.app import app
from app import views

app.add_routes([
    web.get('/tags/{account}/', views.get_tags)
])
