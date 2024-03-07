from aiohttp import web

from . import views

routes = [
    web.get("/", handler=views.HomeView),  # Только метод get!
    web.route("*", "/login", handler=views.LoginView),
    web.route("*", "/notes/create", handler=views.NoteCreateView),
]
