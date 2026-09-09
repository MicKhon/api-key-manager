from datetime import date


def get_key_status(is_active: bool) -> str:
    """Возвращает текстовый статус API-ключа."""
    if is_active:
        return 'Ключ активен'
    return 'Ключ отозван'


def is_key_expired(expiry_date: date, today: date) -> bool:
    """Проверяет, истёк ли срок действия ключа."""
    if expiry_date < today:
        return True
    return False


def has_permission(
    user_permission: str,
    required_permission: str,
) -> bool:
    """Проверяет, достаточно ли разрешения для действия."""
    if user_permission == 'admin':
        return True
    if user_permission == required_permission:
        return True
    return False


def mask_api_key(api_key: str) -> str:
    """Маскирует ключ, оставляя видимыми крайние символы."""
    if len(api_key) < 8:
        return '***'
    prefix = api_key[0:4]
    suffix = api_key[-4:]
    return prefix + '...' + suffix


user_name = 'Михаил Хонинев'
app_name = 'Платежный шлюз'
api_key = 'ak_live_9f3a2c1b8e7d'
is_active = True
user_permission = 'write'
required_permission = 'write'
expiry_date = date(2026, 12, 31)
today = date(2026, 9, 9)

print(f'Пользователь: {user_name}')
print(f'Приложение: {app_name}')
print(f'Ключ: {mask_api_key(api_key)}')
print(get_key_status(is_active))

if is_key_expired(expiry_date, today):
    print('Срок действия ключа истёк.')
else:
    print('Срок действия ключа не истёк.')

if has_permission(user_permission, required_permission):
    print('Разрешение на запись есть.')
else:
    print('Разрешения на запись нет.')
