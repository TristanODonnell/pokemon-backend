// src/components/PokemonSearch.jsx

import { useState } from "react";
import { fetchPokemon } from "../lib/api";

export default function PokemonSearch() {
    // State Management: These track the 'life' of a search request
    const [q, setQ] = useState(""); // The raw user input
    const [card, setCard] = useState(null); // The successful data from backend
    const [loading, setLoading] = useState(false); // UI state for the button
    const [err, setErr] = useState(""); // Error messages (404s, etc.)


    async function onSubmit(e) {
        // Prevent the browser from reloading the page (Standard SPA behavior)
        e.preventDefault();

        // Reset UI state before starting a new search
        setErr(""); setCard(null); setLoading(true); // Prep UI for new request
        try { // The Handshake: Calling our API bridge to talk to the FastAPI backend
            setCard(await fetchPokemon(q)); }
        catch (e) {  // Catching backend/network errors and displaying them to the user
            setErr(e.message || "Something went wrong."); }
        finally { // Ensure the button is re-enabled regardless of success or failure
            setLoading(false); }
    }

    // Asset Selection: Heuristic to find the best image available in the data
    const img = card?.sprite?.official || card?.sprite?.default || "";

    return (
        <div style={{ maxWidth: 720, margin: "2rem auto", padding: "1rem" }}>
            <h1>Pokémon Search</h1>
            <form onSubmit={onSubmit} style={{ display: "flex", gap: 8, marginBottom: 16 }}>
                <input value={q} onChange={(e)=>setQ(e.target.value)} placeholder="e.g. pikachu" style={{flex:1,padding:8}}/>
                <button disabled={loading}>{loading ? "Searching..." : "Search"}</button>
            </form>
            {err && <div style={{ color: "crimson", marginBottom: 12 }}>{err}</div>}
            {card && (
                <article style={{ display:"grid", gridTemplateColumns:"160px 1fr", gap:16, border:"1px solid #ddd", borderRadius:12, padding:16 }}>
                    <div style={{ textAlign:"center" }}>
                        {img ? <img src={img} alt={card.name} width={140} height={140}/> : <div style={{width:140,height:140,background:"#eee"}}/>}
                    </div>
                    <div>
                        <h2 style={{ textTransform:"capitalize", margin:0 }}>
                            {card.name} <small style={{ color:"#777" }}>#{card.id}</small>
                        </h2>
                        <p style={{ margin:"4px 0 8px" }}>Types: {card.types?.join(", ") || "—"}</p>
                        <p style={{ margin:"0 0 8px" }}>{card.description || "No description available."}</p>
                        <p style={{ margin:0, color:"#666", fontSize:14 }}>Ht: {card.height} • Wt: {card.weight}</p>
                    </div>
                </article>
            )}
        </div>
    );
}
