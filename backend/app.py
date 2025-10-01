from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import faiss, numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

app = FastAPI()

# Enable CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # use frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data at startup
@app.on_event("startup")
def load_index():
    global index, model, product_ids, products
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index("../data/products.index")
    product_ids = np.load("../data/product_ids.npy")
    products = pd.read_csv("../data/products.csv")

# Endpoint: all products
@app.get("/products")
def get_all_products():
    return products.to_dict(orient="records")

# Endpoint: similar products
@app.get("/similar/{product_id}")
def get_similar(product_id: int, k: int = 3):
    if product_id not in products["id"].values:
        return {"error": "Product not found"}
    row = products[products["id"] == product_id].iloc[0]
    emb = model.encode([row["description"]], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(emb)
    D, I = index.search(emb, k + 1)
    recs = []
    for i, idx in enumerate(I[0]):
        pid = int(product_ids[idx])
        if pid != product_id:
            recs.append({
                **products[products["id"] == pid].to_dict(orient="records")[0],
                "score": float(D[0][i])
            })
    return {"recommendations": recs}
