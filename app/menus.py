from typing import List
from fastapi import APIRouter, Depends

from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app import schemas
from app.crud import DishCRUD, MenuCRUD, SubmenuCRUD
from app.database import get_db
from app.models import Dish, Menu, SubMenu

router = APIRouter()


menu_crud = MenuCRUD()
submenu_crud = SubmenuCRUD()
dish_crud = DishCRUD()


# MENU


@router.post('/menus/', name='post_menu', status_code=201, response_model=schemas.Menu)
def create_menu(item_schema: schemas.MenuCreate, db: Session = Depends(get_db)) -> Menu:
    new_menu = menu_crud.create_item(db=db, item_schema=item_schema)
    return new_menu


@router.get('/menus/', name='get_menus', response_model=List[schemas.MenuReponse])  # type: ignore
# @cache(expire=60)
def read_menus(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''
) -> List[Menu]:  # type: ignore
    menus = menu_crud.read_items(db=db, limit=limit, page=page, search=search)
    for menu in menus:
        menu.submenus_count = len(menu.submenus)
        menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)
    return menus

@router.get('/menus/', name='get_menus', response_model=List[schemas.MenuReponse])  # type: ignore
# @cache(expire=60)
def read_menus(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''
) -> List[Menu]:  # type: ignore
    menus = menu_crud.read_items(db=db, limit=limit, page=page, search=search)
    for menu in menus:
        menu.submenus_count = len(menu.submenus)
        menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)
    return menus


@router.get('/menus/{menu_id}', name='get_menu', response_model=schemas.MenuReponse)
# @cache(expire=60)
async def read_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = menu_crud.read_item(db=db, menu_id=menu_id)

    menu.submenus_count = len(menu.submenus)
    menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)

    return menu


@router.patch('/menus/{menu_id}', name='patch_menu', response_model=schemas.Menu)
async def update_menu(
    menu_id: int, item_schema: schemas.MenuUpdate, db: Session = Depends(get_db)
) -> Menu:
    updated_menu = menu_crud.update_item(
        db=db,
        item_schema=item_schema,
        item_id=menu_id,
        menu_id=menu_id,
    )
    return updated_menu


@router.delete('/menus/{menu_id}', name='delete_menu')
async def delete_menu(menu_id: int, db: Session = Depends(get_db)) -> None:
    # redis_client.delete(get_cache_key("GET", "{routers}/menus/"))
    return menu_crud.delete_item(
        db=db,
        item_id=menu_id,
        menu_id=menu_id,
    )


# SUBMENU


@router.post(
    '/menus/{menu_id}/submenus',
    name='post_submenu',
    status_code=201,
    response_model=schemas.SubMenu,
)
async def create_submenu(
    menu_id: int, item_schema: schemas.SubMenuCreate, db: Session = Depends(get_db)
) -> SubMenu:
    new_submenu = submenu_crud.create_item(
        db=db, item_schema=item_schema, menu_id=menu_id
    )

    return new_submenu


@router.get(
    '/menus/{menu_id}/submenus',
    name='get_submenus',
    response_model=List[schemas.SubMenuReponse]  # type: ignore
)
# @cache(expire=60)
async def read_submenus(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''
) -> List[SubMenu]:  # type: ignore
    submenus = submenu_crud.read_items(db=db, limit=limit, page=page, search=search)
    for submenu in submenus:
        submenu.dishes_count = len(submenu.dishes)
    return submenus


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}',
    name='get_submenu',
    response_model=schemas.SubMenuReponse,
)
# @cache(expire=60)
async def read_submenu(
    menu_id: int, submenu_id: int, db: Session = Depends(get_db)
) -> SubMenu:
    submenu = submenu_crud.read_item(db=db, menu_id=menu_id, submenu_id=submenu_id)
    submenu.dishes_count = len(submenu.dishes)
    return submenu


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}',
    name='patch_submenu',
    response_model=schemas.SubMenu,
)
async def update_submenu(
    menu_id: int,
    submenu_id: int,
    item_schema: schemas.SubMenuUpdate,
    db: Session = Depends(get_db),
) -> SubMenu:
    updated_menu = submenu_crud.update_item(
        db=db,
        item_schema=item_schema,
        menu_id=menu_id,
        submenu_id=submenu_id,
        item_id=submenu_id,
    )

    return updated_menu


@router.delete('/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(
    menu_id: int, submenu_id: int, db: Session = Depends(get_db)
) -> None:
    return submenu_crud.delete_item(
        db=db, menu_id=menu_id, submenu_id=submenu_id, item_id=submenu_id
    )


# DISH


@router.post(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/',
    name='post_dish',
    status_code=201,
    response_model=schemas.Dish,
)
async def create_dish(
    menu_id: int,
    submenu_id: int,
    item_schema: schemas.DishCreate,
    db: Session = Depends(get_db),
) -> Dish:
    new_dish = dish_crud.create_item(
        db=db, item_schema=item_schema, menu_id=menu_id, submenu_id=submenu_id
    )
    return new_dish


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/',
    name='get_dishes',
    response_model=List[schemas.Dish],  # type: ignore
)
# @cache(expire=60)
async def read_dishes(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''
) -> List[Dish]:  # type: ignore
    dishes = dish_crud.read_items(db=db, limit=limit, page=page, search=search)
    return dishes


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    name='get_dish',
    response_model=schemas.Dish,
)
# @cache(expire=60)
async def read_dish(
    menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)
) -> Dish:
    dish = dish_crud.read_item(
        db=db, submenu_id=submenu_id, menu_id=menu_id, dish_id=dish_id
    )
    return dish


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    name='patch_dish',
    response_model=schemas.Dish,
)
async def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    item_schema: schemas.DishUpdate,
    db: Session = Depends(get_db),
) -> Dish:
    updated_dish = dish_crud.update_item(
        db=db,
        item_id=dish_id,
        submenu_id=submenu_id,
        menu_id=menu_id,
        dish_id=dish_id,
        item_schema=item_schema,
    )

    return updated_dish


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', name='delete_dish'
)
async def delete_dish(
    menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)
) -> None:
    return dish_crud.delete_item(
        db=db, item_id=dish_id, submenu_id=submenu_id, menu_id=menu_id, dish_id=dish_id
    )
