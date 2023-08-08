import os
from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app import schemas
from app.crud import SubmenuCRUD
from app.database import get_db
from app.models import SubMenu

router = APIRouter()


def get_cache(expire=60):
    if os.environ.get('MENU_ENV') == 'app':
        return cache(expire=expire)
    else:
        def no_cache_decorator(func):
            return func
        return no_cache_decorator


submenu_crud = SubmenuCRUD()


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
    response_model=List[schemas.SubMenuReponse]
)
@get_cache(expire=60)
async def read_submenus(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''
) -> List[SubMenu]:
    submenus = submenu_crud.read_items(db=db, limit=limit, page=page, search=search)
    for submenu in submenus:
        submenu.dishes_count = len(submenu.dishes)
    return submenus


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}',
    name='get_submenu',
    response_model=schemas.SubMenuReponse,
)
@get_cache(expire=60)
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
