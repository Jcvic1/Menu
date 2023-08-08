import os
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app import schemas
from app.crud import MenuCRUD
from app.database import get_db
from app.models import Menu

router = APIRouter()


def get_cache(expire=60):
    if os.environ.get('MENU_ENV') == 'app':
        return cache(expire=expire)
    else:
        def no_cache_decorator(func):
            return func
        return no_cache_decorator


menu_crud = MenuCRUD()


# MENU


@router.post('/menus/', name='post_menu', status_code=201, response_model=schemas.Menu)
def create_menu(item_schema: schemas.MenuCreate, db: Session = Depends(get_db)) -> Menu:
    new_menu = menu_crud.create_item(db=db, item_schema=item_schema)
    return new_menu


@router.get('/menus/', name='get_menus', response_model=List[schemas.MenuReponse])
@get_cache(expire=60)
def read_menus(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''
) -> List[Menu]:
    menus = menu_crud.read_items(db=db, limit=limit, page=page, search=search)
    for menu in menus:
        menu.submenus_count = len(menu.submenus)
        menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)
    return menus


@router.get('/menus/{menu_id}', name='get_menu', response_model=schemas.MenuReponse)
@get_cache(expire=60)
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
    return menu_crud.delete_item(
        db=db,
        item_id=menu_id,
        menu_id=menu_id,
    )
