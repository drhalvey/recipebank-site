import os, pathlib
SITE = pathlib.Path(__file__).resolve().parent.parent
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Special+Elite&display=swap" rel="stylesheet">'

GA = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-C3EH7R542Y"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-C3EH7R542Y');</script>"""

def head(title, desc, extra="", analytics=True):
    return f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
{GA if analytics else ""}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://recipebank.app/assets/og.jpg">
<meta name="theme-color" content="#EFE5D3">
<link rel="icon" href="/assets/icon-64.png">
<link rel="apple-touch-icon" href="/assets/icon-180.png">
{FONTS}
<link rel="stylesheet" href="/assets/site.css?v=3">
{extra}
</head>
<body>
'''

TOP = '''<header class="top"><div class="wrap">
<a class="brand" href="/"><img src="/assets/icon-64.png" alt="">Recipe Bank</a>
<nav><a class="hide-sm" href="/#features">Features</a><a class="hide-sm" href="/my/">Web version</a><a href="/support/">Help</a></nav>
</div></header>
'''
FOOT = '''<footer><div class="wrap">
<span>© 2026 Edward Halvey, Perth, Western Australia</span>
<a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/support/">Support</a><a href="mailto:hello@recipebank.app">hello@recipebank.app</a>
</div></footer>
'''

def page(path, title, desc, body, extra_head="", scripts="", top=True, foot=True, analytics=True):
    p = SITE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(head(title, desc, extra_head, analytics) + (TOP if top else "") + body + (FOOT if foot else "") + scripts + "\n</body>\n</html>\n")

polaroid = lambda f, cap, cls="": f'<figure class="polaroid tape {cls}"><img src="/assets/food/{f}.jpg" alt="{cap}" loading="lazy" width="800" height="800"><figcaption>{cap}</figcaption></figure>'
card = lambda n, t, d: f'<article class="icard"><span class="no">No. {n}</span><h3>{t}</h3><p>{d}</p></article>'
shot = lambda f, cap: f'<figure class="print tape"><img src="/assets/shots/{f}.jpg" alt="{cap}" loading="lazy" width="600" height="1303"><figcaption>{cap}</figcaption></figure>'
ARROW = '<svg class="arrow" viewBox="0 0 120 70" aria-hidden="true"><path d="M4 8 C 40 4, 78 18, 96 50" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/><path d="M84 46 L97 53 L100 38" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ---------- Landing ----------
page("index.html", "Recipe Bank: every recipe you love, in one place",
 "Save recipes from any website, video, screenshot or message. Swap ingredients, make any recipe dairy-free or high protein, cook hands-free and shop at Coles or Woolworths.",
f'''<main class="scrap">
<section class="s-hero"><div class="wrap">
  <div class="s-hero-text">
    <h1>Every recipe you love, <span class="scribble">in one tin.</span></h1>
    <p class="lead">The screenshot of that TikTok pasta. Nan's banana bread. The curry off the back of the packet. Recipe Bank reads them all and writes them out as clean, simple recipes you can scale, swap, cook hands-free and shop for.</p>
    <div class="cta">
      <a class="stamp-btn" href="mailto:hello@recipebank.app?subject=Recipe%20Bank%20early%20access">Get early access</a>
      <span class="aside">{ARROW}free for iPhone,<br>no ads, no account</span>
    </div>
  </div>
  <div class="collage" aria-hidden="true">
    {polaroid("ragu", "Sunday ragu", "c1")}
    {polaroid("bananabread", "Nan's banana bread", "c2")}
    <div class="print tape c3"><img src="/assets/shots/recipe.jpg" alt="" width="600" height="1303"></div>
    <div class="sticky c4"><b>Saved this week</b><span>✓ that TikTok pasta</span><span>✓ Nan's banana bread</span><span>✓ pumpkin soup (no cream!)</span><span>✓ the good cookies</span></div>
  </div>
</div></section>

<section class="s-tin" id="features"><div class="wrap">
  <h2 class="hand">What's in the tin</h2>
  <div class="icards">
    {card(1, "Save it from anywhere", "A website, a YouTube video, an Instagram, TikTok or Facebook post, a screenshot or a photo of a cookbook page. No ads, no life story, just the recipe.")}
    {card(2, "Swap anything", "Out of buttermilk? Allergic to nuts? Coriander haters at the table? Tap the ingredient. The method and the nutrition change with it.")}
    {card(3, "Make it…", "Dairy-free, gluten-free, high protein, keto, vegan, kid-friendly, cheaper or quicker, in one tap. Every change is listed so nothing sneaks past you.")}
    {card(4, "Cook hands-free", "Big steps, read aloud. Say 'next', 'back' or 'repeat' with flour on your hands. The timers start themselves.")}
    {card(5, "Shop for it", "A list of what to actually buy, with a rough cost, then your Coles or Woolworths trolley right inside the app.")}
    {card(6, "Ideas when you're stuck", "Chicken, spinach and feta? Photograph the fridge, or pick an occasion: kids' party, staff morning tea, a quiet night in.")}
  </div>
