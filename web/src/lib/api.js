// src/lib/api.js
// The destination. If you change your backend host, this is the ONLY line you update.
export const API_BASE = "https://pokemon-backend-wvbb.onrender.com"; // your Render URL

export async function apiGet(path) {
    const res = await fetch(`${API_BASE}${path}`);
    // Check if the server returned a 200-range status code
    if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try { // Attempt to extract the specific error message from FastAPI
            const body = await res.json();
            if (body?.detail) msg = body.detail;
        } catch {
            // If the body isn't JSON, we fall back to the "HTTP 404" style message
        }
        throw new Error(msg); // This explodes so the .jsx catch block can see it
    }
    return res.json();
}

export async function fetchPokemon(name) {
    // Input Validation: Clean up the user's messy typing
    const q = (name || "").trim();
    if (!q) throw new Error("Please enter a Pokémon name.");
    return apiGet(`/api/pokemon/${encodeURIComponent(q)}`);
}