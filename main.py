from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from decimal import Decimal
from uuid import UUID, uuid4

app = FastAPI()


class MenuItem(BaseModel):
    naam: str
    omschrijving: Optional[str]
    prijs: Decimal
    allergenen: Optional[List[str]]
    urlPlaatje: Optional[HttpUrl]


class MenuItemIn(MenuItem):
    pass


class MenuItemOut(MenuItem):
    id: UUID


menuItem1 = MenuItemOut(id=uuid4(), naam="biertje", omschrijving="Lekker fris pils!", prijs=2.50, allergenen=[
                        "gluten"], urlPlaatje='https://www.fun-en-feest.nl/img/large/groot-decoratie-bord-biertje/10032/985.gif')
menuItem2 = MenuItemOut(id=uuid4(), naam="bitterballen", prijs=5.0)

example_source = [menuItem1, menuItem2]


@app.get("/menuitems", response_model=List[MenuItemOut])
def read_menu_items():
    return example_source


@app.get("/menuitem/{menuitem_id}", response_model=MenuItemOut)
def read_menu_item(menuitem_id: UUID):
    result = [menuitem for menuitem in example_source if menuitem.id == menuitem_id]
    if not result:
        raise HTTPException(
            status_code=404, detail="Menu item with id " + str(menuitem_id) + " not found")
    return result[0]


@app.post("/menuitem", response_model=MenuItemOut)
def create_menu_item(menuItem: MenuItemIn):
    # Assign new ID to klant
    menuItemOut = MenuItemOut(**menuItem.dict(), id=uuid4())
    example_source.append(menuItemOut)
    return menuItemOut


@app.put("/menuitem/{menuitem_id}", response_model=MenuItemOut)
def update_menu_item(menuitem_id: UUID, menuItem: MenuItemIn):
    result = [menuitem for menuitem in example_source if menuitem.id == menuitem_id]
    if not result:
        raise HTTPException(
            status_code=404, detail="Menu item with id " + str(menuitem_id) + " not found")
    example_source.remove(result[0])
    menuItemOut = MenuItemOut(**menuItem.dict(), id=menuitem_id)
    example_source.append(menuItemOut)
    return menuItemOut


@app.delete("/menuitem/{menuitem_id}", response_model=MenuItemOut)
def delete_menu_item(menuitem_id: UUID):
    result = [menuitem for menuitem in example_source if menuitem.id == menuitem_id]
    if not result:
        raise HTTPException(
            status_code=404, detail="Menu item with id " + str(menuitem_id) + " not found")
    example_source.remove(result[0])
    return result[0]
