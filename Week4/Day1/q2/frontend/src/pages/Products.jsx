import React, { useEffect, useState } from 'react';
import api from '../api';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';

function Products() {
  const { token, logout } = useAuth();
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  async function fetchProducts() {
    setLoading(true);
    try {
      const params = {};
      if (search) params.search = search;
      if (category) params.category = category;
      const resp = await api.get('/products', { params });
      setProducts(resp.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    logout();
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow p-4 flex justify-between">
        <h1 className="text-xl font-bold">Catalog</h1>
        {token && (
          <button onClick={handleLogout} className="text-sm text-red-600">
            Logout
          </button>
        )}
      </nav>

      <div className="max-w-5xl mx-auto p-4">
        <div className="flex space-x-2 mb-4">
          <input
            className="border px-3 py-2 rounded w-full"
            placeholder="Search products..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button
            className="bg-blue-600 text-white px-4 rounded"
            onClick={fetchProducts}
          >
            Search
          </button>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {products.map((p) => (
              <div
                key={p.id}
                className="bg-white shadow rounded p-4 flex flex-col"
              >
                {p.image_url && (
                  <img
                    src={p.image_url}
                    alt={p.name}
                    className="h-32 w-full object-cover rounded mb-2"
                  />
                )}
                <h2 className="font-semibold mb-1 line-clamp-2">{p.name}</h2>
                <p className="text-sm text-gray-500 mb-2">{p.category}</p>
                <p className="font-bold mb-2">${p.price?.toFixed(2)}</p>
                {/* TODO: add detail link later */}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Products; 