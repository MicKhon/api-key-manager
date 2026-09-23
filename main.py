"""Точка запуска сервиса управления API-ключами."""

from datetime import date

from entities.applications import (
    Application,
    add_application,
    find_application,
    find_application_by_id,
    sort_applications,
)
from entities.keys import (
    ApiKey,
    filter_active_keys,
    find_key,
    get_keys_stats,
    issue_key,
    revoke_key,
    sort_keys,
)
from entities.permissions import (
    Permission,
    find_permission,
    sort_permissions,
)
from entities.users import (
    User,
    add_user,
    find_user,
    find_user_by_id,
    sort_users,
)
from storage.storage import (
    load_applications,
    load_keys,
    load_permissions,
    load_users,
    save_applications,
    save_keys,
    save_permissions,
    save_users,
)
from utils.utils import input_date, input_int


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print('Пользователей пока нет.')
        return
    print('ID  Имя')
    for user in sort_users(users):
        print(user)


def show_applications(applications: list[Application]) -> None:
    """Вывести список приложений."""
    if not applications:
        print('Приложений пока нет.')
        return
    print('ID  Название                    Владелец')
    for application in sort_applications(applications):
        print(
            f'{application.id:<4}'
            f'{application.name:<28}'
            f'{application.user.name}'
        )


def show_permissions(permissions: list[Permission]) -> None:
    """Вывести список разрешений."""
    if not permissions:
        print('Разрешений пока нет.')
        return
    print('ID  Код       Название')
    for permission in sort_permissions(permissions):
        print(
            f'{permission.id:<4}'
            f'{permission.code:<10}'
            f'{permission.title}'
        )


def show_keys(keys: list[ApiKey]) -> None:
    """Вывести список ключей с маскированием значения."""
    if not keys:
        print('Ключей пока нет.')
        return
    print('ID  Приложение                 Ключ              Статус')
    for key in sort_keys(keys):
        print(
            f'{key.id:<4}'
            f'{key.application.name:<26}'
            f'{ApiKey.mask_value(key.value):<18}'
            f'{key.status}'
        )


def show_stats(keys: list[ApiKey]) -> None:
    """Вывести статистику по ключам."""
    stats = get_keys_stats(keys)
    active_keys = list(filter_active_keys(keys))
    print(
        f'Всего ключей: {stats["total"]}. '
        f'Активных: {stats["active"]}. '
        f'Отозванных: {stats["revoked"]}.'
    )
    print(f'Активных ключей в выборке: {len(active_keys)}.')


def _choose_user(users: list[User]) -> User | None:
    user_id = input_int('Введите ID пользователя: ')
    user = find_user_by_id(users, user_id)
    if user is None:
        print('Пользователь не найден.')
        return None
    return user


def _choose_application(
    applications: list[Application],
) -> Application | None:
    app_id = input_int('Введите ID приложения: ')
    application = find_application_by_id(applications, app_id)
    if application is None:
        print('Приложение не найдено.')
        return None
    return application


def _choose_key(keys: list[ApiKey]) -> ApiKey | None:
    key_id = input_int('Введите ID ключа: ')
    key = find_key(keys, key_id)
    if key is None:
        print('Ключ не найден.')
        return None
    return key


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
    """Точка запуска: меню и вызов методов объектов."""
    users = load_users()
    applications = load_applications(users)
    permissions = load_permissions()
    keys = load_keys(applications, permissions)

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
                    print(item)

        elif choice == '3':
            name = input('Имя пользователя: ').strip()
            if not name:
                print('Имя не должно быть пустым.')
                continue
            add_user(users, name)
            save_users(users)
            print('Пользователь добавлен.')

        elif choice == '4':
            show_applications(applications)

        elif choice == '5':
            query = input('Подстрока названия: ').strip()
            found = find_application(applications, query)
            if not found:
                print('Ничего не найдено.')
            else:
                for item in found:
                    print(item)

        elif choice == '6':
            user = _choose_user(users)
            if user is None:
                continue
            name = input('Название приложения: ').strip()
            if not name:
                print('Название не должно быть пустым.')
                continue
            add_application(applications, name, user)
            save_applications(applications)
            print('Приложение добавлено.')

        elif choice == '7':
            show_permissions(permissions)

        elif choice == '8':
            show_keys(keys)

        elif choice == '9':
            key = _choose_key(keys)
            if key is None:
                continue
            today = date.today()
            print(key.status)
            if key.is_expired(key.expiry_date, today):
                print('Срок действия ключа истёк.')
            else:
                print('Срок действия ключа не истёк.')

        elif choice == '10':
            key = _choose_key(keys)
            if key is None:
                continue
            required = input('Требуемое разрешение: ').strip()
            today = date.today()
            if key.is_usable(today, required):
                print('Ключ можно использовать для этого действия.')
            else:
                print('Ключ использовать нельзя.')
            if key.permission.covers(required):
                print('Разрешение у ключа достаточное.')
            else:
                print('Разрешения недостаточно.')

        elif choice == '11':
            application = _choose_application(applications)
            if application is None:
                continue
            code = input('Код разрешения (read/write/admin): ').strip()
            permission = find_permission(permissions, code)
            if permission is None:
                print('Некорректное разрешение.')
                continue
            expiry_date = input_date('Срок действия (ГГГГ-ММ-ДД): ')
            key = issue_key(keys, application, permission, expiry_date)
            save_keys(keys)
            print(
                'Ключ выпущен: '
                f'{ApiKey.mask_value(key.value)} (id={key.id})'
            )

        elif choice == '12':
            key = _choose_key(keys)
            if key is None:
                continue
            try:
                revoke_key(keys, key.id)
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
