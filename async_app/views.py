from aiohttp import web
from aiohttp_jinja2 import template
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from aiohttp.web_request import Request
from aiohttp_session import get_session

from .database.connector import db_conn
from .models import Post, User
from .services.mixins import ValidateRegisterMixin


class BaseView(web.View):

    def prepare_context(self, new_context: dict = None) -> dict:
        context = {'request': self.request}
        if new_context:
            context.update(new_context)
        return context


class HomeView(BaseView):
    @template("home.html")
    async def get(self):
        async with db_conn.session as session:
            query = select(Post).options(joinedload(Post.user))
            result = await session.execute(query)
            all_posts = result.scalars().all()

            username = self.request.user.username if self.request.user else "Anonymous"
            # Возвращаем контекст в шаблон.
            context = ({"title": "Hello World", "user": username, "posts": all_posts})

            return self.prepare_context(context)


class NoteCreateView(BaseView):
    @template("notes/create_form.html")
    async def get(self):
        return self.prepare_context()

    @template("notes/create_form.html")
    async def post(self):
        user_data = await self.request.post()
        title = user_data.get('title')
        content = user_data.get('content')
        post = await Post.create(title=title, content=content, user_id=self.request.user.id)
        raise web.HTTPFound(f"/notes/{post.id}")


class NoteShowView(BaseView):
    @template("notes/show_note.html")
    async def get(self):
        post_id = self.request.match_info.get('post_id')
        async with db_conn.session as session:
            query = select(Post).where(Post.id == post_id).options(joinedload(Post.user))
            post = await session.execute(query)
            context = {'post': post.scalar_one_or_none()}
            return self.prepare_context(context)


class LoginView(BaseView):

    @template("account/login.html")
    async def get(self):
        return self.prepare_context()  # Нет контекста.

    @template("account/login.html")
    async def post(self):
        user_data = await self.request.post()

        username = user_data.get('username')
        password = user_data.get('password')

        user = await User.get_valid_user(username, password)
        if not user:
            return self.prepare_context({"error": "Invalid username or password"})

        # Создать сессию пользователя!
        self.request.session["user_id"] = user.id

        raise web.HTTPFound("/")  # Перенаправление на главную!


async def logout(request):
    session = await get_session(request)
    session.pop('user_id', None)
    raise web.HTTPFound("/")


class RegisterView(BaseView, ValidateRegisterMixin):

    @template('account/register.html')
    async def get(self):
        return self.prepare_context()

    @template('account/register.html')
    async def post(self):
        is_valid = await self.is_valid()
        if is_valid:
            user = await User.create_user(**self.clean_data)
            self.request.session["user_id"] = user.id
            raise web.HTTPFound("/")

        else:
            result_dict: dict = {str: []}
            for errors in self.invalid_data.values():
                for error in errors:
                    result_dict['errors'].append(error)
                    result_dict.update(self.data)
        return self.prepare_context(result_dict)


class NoteChangeView(BaseView):

    @template("notes/change_note_form.html")
    async def get(self):
        if not self.request.user:
            raise web.HTTPForbidden()
        post: Post = await Post.get(id=self.request.match_info.get('post_id'))
        if post.user_id != self.request.user.id:
            raise web.HTTPForbidden()

        context = {'post': post}
        return self.prepare_context(context)

    @template("notes/change_note_form.html")
    async def post(self):
        user_data = await self.request.post()
        post_id = self.request.match_info.get('post_id')
        title = user_data.get('title')
        content = user_data.get('content')

        post: Post = await Post.get(id=post_id)
        if post:
            await post.update(title=title, content=content)
            return web.HTTPFound(f"/notes/{post_id}")
        else:
            return web.HTTPNotFound()