</div></section>

<section class="s-dinner"><div class="wrap">
  <div class="dinner-photos" aria-hidden="true">
    {polaroid("potato", "loaded potatoes", "d1")}
    {polaroid("chicken", "lemon chicken", "d2")}
    {polaroid("salad", "peach & burrata", "d3")}
  </div>
  <div class="dinner-card">
    <h2 class="hand">Three dishes, one dinner time.</h2>
    <p>Pick what's for dinner and when you want to eat. Recipe Bank works backwards and hands you one plan, so nothing's cold and nothing's waiting.</p>
    <ol class="plan">
      <li><time>5:15</time>Potatoes into a 200°C oven</li>
      <li><time>5:35</time>Chicken tray in alongside</li>
      <li><time>6:10</time>Make the salad, crisp the bacon</li>
      <li><time>6:20</time>Chicken out to rest, load the potatoes</li>
      <li><time>6:30</time><b>Dinner</b></li>
    </ol>
  </div>
</div></section>

<section class="s-peek"><div class="wrap">
  <h2 class="hand">A peek inside</h2>
  <div class="prints">
    {shot("list", "all your recipes")}
    {shot("recipe", "tidied up, no ads")}
    {shot("swap", "swap any ingredient")}
    {shot("adapt", "make it dairy-free")}
    {shot("cook", "hands-free cooking")}
    {shot("ideas", "ideas for any occasion")}
    {shot("shopping", "the shopping, sorted")}
    {shot("nutrition", "nutrition per serve")}
  </div>
</div></section>

<section class="s-more"><div class="wrap">
  <div class="notebook">
    <h2 class="hand">Also in the tin</h2>
    <ul>
      <li><b>Nutrition per serve</b>, updated when you swap, and one tap to log a meal to Apple Health.</li>
      <li><b>Translate</b> a whole recipe, units and all, for family in Poland, Italy, Greece or China.</li>
      <li><b>Share a recipe</b> as a link anyone can open, with or without the app.</li>
      <li><b>On the laptop too.</b> Turn on the web version and cook from the kitchen iPad: search, scale, print, timers. It's a private link, and turning it off deletes the copy.</li>
    </ul>
  </div>
  {polaroid("soup", "pumpkin soup, dairy-free", "m1")}
</div></section>

<section class="s-private"><div class="wrap">
  <div class="stamps" aria-hidden="true"><span>No ads</span><span>No account</span><span>Nothing sold</span></div>
  <p>Your recipes live on your iPhone. They only leave it when you ask: to read a recipe with AI, to share one, or to switch on the web version. <a href="/privacy/">The privacy policy</a> says exactly how.</p>
  <p><a class="stamp-btn" href="mailto:hello@recipebank.app?subject=Recipe%20Bank%20early%20access">Get early access</a></p>
</div></section>
</main>
''')

# ---------- Privacy ----------
page("privacy/index.html", "Privacy policy · Recipe Bank", "How Recipe Bank handles your recipes and information.", '''<main class="doc"><div class="narrow">
<p class="eyebrow">Privacy policy</p>
<h1>Your recipes are yours.</h1>
<p class="muted">Last updated 30 September 2026</p>
<div class="note"><b>In short:</b> no account, no ads, nothing tracked inside the app, nothing sold. Your recipes are stored on your iPhone. This website counts its visitors with Google Analytics (see below). Information leaves your phone only when you use a feature that needs it, and only for that purpose.</div>

<h2>Who we are</h2>
<p>Recipe Bank is made by Edward Halvey in Perth, Western Australia ("we"). Contact: <a href="mailto:hello@recipebank.app">hello@recipebank.app</a>. We handle personal information in line with the Australian Privacy Principles.</p>

<h2>What stays on your iPhone</h2>
<ul>
<li>Your recipes, photos, categories, shopping list, meal plans, likes and dislikes, and settings. They are kept in the app's own storage and in your normal iPhone backups.</li>
<li>Voice control in cook mode uses Apple's speech recognition, on the device where your iPhone supports it.</li>
</ul>

