# Простое хранилище в памяти: данные пока держим просто в списках.
users = []
projects = []

# Счётчики для автогенерации id (пользователь не передаёт id сам).
_next_user_id = 1
_next_project_id = 1


def next_user_id() -> int:
    global _next_user_id
    user_id = _next_user_id
    _next_user_id += 1
    return user_id


def next_project_id() -> int:
    global _next_project_id
    project_id = _next_project_id
    _next_project_id += 1
    return project_id
