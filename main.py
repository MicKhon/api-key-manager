"""Точка запуска сервиса управления API-ключами."""

from datetime import date

from applications import (
    add_application,
    find_application,
    sort_applications,
)
from keys import (
    filter_active_keys,
    find_key,
    get_key_status,
    get_keys_stats,
    is_key_expired,
    is_key_usable,
    issue_key,
    mask_api_key,
    revoke_key,
    sort_keys,
)
from permissions import (
    find_permission,
    has_permission,
    sort_permissions,
)
from storage import (
    load_applications,
    load_keys,
    load_permissions,
    load_users,
    save_applications,
    save_keys,
    save_permissions,
    save_users,
)
from users import add_user, find_user, sort_users
from utils import input_date, input_int


def _user_name(users: dict[int, dict], user_id: int) -> str:
    user = users.get(user_id, {})
    return user.get('name', 'неизвестно')


def show_users(users: dict[int, dict]) -> None:
    """Вывести список пользователей."""
    if not users:
        print('Пользователей пока нет.')
        return
    print('ID  Имя')
    for user in sort_users(users):
        print(f'{user["id"]:<4}{user["name"]}')


def show_applications(
    applications: dict[int, dict],
    users: dict[int, dict],
) -> None:
    """Вывести список приложений."""
    if not applications:
        print('Приложений пока нет.')
        return
    print('ID  Название                    Владелец')
    for application in sort_applications(applications):
        owner = _user_name(users, application['user_id'])
        print(
            f'{application["id"]:<4}'
            f'{application["name"]:<28}'
            f'{owner}'
        )


def show_permissions(permissions: dict[int, dict]) -> None:
    """Вывести список разрешений."""
    if not permissions:
        print('Разрешений пока нет.')
        return
    print('ID  Код       Название')
    for permission in sort_permissions(permissions):
        print(
            f'{permission["id"]:<4}'
            f'{permission["code"]:<10}'
            f'{permission["title"]}'
        )


def show_keys(
    keys: dict[int, dict],
    applications: dict[int, dict],
) -> None:
    """Вывести список ключей с маскированием значения."""
    if not keys:
        print('Ключей пока нет.')
        return
    print('ID  Приложение                 Ключ              Статус')
    for key in sort_keys(keys):
        application = applications.get(key['app_id'], {})
        app_name = application.get('name', 'неизвестно')
        status = get_key_status(key['is_active'])
        print(
            f'{key["id"]:<4}'
            f'{app_name:<26}'
            f'{mask_api_key(key["value"]):<18}'
            f'{status}'
        )


def show_stats(keys: dict[int, dict]) -> None:
    """Вывести статистику по ключам."""
    stats = get_keys_stats(keys)
    active_keys = list(filter_active_keys(keys))
    print(
        f'Всего ключей: {stats["total"]}. '
        f'Активных: {stats["active"]}. '
        f'Отозванных: {stats["revoked"]}.'
    )
    print(f'Активных ключей в выборке: {len(active_keys)}.')


def _choose_user(users: dict[int, dict]) -> int | None:
    user_id = input_int('Введите ID пользователя: ')
    if user_id not in users:
        print('Пользователь не найден.')
        return None
    return user_id


def _choose_application(applications: dict[int, dict]) -> int | None:
    app_id = input_int('Введите ID приложения: ')
    if app_id not in applications:
        print('Приложение не найдено.')
        return None
    return app_id


def _choose_key(keys: dict[int, dict]) -> int | None:
    key_id = input_int('Введите ID ключа: ')
    if find_key(keys, key_id) is None:
        print('Ключ не найден.')
        return None
    return key_id


