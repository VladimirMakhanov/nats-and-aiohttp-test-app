from aiohttp import web
from app.app import app
from app import views

app.add_routes([
    web.get('/get_stat/{account}/', views.get_stat)
])
