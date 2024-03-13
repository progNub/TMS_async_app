from aiohttp import web

from . import views

routes = [
    web.get("/", handler=views.HomeView),  # Только метод get!
    web.route("*", "/login", handler=views.LoginView),
    web.route("*", "/register", handler=views.RegisterView),
    web.get("/logout", handler=views.logout),

    web.route("*", "/notes/create", handler=views.NoteCreateView),
    web.route("*", "/notes/{post_id}", handler=views.NoteShowView),
    web.route("*", "/notes/change/{post_id}", handler=views.NoteChangeView),
    web.route("*", "/notes/delete/{post_id}", handler=views.NoteDeleteView),

]
