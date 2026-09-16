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
    has_permission,
    is_key_expired,
    is_key_usable,
    issue_key,
    mask_api_key,
    revoke_key,
    sort_keys,
)
from storage import (
    load_applications,
    load_keys,
    save_applications,
    save_keys,
)
from utils import input_date, input_int


def show_applications(applications: dict[int, dict]) -> None:
    """Вывести список приложений."""
    if not applications:
        print('Приложений пока нет.')
        return
    print('ID  Название                    Владелец')
    for application in sort_applications(applications):
        print(
            f'{application["id"]:<4}'
            f'{application["name"]:<28}'
            f'{application["owner"]}'
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
    print('1. Показать приложения')
    print('2. Найти приложение по названию')
    print('3. Добавить приложение')
    print('4. Показать ключи')
    print('5. Проверить статус ключа')
    print('6. Проверить разрешение ключа')
    print('7. Выпустить ключ')
    print('8. Отозвать ключ')
    print('9. Показать статистику')
    print('0. Выход')


def main() -> None:
    """Точка запуска: меню и вызов функций проекта."""
    applications = load_applications()
    keys = load_keys()

    while True:
        print_menu()
        choice = input('Выберите действие: ').strip()

        if choice == '1':
            show_applications(applications)

        elif choice == '2':
            query = input('Подстрока названия: ').strip()
            found = find_application(applications, query)
            if not found:
                print('Ничего не найдено.')
            else:
                for item in found:
                    print(f'{item["id"]}. {item["name"]} ({item["owner"]})')

        elif choice == '3':
            name = input('Название приложения: ').strip()
            owner = input('Владелец: ').strip()
            if not name or not owner:
                print('Название и владелец не должны быть пустыми.')
                continue
            add_application(applications, name, owner)
            save_applications(applications)
            print('Приложение добавлено.')

        elif choice == '4':
            show_keys(keys, applications)

        elif choice == '5':
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

        elif choice == '6':
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

        elif choice == '7':
            app_id = _choose_application(applications)
            if app_id is None:
                continue
            permission = input('Разрешение (read/write/admin): ').strip()
            if permission not in {'read', 'write', 'admin'}:
                print('Некорректное разрешение.')
                continue
            expiry_date = input_date('Срок действия (ГГГГ-ММ-ДД): ')
            key = issue_key(keys, app_id, permission, expiry_date)
            save_keys(keys)
            print(
                'Ключ выпущен: '
                f'{mask_api_key(key["value"])} (id={key["id"]})'
            )

        elif choice == '8':
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

        elif choice == '9':
            show_stats(keys)

        elif choice == '0':
            save_applications(applications)
            save_keys(keys)
            print('Данные сохранены. Выход.')
            break

        else:
            print('Неизвестная команда. Выберите пункт меню.')


if __name__ == '__main__':
    main()
