import { useState } from "react";
import { fetchPokemon } from "./lib/api";
import PokemonCard from "./components/PokemonCard";

export default function App() {
    const [name, setName] = useState("");
    const [data, setData] = useState(null);
    const [status, setStatus] = useState("idle"); // idle | loading | error | ok
    const [error, setError] = useState("");

    async function onSearch(e) {
        e.preventDefault();
        const q = name.trim().toLowerCase();
        if (!q) return;
        setStatus("loading"); setError(""); setData(null);
        try {
            const p = await fetchPokemon(q);
            setData(p); setStatus("ok");
        } catch (err) {
            setError(err.message || String(err));
            setStatus("error");
        }
    }
    return (
        <div className="min-h-screen grid place-items-center">
            <div className="text-center">
                <h1 className="text-5xl font-extrabold mb-8">PokemonAPI — Frontend</h1>

                <form onSubmit={onSearch} className="flex gap-2 justify-center">
                    <input
                        className="px-3 py-2 rounded-xl bg-zinc-900/40 border border-zinc-700 focus:outline-none"
                        placeholder="Type a Pokémon (e.g., pikachu)"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                    <button
                        disabled={status === "loading"}
                        className="px-4 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50"
                    >
                        {status === "loading" ? "Searching…" : "Search"}
                    </button>
                </form>

                {status === "loading" && <p className="mt-4">Loading…</p>}
                {status === "error" && <p className="mt-4 text-red-400">Error: {error}</p>}
                <PokemonCard p={data} />
            </div>
        </div>
    );
}