def print_menu() -> None:
    """Напечатать меню приложения."""
    print()
    print('=== Сервис управления API-ключами ===')
    print('1. Показать пользователей')
    print('2. Найти пользователя')
    print('3. Добавить пользователя')
    print('4. Показать приложения')
    print('5. Найти приложение')
    print('6. Добавить приложение')
    print('7. Показать разрешения')
    print('8. Показать ключи')
    print('9. Проверить статус ключа')
    print('10. Проверить разрешение ключа')
    print('11. Выпустить ключ')
    print('12. Отозвать ключ')
    print('13. Показать статистику')
    print('0. Выход')


def main() -> None:
    """Точка запуска: меню и вызов функций проекта."""
    users = load_users()
    applications = load_applications()
    permissions = load_permissions()
    keys = load_keys()

    while True:
        print_menu()
        choice = input('Выберите действие: ').strip()

        if choice == '1':
            show_users(users)

        elif choice == '2':
            query = input('Подстрока имени: ').strip()
            found = find_user(users, query)
            if not found:
                print('Ничего не найдено.')
            else:
                for item in found:
                    print(f'{item["id"]}. {item["name"]}')

        elif choice == '3':
            name = input('Имя пользователя: ').strip()
            if not name:
                print('Имя не должно быть пустым.')
                continue
            add_user(users, name)
            save_users(users)
            print('Пользователь добавлен.')

        elif choice == '4':
            show_applications(applications, users)

        elif choice == '5':
            query = input('Подстрока названия: ').strip()
            found = find_application(applications, query)
            if not found:
                print('Ничего не найдено.')
            else:
                for item in found:
                    owner = _user_name(users, item['user_id'])
                    print(f'{item["id"]}. {item["name"]} ({owner})')

        elif choice == '6':
            user_id = _choose_user(users)
            if user_id is None:
                continue
            name = input('Название приложения: ').strip()
            if not name:
                print('Название не должно быть пустым.')
                continue
            add_application(applications, name, user_id)
            save_applications(applications)
            print('Приложение добавлено.')

        elif choice == '7':
            show_permissions(permissions)

        elif choice == '8':
            show_keys(keys, applications)

        elif choice == '9':
            key_id = _choose_key(keys)
            if key_id is None:
                continue
            key = keys[key_id]
            today = date.today()
            expiry_date = date.fromisoformat(key['expiry_date'])
            print(get_key_status(key['is_active']))
            if is_key_expired(expiry_date, today):
                print('Срок действия ключа истёк.')
            else:
                print('Срок действия ключа не истёк.')

        elif choice == '10':
            key_id = _choose_key(keys)
            if key_id is None:
                continue
            required = input('Требуемое разрешение: ').strip()
            key = keys[key_id]
            today = date.today()
            if is_key_usable(keys, key_id, today, required):
                print('Ключ можно использовать для этого действия.')
            else:
                print('Ключ использовать нельзя.')
            if has_permission(key['permission'], required):
                print('Разрешение у ключа достаточное.')
            else:
                print('Разрешения недостаточно.')

        elif choice == '11':
            app_id = _choose_application(applications)
            if app_id is None:
                continue
            code = input('Код разрешения (read/write/admin): ').strip()
            if find_permission(permissions, code) is None:
                print('Некорректное разрешение.')
                continue
            expiry_date = input_date('Срок действия (ГГГГ-ММ-ДД): ')
            key = issue_key(keys, app_id, code, expiry_date)
            save_keys(keys)
            print(
                'Ключ выпущен: '
                f'{mask_api_key(key["value"])} (id={key["id"]})'
            )

        elif choice == '12':
            key_id = _choose_key(keys)
            if key_id is None:
                continue
            try:
                revoke_key(keys, key_id)
            except ValueError as error:
                print(error)
                continue
            save_keys(keys)
            print('Ключ отозван.')

        elif choice == '13':
            show_stats(keys)

        elif choice == '0':
            save_users(users)
            save_applications(applications)
            save_permissions(permissions)
            save_keys(keys)
            print('Данные сохранены. Выход.')
            break

        else:
            print('Неизвестная команда. Выберите пункт меню.')


if __name__ == '__main__':
    main()
