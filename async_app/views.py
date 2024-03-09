from aiohttp import web
from aiohttp_jinja2 import template
from sqlalchemy.exc import NoResultFound

from .models import Post, User
from .services.mixins import ValidateRegisterMixin


class HomeView(web.View):
    @template("home.html")
    async def get(self):
        all_posts = await Post.all()
        print(all_posts)
        username = self.request.user.username if self.request.user else "Anonymous"

        # Возвращаем контекст в шаблон.
        return {"title": "Hello World", "user": username, "posts": all_posts}


class NoteCreateView(web.View):
    @template("notes/create_form.html")
    async def get(self):
        return {}

    @template("notes/create_form.html")
    async def post(self):
        user_data = await self.request.post()
        title = user_data.get('title')
        content = user_data.get('content')
        post = await Post.create(title=title, content=content, user_id=self.request.user)
        print(post)

        raise web.HTTPFound("/")
        # raise web.HTTPFound(f"/notes/{post.id}")


class LoginView(web.View):

    @template("account/login.html")
    async def get(self):
        return {}  # Нет контекста.

    @template("account/login.html")
    async def post(self):
        user_data = await self.request.post()

        username = user_data.get('username')
        password = user_data.get('password')

        try:
            user = await User.get_valid_user(username, password)
        except NoResultFound:
            return {"error": "Invalid username or password"}

        # Создать сессию пользователя!
        self.request.session["user_id"] = user.id

        raise web.HTTPFound("/")  # Перенаправление на главную!


class RegisterView(web.View, ValidateRegisterMixin):

    @template('account/register.html')
    async def get(self):
        return {}

    @template('account/register.html')
    async def post(self):
        is_valid = await self.is_valid()
        if is_valid:
            user = await User.create_user(**self.clean_data)
            self.request.session["user_id"] = user.id
            raise web.HTTPFound("/")

        else:
            result_dict: dict = {'errors': []}
            for errors in self.invalid_data.values():
                for error in errors:
                    result_dict['errors'].append(error)
                    result_dict.update(self.data)
        return result_dict
