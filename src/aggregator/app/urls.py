from aiohttp import web
from app import app, views

app.add_routes([
    web.get('/info/{account}/', views.get_info)
])
