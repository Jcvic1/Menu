import os
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app import schemas
from app.crud import DishCRUD
from app.database import get_db
from app.models import Dish

router = APIRouter()


def get_cache(expire=60):
    if os.environ.get('MENU_ENV') == 'app':
        return cache(expire=expire)
    else:
        def no_cache_decorator(func):
            return func
        return no_cache_decorator


dish_crud = DishCRUD()


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
    response_model=List[schemas.Dish],
)
@get_cache(expire=60)
async def read_dishes(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''
) -> List[Dish]:
    dishes = dish_crud.read_items(db=db, limit=limit, page=page, search=search)
    return dishes


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    name='get_dish',
    response_model=schemas.Dish,
)
@get_cache(expire=60)
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
