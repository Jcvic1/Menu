import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis  # type ignore
from app.database import Base, engine
from app.main import app
from app.config import settings



TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)

# Drop all existing tables before each test

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)


# Use a pytest fixture to create a clean database for each test
@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



client = TestClient(app)



menu_data = {'title': 'Sample Menu 1', 'description': 'Menu Description 1'}

submenu_data = {
    'title': 'Sample SubMenu 1',
    'description': 'SubMenu Description 1',
}

dish_data = {
    'title': 'Sample Dish 1',
    'description': 'Dish Description 1',
    'price': '1.50',
}

dish_datas = [
    {
        'title': 'Sample Dish 1',
        'description': 'Dish Description 1',
        'price': '1.50',
    },
    {
        'title': 'Sample Dish 2',
        'description': 'Dish Description 2',
        'price': '2.50',
    },
    {
        'title': 'Sample Dish 3',
        'description': 'Dish Description 3',
        'price': '3.50',
    },
    {
        'title': 'Sample Dish 4',
        'description': 'Dish Description 4',
        'price': '4.50',
    },
    {
        'title': 'Sample Dish 5',
        'description': 'Dish Description 5',
        'price': '5.50',
    },
]

update_dish_datas = [
    {
        'title': 'Sample Dish Update 1',
        'description': 'Dish Description Update 1',
        'price': '5.50',
    },
    {
        'title': 'Sample Dish Update 2',
        'description': 'Dish Description Update 2',
        'price': '4.50',
    },
    {
        'title': 'Sample Dish Update 3',
        'description': 'Dish Description Update 3',
        'price': '3.50',
    },
    {
        'title': 'Sample Dish 4',
        'description': 'Dish Description 4',
        'price': '2.50',
    },
    {
        'title': 'Sample Dish 5',
        'description': 'Dish Description 5',
        'price': '1.50',
    },
]


def get_menu_id():
    response = client.get(app.url_path_for('get_menus'))
    assert response.status_code == 200
    menu_list = response.json()

    return menu_list[0]['id']


def get_submenu_id():
    menu_id = get_menu_id()
    response = client.get(app.url_path_for('get_submenus', menu_id=menu_id))
    assert response.status_code == 200
    submenu_list = response.json()

    return submenu_list[0]['id']


def test_create_dish():
    # create menu

    response = client.post(app.url_path_for('post_menu'), json=menu_data)
    assert response.status_code == 201
    assert response.json()['title'] == menu_data['title']
    assert 'id' in response.json()

    menu_id = get_menu_id()

    # create submenu

    response = client.post(app.url_path_for('post_submenu', menu_id=menu_id),
                           json=submenu_data)
    assert response.status_code == 201
    assert response.json()['title'] == submenu_data['title']
    assert 'id' in response.json()

    submenu_id = get_submenu_id()

    # create dish

    response = client.post(
        app.url_path_for('post_dish', menu_id=menu_id, submenu_id=submenu_id),
        json=dish_data
    )
    assert response.status_code == 201
    assert response.json()['title'] == dish_data['title']
    assert 'id' in response.json()

    response = client.get(
        app.url_path_for('get_dishes', menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200
    dish_list = response.json()

    dish_id = dish_list[0]['id']

    response = client.delete(
        app.url_path_for( 'delete_dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    )


def test_read_dishes():
    menu_id = get_menu_id()
    submenu_id = get_submenu_id()

    for dish_data in dish_datas:
        response = client.post(
            app.url_path_for('post_dish', menu_id=menu_id, submenu_id=submenu_id),
            json=dish_data
        )
        assert response.status_code == 201
        assert 'id' in response.json()

    response = client.get(
        app.url_path_for('get_dishes', menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200
    dish_list = response.json()
    assert isinstance(dish_list, list)

    titles = [dish['title'] for dish in dish_list]

    expected_titles = [dish_data['title'] for dish_data in dish_datas]
    assert titles == expected_titles

    for dish in dish_list:
        response = client.delete(
            app.url_path_for('delete_dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish['id'])
        )


def test_read_dish():
    menu_id = get_menu_id()
    submenu_id = get_submenu_id()

    response = client.post(
        app.url_path_for('post_dish', menu_id=menu_id, submenu_id=submenu_id),
        json=dish_data
    )
    assert response.status_code == 201
    assert response.json()['title'] == dish_data['title']
    assert 'id' in response.json()

    response = client.get(
        app.url_path_for( 'get_dishes', menu_id=menu_id, submenu_id=submenu_id))
    assert response.status_code == 200
    dish_list = response.json()

    dish_id = dish_list[0]['id']
    title = dish_list[0]['title']

    response = client.get(
        app.url_path_for('get_dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    )
    assert response.status_code == 200
    assert response.json()['title'] == title

    response = client.delete(
        app.url_path_for('delete_dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))


def test_update_dish():
    menu_id = get_menu_id()
    submenu_id = get_submenu_id()

    for update_dish_data in update_dish_datas:
        response = client.post(
            app.url_path_for('post_dish', menu_id=menu_id, submenu_id=submenu_id),
            json=update_dish_data,
        )
        assert response.status_code == 201
        assert 'id' in response.json()

    response = client.get(
        app.url_path_for('get_dishes', menu_id=menu_id, submenu_id=submenu_id))
    assert response.status_code == 200
    dish_list = response.json()
    assert isinstance(dish_list, list)

    titles = [dish['title'] for dish in dish_list]

    expected_titles = [
        update_dish_data['title'] for update_dish_data in update_dish_datas
    ]
    assert titles == expected_titles

    for dish in dish_list:
        response = client.delete(
            app.url_path_for('delete_dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish['id'])
        )


def test_delete_dish():
    menu_id = get_menu_id()
    submenu_id = get_submenu_id()

    response = client.post(
        app.url_path_for('post_dish', menu_id=menu_id, submenu_id=submenu_id),
        json=dish_data
    )
    assert response.status_code == 201
    assert response.json()['title'] == dish_data['title']
    assert 'id' in response.json()

    response = client.get(
        app.url_path_for('get_dishes', menu_id=menu_id, submenu_id=submenu_id))
    assert response.status_code == 200
    dish_list = response.json()

    dish_id = dish_list[0]['id']

    response = client.delete(
        app.url_path_for('delete_dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    )

    response = client.get(
        app.url_path_for('get_dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    )
    assert response.status_code == 404

    response = client.delete(
        app.url_path_for('delete_submenu', menu_id=menu_id, submenu_id=submenu_id))

    response = client.get(app.url_path_for('get_submenu', menu_id=menu_id, submenu_id=submenu_id))
    assert response.status_code == 404

    response = client.delete(app.url_path_for('delete_menu', menu_id=menu_id))

    response = client.get(app.url_path_for('get_menu', menu_id=menu_id))
    assert response.status_code == 404
