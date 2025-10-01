from sentence_transformers import SentenceTransformer
import pandas as pd
import faiss
import numpy as np

# Load product data
df = pd.read_csv("../data/products.csv")

# Model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode product descriptions
embeddings = model.encode(df["description"].tolist(), convert_to_numpy=True).astype("float32")

# Normalize embeddings (important for cosine similarity)
faiss.normalize_L2(embeddings)

# Build FAISS index
index = faiss.IndexFlatIP(embeddings.shape[1])  # inner product = cosine similarity if normalized
index.add(embeddings)

# Save index + product IDs
faiss.write_index(index, "../data/products.index")
np.save("../data/product_ids.npy", df["id"].values)

print("FAISS index and product IDs saved successfully!")
