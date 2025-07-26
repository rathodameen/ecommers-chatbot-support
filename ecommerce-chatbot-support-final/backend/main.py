from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# Load datasets (mock loading - you need to place the files in the right location)
try:
    orders_df = pd.read_csv("backend/data/orders.csv")
    products_df = pd.read_csv("backend/data/products.csv")
except Exception:
    orders_df = pd.DataFrame()
    products_df = pd.DataFrame()

@app.get("/")
def read_root():
    return {"message": "E-commerce chatbot backend is running."}

@app.get("/top-products")
def get_top_products():
    try:
        top = products_df.sort_values(by="sold", ascending=False).head(5)
        return top[["product_id", "name", "sold"]].to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/order-status/{order_id}")
def get_order_status(order_id: int):
    try:
        order = orders_df[orders_df["order_id"] == order_id]
        if order.empty:
            raise HTTPException(status_code=404, detail="Order not found.")
        return order.to_dict(orient="records")[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock/{product_name}")
def get_stock(product_name: str):
    try:
        item = products_df[products_df["name"].str.lower() == product_name.lower()]
        if item.empty:
            raise HTTPException(status_code=404, detail="Product not found.")
        return {"product": product_name, "stock": int(item.iloc[0]["stock"])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
