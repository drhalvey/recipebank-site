// Recipe Bank on the web: shows a recipe (shared link or your own library) with serves, ticking and cook mode.
const RB = (() => {
  const API = "https://bbwjroytqxynborrqylr.supabase.co/functions/v1/recipebank";
  const PLURALS = { cup: "cups", clove: "cloves", can: "cans", tin: "tins", jar: "jars", bunch: "bunches", sprig: "sprigs",
    handful: "handfuls", slice: "slices", piece: "pieces", stick: "sticks", packet: "packets", sheet: "sheets", stalk: "stalks",
    head: "heads", fillet: "fillets", rasher: "rashers", knob: "knobs", pinch: "pinches", dash: "dashes", punnet: "punnets",
    sachet: "sachets", bottle: "bottles", bag: "bags", block: "blocks", drop: "drops", leaf: "leaves", pint: "pints", quart: "quarts" };
  const LABELS = { l: "L", floz: "fl oz", ml: "mL" };
  const FRACS = [[0, ""], [1 / 8, "⅛"], [1 / 4, "¼"], [1 / 3, "⅓"], [1 / 2, "½"], [2 / 3, "⅔"], [3 / 4, "¾"], [1, ""]];

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  function num(x) {
    if (!isFinite(x) || x <= 0) return "";
    let w = Math.floor(x); const f = x - w;
    let best = FRACS[0], d = 9;
    for (const fr of FRACS) { const e = Math.abs(fr[0] - f); if (e < d) { d = e; best = fr; } }
    if (d > 0.05) return x >= 10 ? String(Math.round(x)) : String(Math.round(x * 10) / 10);
    if (best[0] === 1) { w += 1; best = [0, ""]; }
    return w === 0 ? (best[1] || "0") : `${w}${best[1]}`;
  }
  function unitLabel(u, q) {
    if (!u) return "";
    if (LABELS[u]) return LABELS[u];
    return q > 1 && PLURALS[u] ? PLURALS[u] : u;
  }
  function amount(i, scale) {
    if (i.quantity == null) return "";
    const q = i.quantity * scale;
    let s = num(q);
    if (i.quantityMax != null) s += "–" + num(i.quantityMax * scale);
    // 1250 g reads better as 1.25 kg
    let u = i.unit || "";
    if (u === "g" && q >= 1000 && i.quantityMax == null) { s = num(q / 1000); u = "kg"; }
    if (u === "ml" && q >= 1000 && i.quantityMax == null) { s = num(q / 1000); u = "l"; }
    return (s + " " + unitLabel(u, q)).trim();
  }
  function mins(m) {
    if (!m) return "";
    const h = Math.floor(m / 60), r = m % 60;
    return h ? `${h} h${r ? " " + r + " min" : ""}` : `${m} min`;
  }
  const EMOJI = [["breakfast|pancake|waffle|egg", "🥞"], ["cookie|biscuit", "🍪"], ["cake|muffin|brownie|slice|dessert|baking", "🍰"], ["soup", "🍲"], ["salad", "🥗"], ["pasta|spaghetti|noodle", "🍝"],
    ["chicken", "🍗"], ["beef|steak|lamb|pork|mince", "🥩"], ["fish|salmon|prawn|seafood", "🐟"], ["curry", "🍛"], ["bread", "🍞"]];
  function emoji(r) {
    const t = (r.title + " " + (r.tags || []).join(" ")).toLowerCase();
    for (const [re, e] of EMOJI) if (new RegExp(re).test(t)) return e;
    return "🍽️";
  }

  // Times in a step become timers: "simmer 20 minutes", "1 1/2 hours", "1 hour 30 minutes".
  function timers(text) {
    const out = [];
    const re = /(?<![\w\/.])(\d+\s+\d+\/\d+|\d+\/\d+|\d+(?:\.\d+)?|an?|one|two|three|four|five|ten|fifteen|twenty|thirty|forty|forty-five)(?:\s*(?:-|–|to|or)\s*(\d+(?:\.\d+)?))?\s*(hours?|hrs?|minutes?|mins?|seconds?|secs?)\b(?:\s*(?:and\s*)?(\d+)\s*(?:minutes?|mins?)\b)?/gi;
    const words = { a: 1, an: 1, one: 1, two: 2, three: 3, four: 4, five: 5, ten: 10, fifteen: 15, twenty: 20, thirty: 30, forty: 40, "forty-five": 45 };
    const parse = (s) => { let t = 0; for (const p of s.trim().split(/\s+/)) { if (p.includes("/")) { const [a, b] = p.split("/"); t += (+a) / (+b); } else t += +p; } return t; };
    for (const m of text.replace(/½/g, " 1/2").replace(/¼/g, " 1/4").replace(/¾/g, " 3/4").matchAll(re)) {
      const n = words[m[1].toLowerCase()] ?? parse(m[1]);
      const u = m[3].toLowerCase();
      let secs = n * (u.startsWith("h") ? 3600 : u.startsWith("s") ? 1 : 60);
      if (u.startsWith("h") && m[4]) secs += (+m[4]) * 60;
      if (secs >= 10 && secs <= 86400 && !out.find((x) => x.label === m[0].trim())) out.push({ label: m[0].trim(), secs: Math.round(secs) });
    }
    return out;
  }
  const clock = (s) => { s = Math.max(0, s); const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), r = s % 60;
    return h ? `${h}:${String(m).padStart(2, "0")}:${String(r).padStart(2, "0")}` : `${m}:${String(r).padStart(2, "0")}`; };

  /// Renders a recipe into `el`. opts: { image, back, extraActions }
  function render(el, r, opts = {}) {
    const base = r.servings > 0 ? r.servings : 4;
    let serves = base;
    const ticked = new Set();
    const img = opts.image || r.imageURL;
    el.innerHTML = `
      <div class="recipe-hero">${img ? `<img src="${esc(img)}" alt="">` : `<div class="ph">${emoji(r)}</div>`}</div>
      <div class="recipe-body">
        ${opts.back ? `<button class="back" data-back>‹ ${esc(opts.back)}</button>` : ""}
        ${(r.tags || []).length ? `<p class="eyebrow">${esc(r.tags.slice(0, 3).join(" · "))}</p>` : ""}
        <h1>${esc(r.title)}</h1>
        <div class="meta">
          ${r.prepMinutes ? `<span>Prep <b>${mins(r.prepMinutes)}</b></span>` : ""}
          ${r.cookMinutes ? `<span>Cook <b>${mins(r.cookMinutes)}</b></span>` : ""}
          ${r.servingsLabel ? `<span><b>${esc(r.servingsLabel)}</b></span>` : ""}
          ${r.sourceURL ? `<span><a href="${esc(r.sourceURL)}" target="_blank" rel="noopener">Original recipe</a></span>` : ""}
        </div>
        <div class="actions">
          ${(r.steps || []).length ? `<button class="btn" data-cook>Start cooking</button>` : ""}
          <button class="btn soft" data-print>Print</button>
          ${opts.extraActions || ""}
        </div>
        <div class="card">
          <h2>Ingredients <span class="stepper"><button data-less aria-label="Fewer serves">−</button><span data-serves></span><button data-more aria-label="More serves">+</button></span></h2>
          <div data-ings></div>
        </div>
        ${r.nutrition && r.nutrition.kcal ? `<div class="card"><h2>Nutrition <small class="muted small" style="font-family:var(--sans)">PER SERVE, ESTIMATED</small></h2>
          <div class="nut"><div><b>${Math.round(r.nutrition.kcal)}</b><small>kcal</small></div><div><b>${Math.round(r.nutrition.protein || 0)} g</b><small>protein</small></div>
          <div><b>${Math.round(r.nutrition.carbs || 0)} g</b><small>carbs</small></div><div><b>${Math.round(r.nutrition.fat || 0)} g</b><small>fat</small></div></div></div>` : ""}
        ${(r.steps || []).length ? `<div class="card"><h2>Method</h2><ol class="steps">${r.steps.map((s) => `<li>${esc(s.text)}</li>`).join("")}</ol></div>` : ""}
        ${r.notes ? `<div class="card"><h2>Notes</h2><p style="white-space:pre-line">${esc(r.notes)}</p></div>` : ""}
      </div>
      <div class="cook" data-cookpane></div>`;

    const ingsEl = el.querySelector("[data-ings]");
    function drawIngs() {
      el.querySelector("[data-serves]").textContent = r.servingsLabel ? `${num(serves / base)} batch${serves === base ? "" : "es"}` : `${num(serves)} serve${serves === 1 ? "" : "s"}`;
      const scale = serves / base;
      ingsEl.innerHTML = (r.groups || []).map((g, gi) => `
        ${g.name ? `<div class="group-name">${esc(g.name)}</div>` : ""}
        <ul class="ings">${(g.items || []).map((i, ii) => {
          const k = gi + ":" + ii, a = amount(i, scale);
          return `<li data-k="${k}" class="${ticked.has(k) ? "done" : ""}"><span class="tick"></span><span>${a ? `<span class="amt">${esc(a)}</span> ` : ""}${esc(i.name)}${i.preparation ? `<span class="prep">, ${esc(i.preparation)}</span>` : ""}${i.optional ? `<span class="prep"> (optional)</span>` : ""}</span></li>`;
        }).join("")}</ul>`).join("");
    }
    ingsEl.addEventListener("click", (e) => {
      const li = e.target.closest("li[data-k]"); if (!li) return;
      const k = li.dataset.k; ticked.has(k) ? ticked.delete(k) : ticked.add(k); li.classList.toggle("done");
    });
    const stepBy = r.servingsLabel ? base / 2 : 1;   // "24 cookies" goes up and down in half batches
    el.querySelector("[data-less]").onclick = () => { serves = Math.max(stepBy, serves - stepBy); drawIngs(); };
    el.querySelector("[data-more]").onclick = () => { serves = Math.min(base * 20, serves + stepBy); drawIngs(); };
    el.querySelector("[data-print]").onclick = () => window.print();
    const back = el.querySelector("[data-back]"); if (back && opts.onBack) back.onclick = opts.onBack;
    const cookBtn = el.querySelector("[data-cook]"); if (cookBtn) cookBtn.onclick = () => cook(el.querySelector("[data-cookpane]"), r, serves / base);
    drawIngs();
  }

  // One step at a time, big text, timers you tap to start, screen kept awake.
  function cook(pane, r, scale) {
    const pages = ["ingredients", ...r.steps.map((s) => s.text)];
    let page = 0, lock = null;
    const running = {};
    try { navigator.wakeLock?.request("screen").then((l) => lock = l).catch(() => {}); } catch {}
    pane.classList.add("on");
    document.body.style.overflow = "hidden";
    function close() { pane.classList.remove("on"); document.body.style.overflow = ""; try { lock?.release(); } catch {} clearInterval(ticker); }
    function draw() {
      const p = pages[page];
      const body = page === 0
        ? `<div class="num">Get everything out</div><ul class="ings" style="margin-top:14px">${(r.groups || []).flatMap((g) => g.items || []).map((i) => {
            const a = amount(i, scale); return `<li><span class="tick"></span><span>${a ? `<span class="amt">${esc(a)}</span> ` : ""}${esc(i.name)}</span></li>`; }).join("")}</ul>`
        : `<div class="num">Step ${page} of ${pages.length - 1}</div><p class="big">${esc(p)}</p>
           <div class="timers">${timers(p).map((t) => `<button class="timer" data-t="${t.secs}" data-l="${esc(t.label)}">⏱ ${esc(t.label)}</button>`).join("")}</div>`;
      pane.innerHTML = `<header><span class="t">${esc(r.title)}</span><button class="btn small ghost" data-x>Close</button></header>
        <main>${body}</main>
        <footer><button class="btn soft" data-prev ${page === 0 ? "disabled" : ""}>‹ Back</button>
        <button class="btn" data-next>${page === pages.length - 1 ? "Finish" : page === 0 ? "Start cooking ›" : "Next ›"}</button></footer>`;
      pane.querySelector("[data-x]").onclick = close;
      pane.querySelector("[data-prev]").onclick = () => { if (page > 0) { page--; draw(); } };
      pane.querySelector("[data-next]").onclick = () => { if (page < pages.length - 1) { page++; draw(); } else close(); };
      pane.querySelector("main").addEventListener("click", (e) => {
        const li = e.target.closest(".ings li"); if (li) li.classList.toggle("done");
      });
      pane.querySelectorAll("[data-t]").forEach((b) => {
        const key = page + "|" + b.dataset.l;
        b.dataset.key = key;
        b.onclick = () => {
          if (running[key]) { delete running[key]; b.className = "timer"; b.textContent = `⏱ ${b.dataset.l}`; return; }
          running[key] = { end: Date.now() + (+b.dataset.t) * 1000, label: b.dataset.l }; tick();
        };
      });
      tick();
    }
    // One ticker for every timer, so a timer keeps going (and rings) while you are on another step.
    function tick() {
      for (const [key, t] of Object.entries(running)) {
        const left = Math.round((t.end - Date.now()) / 1000);
        const b = pane.querySelector(`[data-key="${CSS.escape(key)}"]`);
        if (left <= 0) {
          if (!t.rang) { t.rang = true; beep(); if (!b) toast(`Timer done: ${t.label}`); }
          if (b) { b.className = "timer done"; b.textContent = `⏰ ${t.label}: done`; }
        } else if (b) { b.className = "timer running"; b.textContent = `⏱ ${clock(left)}`; }
      }
    }
    const ticker = setInterval(tick, 500);
    function toast(msg) {
      const d = document.createElement("div");
      d.textContent = msg;
      d.style.cssText = "position:fixed;left:50%;top:18px;transform:translateX(-50%);background:var(--accent);color:#fff;padding:12px 18px;border-radius:14px;font-weight:600;z-index:60";
      pane.appendChild(d); setTimeout(() => d.remove(), 6000);
    }
    function beep() {
      try { const c = new (window.AudioContext || window.webkitAudioContext)(); const o = c.createOscillator(); o.frequency.value = 880; o.connect(c.destination); o.start(); setTimeout(() => { o.stop(); c.close(); }, 700); } catch {}
    }
    document.onkeydown = (e) => { if (!pane.classList.contains("on")) return;
      if (e.key === "ArrowRight") pane.querySelector("[data-next]").click();
      if (e.key === "ArrowLeft") pane.querySelector("[data-prev]").click();
      if (e.key === "Escape") close(); };
    draw();
  }

  return { API, esc, render, mins, emoji, num };
})();
