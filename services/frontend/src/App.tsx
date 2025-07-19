import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResults([]);

    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: 5 }),
    });

    const data = await res.json();
    setResults(data.results || []);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 text-gray-900">
      <div className="max-w-2xl mx-auto bg-white shadow-md rounded-lg p-6">
        <h1 className="text-2xl font-bold mb-4">Ask HelpTulsa</h1>
        <form onSubmit={handleSearch} className="flex gap-4 mb-6">
          <input
            type="text"
            className="flex-1 border border-gray-300 rounded px-3 py-2"
            placeholder="e.g. Where can I get housing help?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            {loading ? "Searching..." : "Ask"}
          </button>
        </form>

        {results.length > 0 && (
          <ul className="space-y-4">
            {results.map((item, idx) => (
              <li key={idx} className="p-4 border rounded bg-gray-50">
                <h2 className="text-lg font-semibold">
                  {item.resource["Name"] || "Unknown"}
                </h2>

                {item.resource["Services/Notes"] && (
                  <p className="text-sm">{item.resource["Services/Notes"]}</p>
                )}

                {item.resource["Address"] && (
                  <p className="text-sm italic">{item.resource["Address"]}</p>
                )}

                {item.resource["URL"] && (
                  <a
                    href={item.resource["URL"]}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-600 underline"
                  >
                    {item.resource["URL"]}
                  </a>
                )}

                <p className="text-xs text-gray-500 mt-1">Score: {item.score}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
