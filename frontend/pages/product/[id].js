import { useRouter } from "next/router";
import useSWR from "swr";

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function ProductPage({ product }) {
  const router = useRouter();
  const { data, error } = useSWR(
    `/api/recommend?product_id=${product.id}`,
    fetcher
  );

  if (!product) return <div>Loading product...</div>;
  if (error) return <div>Error loading recommendations</div>;

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">{product.title}</h1>
      <p className="my-4">{product.description}</p>

      <h2 className="text-xl font-semibold mt-8">Similar Products:</h2>
      <div className="grid grid-cols-3 gap-4 mt-4">
        {data?.recommendations?.map((rec) => (
          <div key={rec.id} className="border p-4 rounded shadow">
            <h3 className="font-semibold">{rec.title}</h3>
            <p>{rec.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// Fetch product info server-side
export async function getServerSideProps({ params }) {
  const res = await fetch(`http://127.0.0.1:8000/products`);
  const allProducts = await res.json();
  const product = allProducts.find((p) => p.id === parseInt(params.id));

  return { props: { product: product || null } };
}
