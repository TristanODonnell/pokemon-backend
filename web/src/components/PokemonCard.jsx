export default function PokemonCard({ p }) {
    // GUARD: If 'p' is undefined/null (no search yet), stop here.
    // This prevents "Cannot read property of undefined" crashes.
    if (!p) return null;

    // ASSET PRIORITY: We prefer the high-quality 'official' art.
	// Using ?. (Optional Chaining) allows us to safely check deep
    // nested objects without a crash if 'sprites' is missing.
    const img =
        p.sprites?.official ||
        p.sprites?.default ||
        null;

    return (
        <div className="mt-8 max-w-md mx-auto p-5 rounded-2xl bg-zinc-900/40 shadow">
            <div className="flex items-center gap-4">
                {img ? (
                    <img
                        src={img}
                        alt={p.name}
                        className="w-24 h-24 object-contain"
                    />
                ) : null}
                <div className="text-left">
                    <h2 className="text-2xl font-semibold capitalize">{p.name}</h2>
                    <p className="text-sm text-zinc-400">ID: {p.id}</p>
                    {p.types?.length ? (
                        <p className="text-sm">Types: {p.types.join(", ")}</p>
                    ) : null}
                    <p className="text-sm">Ht: {p.height}  Wt: {p.weight}</p>
                </div>
            </div>

            {p.description ? (
                <p className="mt-3 text-zinc-300 text-sm leading-6">{p.description}</p>
            ) : null}

            {p.evolution?.stages?.length ? (
                <p className="mt-3 text-zinc-400 text-sm">
                    Evolution path: {p.evolution.stages.join(" → ")}{" "}
                    {typeof p.evolution.current_index === "number"
                        ? `(index ${p.evolution.current_index})`
                        : ""}
                </p>
            ) : null}
        </div>
    );
}
