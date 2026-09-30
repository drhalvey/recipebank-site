// Recipe Bank web backend: the web version's private library links, and shared recipes for recipebank.app.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const SB_URL = Deno.env.get("SUPABASE_URL")!;
const SB_SERVICE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const H = { apikey: SB_SERVICE, Authorization: `Bearer ${SB_SERVICE}` };
const APP_TOKEN = "rbw_Hwpr6HqA6lFiDScFXYy0Jl7vlmUPDbpo";      // low value; the write key protects each library
const RELAY = "https://recipe-bank-relay.ejhalvey.workers.dev";
const BUCKET = "recipebank";
const KEY_RE = /^[A-Za-z0-9_-]{24,64}$/;

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, PUT, DELETE, OPTIONS",
  "access-control-allow-headers": "content-type, x-app-token, x-write-key",
};
function json(status: number, body: unknown, extra: Record<string, string> = {}) {
  return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", ...CORS, ...extra } });
}
async function sha256(s: string) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(d)).map((b) => b.toString(16).padStart(2, "0")).join("");
}
async function row(key: string) {
  const r = await fetch(`${SB_URL}/rest/v1/recipebank_libraries?key=eq.${key}&select=*`, { headers: H });
  const a = await r.json();
  return Array.isArray(a) && a.length ? a[0] : null;
}
async function authorised(req: Request, key: string, existing: any) {
  if (req.headers.get("x-app-token") !== APP_TOKEN) return false;
  const wk = req.headers.get("x-write-key") ?? "";
  if (wk.length < 24) return false;
  return !existing || existing.write_hash === await sha256(wk);
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  const url = new URL(req.url);
  const parts = url.pathname.split("/").filter(Boolean);
  const i = parts.indexOf("recipebank");
  const p = i >= 0 ? parts.slice(i + 1) : parts;

  if (p.length === 0 || p[0] === "health") return json(200, { ok: true, service: "recipebank" });

  // A recipe someone shared: the data lives on the Recipe Bank relay; passed through so the website can read it.
  if (p[0] === "r" && p[1] && /^[A-Za-z0-9]{6,16}$/.test(p[1]) && req.method === "GET") {
    const r = await fetch(`${RELAY}/r/${p[1]}.json`);
    if (!r.ok) return json(r.status === 404 ? 404 : 502, { error: "not found" });
    return new Response(await r.text(), { status: 200, headers: { "content-type": "application/json", "cache-control": "public, max-age=60", ...CORS } });
  }

  if (p[0] !== "lib" || !p[1] || !KEY_RE.test(p[1])) return json(404, { error: "not found" });
  const key = p[1];

  // Read a library (anyone with the private link).
  if (req.method === "GET" && p.length === 2) {
    const r = await row(key);
    if (!r) return json(404, { error: "not found" });
    return json(200, { name: r.name, updated_at: r.updated_at, recipes: r.recipes,
      images: `${SB_URL}/storage/v1/object/public/${BUCKET}/${key}/` }, { "cache-control": "no-store" });
  }

  const existing = await row(key);
  if (!(await authorised(req, key, existing))) return json(401, { error: "not allowed" });

  // Upload one photo.
  if (req.method === "PUT" && p[2] === "img" && p[3] && /^[A-Za-z0-9._-]{4,80}\.jpg$/.test(p[3])) {
    if (!existing) return json(409, { error: "save the library first" });
    const body = await req.arrayBuffer();
    if (body.byteLength > 2_000_000) return json(413, { error: "too big" });
    const r = await fetch(`${SB_URL}/storage/v1/object/${BUCKET}/${key}/${p[3]}`, {
      method: "POST", headers: { ...H, "content-type": "image/jpeg", "x-upsert": "true", "cache-control": "max-age=31536000" }, body });
    return r.ok ? json(200, { ok: true }) : json(502, { error: "upload failed" });
  }

  // Save the whole library (recipes without photos).
  if (req.method === "PUT" && p.length === 2) {
    const text = await req.text();
    if (text.length > 8_000_000) return json(413, { error: "too big" });
    let b: any;
    try { b = JSON.parse(text); } catch { return json(400, { error: "bad json" }); }
    if (!Array.isArray(b?.recipes)) return json(400, { error: "recipes required" });
    const rec = { key, name: String(b.name ?? "").slice(0, 80) || null, recipes: b.recipes, bytes: text.length,
      updated_at: new Date().toISOString(),
      write_hash: existing?.write_hash ?? await sha256(req.headers.get("x-write-key")!) };
    const r = await fetch(`${SB_URL}/rest/v1/recipebank_libraries?on_conflict=key`, {
      method: "POST", headers: { ...H, "content-type": "application/json", Prefer: "resolution=merge-duplicates,return=minimal" },
      body: JSON.stringify(rec) });
    return r.ok ? json(200, { ok: true, count: b.recipes.length }) : json(502, { error: "save failed" });
  }

  // Turn the web version off: remove everything.
  if (req.method === "DELETE" && p.length === 2) {
    if (!existing) return json(200, { ok: true });
    const list = await fetch(`${SB_URL}/storage/v1/object/list/${BUCKET}`, {
      method: "POST", headers: { ...H, "content-type": "application/json" }, body: JSON.stringify({ prefix: key + "/", limit: 1000 }) })
      .then((r) => r.json()).catch(() => []);
    const names = Array.isArray(list) ? list.map((o: any) => `${key}/${o.name}`) : [];
    if (names.length) await fetch(`${SB_URL}/storage/v1/object/${BUCKET}`, {
      method: "DELETE", headers: { ...H, "content-type": "application/json" }, body: JSON.stringify({ prefixes: names }) });
    await fetch(`${SB_URL}/rest/v1/recipebank_libraries?key=eq.${key}`, { method: "DELETE", headers: H });
    return json(200, { ok: true, removed: names.length });
  }

  return json(405, { error: "not allowed" });
});
