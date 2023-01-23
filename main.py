from fastapi import FastAPI, Path, Query,HTTPException,status
from typing import Optional
from pydantic import BaseModel
import uvicorn
app = FastAPI()


#Request Model usually product
class Item(BaseModel):
    mark: str
    price: float
    product:Optional[str] = None

#Request Update Model usually product
class UpdateItem(BaseModel):
    mark: Optional[str] = None
    price: Optional[float] = None
    product:Optional[str] = None
#вьюшка
list_products = {
        1:{
            'mark':'Vim',
            'price':5.80,
            'product':'Milk'
        }
}
#Get
@app.get('/get-item/{product_id}')
def get_product(product_id:int = Path(None,description='The id of the product you like to view ',gt=0)):
    return list_products[product_id]
#query parametrs
@app.get('/get-by-name')
def get_product(*,mark:str = Query(None,title='Mark',description='Mark of product',max_length=10)):
    for product_id in list_products:
        if list_products[product_id]['mark'] == mark:
            return list_products[product_id]
    raise HTTPException(status_code=404,detail='Item mark Not Found')
#post
@app.post('/create-item/{product_id}')
def create_product(product_id:int,product: Item):
    if product_id in list_products:
        raise HTTPException(status_code=400,detail='Item ID already exists')
    list_products[product_id] = product
    return list_products[product_id]

#put
@app.put('/update-item/{product_id}')
def update_product(product_id:int,product: UpdateItem):
    if product_id not in list_products:
        raise HTTPException(status_code=404,detail='Item ID does not already exists')
    if product.mark != None:
        list_products[product_id].mark = product.mark
    if product.price != None:
        list_products[product_id].price = product.price

    if product.product != None:
        list_products[product_id].product = product.product

    return list_products[product_id]


#delete
@app.delete("/delete-item")
def delete_product(product_id:int = Query(..., description='The ID of the item to delete')):
    if product_id not in list_products:
        raise HTTPException(status_code=404,detail='Item ID does not already exists')
    #Инструкция удаляет переменные, элементы, ключи, срезы и атрибуты. del от delete (англ.) — удалить.
    del list_products[product_id]
    return {'Success':'Item delete'}






if __name__ == '__main__':
    uvicorn.run('main:app',port=8000,host='0.0.0.0',reload=True)