<h2>What is sent, and why</h2>
<ul>
<li><b>Reading and writing recipes with AI.</b> When you import a recipe, ask for swaps, adapt a recipe, translate it, work out nutrition, get ideas, plan meals, time several dishes or build a shopping list, the text, link or photo you chose is sent to our servers (hosted by Supabase and Cloudflare) and on to Google's Gemini AI to be processed. We do not keep it after the answer comes back. This goes to Google's paid service, which does not use it to train its models. Videos, and requests on the rare days our paid allowance runs out, go to Google's free service, which may use content to improve its products, so please do not put anything private in a recipe.</li>
<li><b>Cover pictures.</b> When a recipe has no photo, its title and main ingredients are sent to Cloudflare's image AI to draw one.</li>
<li><b>Sharing a recipe.</b> When you share a recipe as a link, that recipe (and its photo) is stored on our server for up to two years so the link works. Anyone who has the link can see that recipe.</li>
<li><b>The web version (optional, off unless you turn it on).</b> A copy of your recipes and their photos is stored with Supabase, a cloud database, behind a long private link. Anyone with the link can view your recipes, so share it only with people you trust. Turning the web version off deletes the web copy.</li>
<li><b>Apple Health (optional).</b> When you tap "Log this meal", the nutrition figures for that serve are written to Apple Health. Recipe Bank never reads your health data.</li>
<li><b>Shopping at Coles or Woolworths.</b> Their websites open inside the app. What you do there, including signing in and your trolley, is between you and them under their own privacy policies; we do not see it.</li>
</ul>

<h2>What we collect about you</h2>
<p><b>In the app:</b> nothing that identifies you. Our server counts how many AI requests it handles each day, with a random code for each installation, so it can share the AI fairly and stop abuse. The app has no analytics, advertising identifiers or tracking.</p>
<p><b>On this website:</b> we use Google Analytics to count visits and see which pages are useful: pages viewed, the type of device and browser, the country and city a visit comes from, and how the visitor found the site. Google Analytics sets cookies in your browser to do this. It does not give us your name or contact details, and Google does not store your full IP address. It is switched off on the web version of your recipes (recipebank.app/my/), so your private link and your recipes are never sent to it. You can block these cookies in your browser settings or with <a href="https://tools.google.com/dlpage/gaoptout">Google's opt-out add-on</a>.</p>
<p>We do not sell or share information with anyone except the service providers named above, and only to run those features.</p>

<h2>Children</h2>
<p>Recipe Bank is a general cooking app for adults and families. It is not designed for children to use on their own.</p>

<h2>Your choices</h2>
<ul>
<li>Delete a recipe, or the app, and it is gone from your iPhone.</li>
<li>Turn off the web version in Settings to delete the web copy.</li>
<li>To remove a shared recipe link early, or with any privacy question or complaint, email <a href="mailto:hello@recipebank.app">hello@recipebank.app</a>. If you are not happy with our answer you can contact the Office of the Australian Information Commissioner (oaic.gov.au).</li>
</ul>

<h2>Changes</h2>
<p>If this policy changes we will update this page and the date above.</p>
</div></main>
''')

# ---------- Terms ----------
page("terms/index.html", "Terms of use · Recipe Bank", "The terms for using Recipe Bank.", '''<main class="doc"><div class="narrow">
<p class="eyebrow">Terms of use</p>
<h1>The fine print, kept short.</h1>
<p class="muted">Last updated 30 September 2026</p>

<h2>Using Recipe Bank</h2>
<p>Recipe Bank is free to use for your own cooking. By using the app or this website you agree to these terms. The app is provided by Edward Halvey, Perth, Western Australia.</p>

<h2>AI can get things wrong</h2>
<p>Recipes read, written, adapted, translated or timed by AI, and all nutrition figures and costs, are estimates. Check amounts, cooking times and temperatures as you cook, and make sure meat, poultry, seafood and eggs are cooked safely.</p>

<h2>Allergies and health</h2>
<p>Allergy swaps and "Make it…" versions (for example gluten-free, dairy-free or nut-free) are suggestions, not guarantees. Always read product labels, which may say "may contain". Diet, nutrition and preparation features are general information, not medical advice: if you have a medical condition or are preparing for a procedure, follow the instructions from your doctor, dietitian or hospital first.</p>

