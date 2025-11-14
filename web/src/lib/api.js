// src/lib/api.js
export const API_BASE = "https://pokemon-backend-wvbb.onrender.com"; // your Render URL

export async function apiGet(path) {
    const res = await fetch(`${API_BASE}${path}`);
    if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try {
            const body = await res.json();
            if (body?.detail) msg = body.detail;
        } catch {}
        throw new Error(msg);
    }
    return res.json();
}

export async function fetchPokemon(name) {
    const q = (name || "").trim();
    if (!q) throw new Error("Please enter a Pokémon name.");
    return apiGet(`/api/pokemon/${encodeURIComponent(q)}`);
}