// src/lib/api.js
export const API_BASE = "http://127.0.0.1:8000";

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