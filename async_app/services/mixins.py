from async_app.models import User


class ValidateRegisterMixin:
    invalid_data: dict[str: [str]] = {}
    clean_data: dict[str, str] = {}
    data: dict[str, str] = {}

    async def validate_username(self) -> bool:
        key = 'username'
        username = self.data.get(key)

        errors = []
        if len(username) < 3:
            errors.append('Username должен состоять минимум из 3 символов.')

        if await User.get(username=username):
            errors.append('Такой username уже существует.')

        if errors:
            self.invalid_data[key] = errors
            return False
        self.clean_data[key] = username
        return True

    async def validate_email(self) -> bool:
        key = 'email'
        email = self.data.get(key)
        errors = []
        if len(email) < 3:
            errors.append('Email должен состоять минимум из 3 символов.')
        if await User.get(email=email):
            errors.append('Такой email уже существует.')
        if errors:
            self.invalid_data[key] = errors
            return False
        self.clean_data[key] = email
        return True

    async def validate_passwords(self) -> bool:
        key = 'password'
        password1 = self.data.get('password1')
        password2 = self.data.get('password2')
        error = []

        if password1 != password2:
            error.append('Пароли должны совпадать.')

        if len(password1) < 3 or len(password2) < 3:
            error.append('Password должен состоять минимум из 3 символов.')

        if error:
            self.invalid_data[key] = error
            return False
        self.clean_data[key] = password1
        return True

    async def is_valid(self) -> bool:
        self.data = dict(await self.request.post())
        await self.validate_username()
        await self.validate_email()
        await self.validate_passwords()

        if self.invalid_data:
            return False
        return True