<h2>Recipes belong to their creators</h2>
<p>Recipes you save from websites, videos and books remain the work of their authors. Save them for your own use, and share them in a way that respects their authors. Do not use Recipe Bank to republish other people's recipes commercially. If you believe content shared through Recipe Bank infringes your rights, email <a href="mailto:hello@recipebank.app">hello@recipebank.app</a> and we will remove it.</p>

<h2>Shared links and the web version</h2>
<p>You are responsible for what you share. Do not use shared links to distribute anything unlawful or offensive; we may remove such content.</p>

<h2>Shops and other services</h2>
<p>Coles, Woolworths, YouTube, Instagram, TikTok, Facebook, Apple Health and Google are separate services with their own terms. Recipe Bank is not affiliated with or endorsed by them. Prices shown are rough guides, not the shops' prices.</p>

<h2>No warranty</h2>
<p>We work hard to keep Recipe Bank working, but it is provided "as is". To the extent the law allows, we are not liable for any loss arising from using it. Nothing in these terms excludes rights you have under the Australian Consumer Law.</p>

<h2>Changes and law</h2>
<p>We may update these terms; the date above shows the latest version. These terms are governed by the law of Western Australia.</p>
</div></main>
''')

# ---------- Support ----------
page("support/index.html", "Help and support · Recipe Bank", "Answers to common questions about Recipe Bank, and how to get in touch.", '''<main class="doc"><div class="narrow">
<p class="eyebrow">Help</p>
<h1>How can we help?</h1>
<p>Email <a href="mailto:hello@recipebank.app">hello@recipebank.app</a> and a real person will reply, usually within a day or two. Screenshots help.</p>

<h2>Saving recipes</h2>
<p><b>From a website or YouTube:</b> tap Share in Safari or YouTube, choose Recipe Bank, and it opens and reads the recipe. Or copy the link and tap Paste in the app.</p>
<p><b>From Instagram, TikTok or Facebook:</b> share the post to Recipe Bank. The caption is read; if the recipe is only spoken in the video, screen-record it and choose Video in the app.</p>
<p><b>From a cookbook or screenshot:</b> choose Screenshots or Camera. Several screenshots of one recipe can be picked together, in order.</p>

<h2>Swaps and "Make it…"</h2>
<p>Tap any ingredient for swaps. Use "Make it…" on a recipe for dairy-free, gluten-free, high protein and more. You can keep the original and save the new version as a copy.</p>

