import bcrypt


def make_password(password: str) -> str:
    # Превращаем строку в байты
    password = password.encode()

    # Генерируем "соль"
    salt = bcrypt.gensalt()

    # Хешируем пароль с использованием соли и декодируем (превращаем в строку)
    hashed_password = bcrypt.hashpw(password, salt).decode()

    return hashed_password


def check_password(password: str, hashed_password: str) -> bool:
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)
