export default async function handler(req, res) {
  const { product_id } = req.query;
  const response = await fetch(
    `http://127.0.0.1:8000/similar/${product_id}`
  );
  const data = await response.json();
  res.status(200).json(data);
}