<h2>Cooking several dishes</h2>
<p>Tap "Cook together" on the Recipes tab (or under any recipe's method), pick the dishes and, if you like, the time you want to eat. Recipe Bank writes one timed plan and opens it in cook mode.</p>

<h2>Shopping at Coles or Woolworths</h2>
<p>Add recipes to the Shopping tab, then tap "Shop at Coles or Woolworths". The shop opens inside the app with your list underneath: add each item, then tap "Added, next". Sign in once and it is the same trolley as in their app. The shops do not let other apps fill the trolley automatically, so this is one tap per item.</p>

<h2>The web version</h2>
<p>In the app, go to Settings, Web version, and turn it on. You get a private link to open your recipes in any browser. Treat the link like a key: anyone who has it can see your recipes. Turning it off deletes the web copy.</p>

<h2>Something says "busy"</h2>
<p>The AI in Recipe Bank is free and shared. At busy times it may take a little longer or ask you to try again in a minute. Everything you have already saved works without it.</p>

<h2>Privacy</h2>
<p>See the <a href="/privacy/">privacy policy</a>. In short: no account, no ads, nothing sold.</p>
</div></main>
''')
print("pages done")

# ---------- Shared recipe: /r/?id=XXXX (and /r/XXXX via 404.html) ----------
SHARED_JS = '''<script src="/assets/rb.js"></script>
<script>
(async () => {
  const el = document.getElementById("app");
  const m = location.pathname.match(/\\/r\\/([A-Za-z0-9]{6,16})\\/?$/);
  const id = new URLSearchParams(location.search).get("id") || (m && m[1]);
  if (!id || !/^[A-Za-z0-9]{6,16}$/.test(id)) { el.innerHTML = '<div class="empty"><h2>Recipe not found</h2><p>This link looks incomplete.</p></div>'; return; }
  try {
    const r = await fetch(RB.API + "/r/" + id);
    if (!r.ok) throw new Error(r.status);
    const file = await r.json();
    const recipe = file.recipe;
    document.title = recipe.title + " · Recipe Bank";
    const img = file.image ? "https://recipe-bank-relay.ejhalvey.workers.dev/r/" + id + ".jpg" : recipe.imageURL;
    RB.render(el, recipe, { image: img,
      extraActions: '<a class="btn ghost" href="recipebank://r/' + id + '">Open in Recipe Bank</a>' });
    const note = document.createElement("div");
    note.className = "narrow";
    note.innerHTML = '<div class="note" style="margin-top:6px"><b>Shared from Recipe Bank.</b> Save recipes from any website, video or screenshot, swap ingredients and cook hands-free. <a href="/">Find out more</a>.</div>';
    el.appendChild(note);
  } catch (e) {
    el.innerHTML = '<div class="empty"><h2>Recipe not found</h2><p>This link has expired or was typed wrongly.</p><p><a class="btn" href="/">About Recipe Bank</a></p></div>';
  }
})();
</script>'''
page("r/index.html", "A recipe shared from Recipe Bank", "A recipe shared from Recipe Bank.", '<main id="app"><div class="empty">Loading the recipe…</div></main>\n', scripts=SHARED_JS)

# 404: GitHub Pages serves this for any unknown path, so /r/XXXX links work too.
page("404.html", "Recipe Bank", "Recipe Bank", '<main id="app"><div class="empty">Loading…</div></main>\n', scripts='''<script>
if (!/^\\/r\\/[A-Za-z0-9]{6,16}\\/?$/.test(location.pathname)) {
  document.getElementById("app").innerHTML = '<div class="empty"><h2>Page not found</h2><p><a class="btn" href="/">Go to Recipe Bank</a></p></div>';
}
</script>
''' + SHARED_JS.replace('(async () => {', '(async () => { if (!/^\\/r\\//.test(location.pathname)) return;'))
print("shared done")

# ---------- Web version: /my/#KEY ----------
MY_JS = '''<script src="/assets/rb.js"></script>
<script>
(() => {
  const app = document.getElementById("app");
  let data = null, key = null, query = "", filter = "all";
  const store = { get(k) { try { return localStorage.getItem(k); } catch { return null; } },
                  set(k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch {} } };

  function askForLink(msg) {
    app.innerHTML = `<div class="narrow doc"><p class="eyebrow">Web version</p><h1>Your recipes, in any browser.</h1>
      ${msg ? `<div class="note">${RB.esc(msg)}</div>` : ""}
      <p class="muted">In the Recipe Bank app, open Settings, then Web version, and turn it on. Open the link it gives you on this computer, or paste it here.</p>
      <form id="f" class="search" style="margin:18px 0"><input id="k" placeholder="Paste your web version link" autocomplete="off"><button class="btn small">Open</button></form>
      <p class="small muted">The link is private: anyone who has it can see your recipes. This browser remembers it until you sign out below.</p></div>`;
    document.getElementById("f").onsubmit = (e) => { e.preventDefault();
      const v = document.getElementById("k").value.trim(); const m = v.match(/[A-Za-z0-9_-]{24,64}$/) || v.match(/#([A-Za-z0-9_-]{24,64})/);
      if (m) location.hash = (m[1] || m[0]); };
  }

  async function load() {
    const h = location.hash.slice(1).split("/");
    key = h[0] || store.get("rb.key");
    if (!key || !/^[A-Za-z0-9_-]{24,64}$/.test(key)) return askForLink();
    if (!data || data.key !== key) {
      app.innerHTML = '<div class="empty">Loading your recipes…</div>';
      try {
        const r = await fetch(RB.API + "/lib/" + key, { cache: "no-store" });
        if (r.status === 404) { store.set("rb.key", null); return askForLink("That link is not active. The web version may have been turned off in the app."); }
        if (!r.ok) throw new Error(r.status);
        data = await r.json(); data.key = key;
        store.set("rb.key", key);
      } catch (e) { app.innerHTML = '<div class="empty"><h2>Could not load your recipes</h2><p>Check the internet connection and try again.</p></div>'; return; }
    }
    const id = h[1];
    const recipe = id && data.recipes.find((x) => x.id === id);
    recipe ? showRecipe(recipe) : showList();
  }

  const imgOf = (r) => r.imageFile ? data.images + r.imageFile : (r.imageURL || null);

  function showList() {
    document.title = (data.name ? data.name + " · " : "") + "Recipe Bank";
    const all = data.recipes.slice().sort((a, b) => (b.added || "").localeCompare(a.added || ""));
    const tags = {};
    all.forEach((r) => (r.tags || []).forEach((t) => tags[t] = (tags[t] || 0) + 1));
    const top = Object.entries(tags).sort((a, b) => b[1] - a[1]).slice(0, 12).map((x) => x[0]);
    app.innerHTML = `<div class="wrap">
      <div class="lib-top"><div><p class="eyebrow">${RB.esc(data.name || "My recipes")}</p><h1 style="margin:0">Recipe Bank</h1>
      <p class="muted small" style="margin:4px 0 0">${all.length} recipe${all.length === 1 ? "" : "s"} · updated ${new Date(data.updated_at).toLocaleString("en-AU", { dateStyle: "medium", timeStyle: "short" })}</p></div></div>
      <div class="lib-top"><label class="search">🔍<input id="q" placeholder="Search recipes or ingredients" value="${RB.esc(query)}"></label></div>
      <div class="chips" id="chips"></div>
      <div class="grid" id="grid"></div>
      <p class="small muted" style="margin-top:36px">Changes are made in the app on your iPhone and appear here a few seconds later. <a href="#" id="out">Forget this link on this browser</a></p>
    </div>`;
    const chips = [["all", "All"], ...(all.some((r) => r.favourite) ? [["fav", "♥ Favourites"]] : []), ...top.map((t) => ["tag:" + t, t[0].toUpperCase() + t.slice(1)])];
    const chipsEl = document.getElementById("chips");
    const draw = () => {
      chipsEl.innerHTML = chips.map(([k, l]) => `<button class="chip ${filter === k ? "on" : ""}" data-f="${RB.esc(k)}">${RB.esc(l)}</button>`).join("");
      const q = query.toLowerCase();
      const shown = all.filter((r) => {
        if (filter === "fav" && !r.favourite) return false;
        if (filter.startsWith("tag:") && !(r.tags || []).includes(filter.slice(4))) return false;
        if (!q) return true;
        const hay = (r.title + " " + (r.tags || []).join(" ") + " " + (r.groups || []).flatMap((g) => g.items || []).map((i) => i.name).join(" ")).toLowerCase();
        return q.split(/\\s+/).every((w) => hay.includes(w));
      });
      document.getElementById("grid").innerHTML = shown.length ? shown.map((r) => {
        const t = (r.prepMinutes || 0) + (r.cookMinutes || 0); const img = imgOf(r);
        return `<a class="tile" href="#${key}/${r.id}"><div class="img">${img ? `<img src="${RB.esc(img)}" alt="" loading="lazy">` : RB.emoji(r)}</div>
          <h3>${RB.esc(r.title)}</h3><div class="muted">${[t ? RB.mins(t) : "", r.favourite ? "♥" : ""].filter(Boolean).join(" · ")}</div></a>`;
      }).join("") : '<div class="empty">Nothing matches that.</div>';
    };
    chipsEl.onclick = (e) => { const b = e.target.closest("[data-f]"); if (b) { filter = b.dataset.f; draw(); } };
    document.getElementById("q").oninput = (e) => { query = e.target.value; draw(); };
    document.getElementById("out").onclick = (e) => { e.preventDefault(); store.set("rb.key", null); data = null; location.hash = ""; askForLink(); };
    draw();
    window.scrollTo(0, 0);
  }

  function showRecipe(r) {
    document.title = r.title + " · Recipe Bank";
    RB.render(app, r, { image: imgOf(r), back: "All recipes", onBack: () => { location.hash = key; } });
    window.scrollTo(0, 0);
  }

  window.addEventListener("hashchange", load);
  load();
})();
</script>'''
page("my/index.html", "My recipes · Recipe Bank", "Your Recipe Bank recipes in the browser.",
     '<main id="app"><div class="empty">Loading…</div></main>\n', extra_head='<meta name="robots" content="noindex">', scripts=MY_JS, analytics=False)

# ---------- Plumbing ----------
(SITE / "CNAME").write_text("recipebank.app\n")
(SITE / ".nojekyll").write_text("")
wk = SITE / ".well-known"; wk.mkdir(exist_ok=True)
aasa = '{"applinks":{"details":[{"appIDs":["7Q53G3JR9B.au.com.drhalvey.recipes"],"components":[{"/":"/r/*","comment":"Shared recipes"}]}]}}\n'
(wk / "apple-app-site-association").write_text(aasa)
(SITE / "robots.txt").write_text("User-agent: *\nDisallow: /my/\nDisallow: /r/\nSitemap: https://recipebank.app/sitemap.xml\n")
(SITE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  "".join(f"<url><loc>https://recipebank.app{p}</loc></url>\n" for p in ["/", "/privacy/", "/terms/", "/support/"]) + "</urlset>\n")
print("my + plumbing done")
