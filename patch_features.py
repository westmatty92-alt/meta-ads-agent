#!/usr/bin/env python3
"""Patch index.html with all 6-part feature additions."""

with open('/home/admin/meta-ads-agent/index.html', 'r') as f:
    html = f.read()

applied = []
missed  = []

def patch(old, new, label, count=1):
    global html
    if old not in html:
        missed.append(label)
        print(f'MISS: {label!r}')
        return
    html = html.replace(old, new, count)
    applied.append(label)
    print(f'OK:   {label}')

# ── PATCH 1: CSS .sname — remove uppercase, weight 700→600 ─────────────────
patch(
    '.sname{font-family:var(--sans);font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
    '.sname{font-family:var(--sans);font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
    'sname CSS'
)

# ── PATCH 2: CSS new component styles ──────────────────────────────────────
NEW_CSS = """\
/* ── Base Profile & Product Cards ── */
.bp-product-card{border:1px solid var(--border2);transition:border-color .2s;}
.bp-product-card:hover{border-color:rgba(0,212,160,.3);}
.bk-palette-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;}
.bk-rm{background:transparent;border:none;color:var(--t2);cursor:pointer;font-size:14px;padding:2px 6px;border-radius:4px;line-height:1;transition:all .15s;}
.bk-rm:hover{color:var(--red);background:rgba(255,80,80,.1);}
.bp-type-btn.active{background:var(--accent)!important;color:#0D1F2D!important;}
"""
patch('</style>', NEW_CSS + '</style>', 'new CSS rules')

# ── PATCH 3: HTML connected-product-pill in panel-data header ──────────────
patch(
    """        <div class="sacts">
          <button class="btn bg bsm" onclick="runQuickHealthCheck()">⚡ Health Check</button>
          <button class="btn bp" onclick="saveData()">Save &amp; Continue →</button>
        </div>
      </div>""",
    """        <div class="sacts" style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
          <button class="btn bg bsm" onclick="runQuickHealthCheck()">⚡ Health Check</button>
          <button class="btn bp" onclick="saveData()">Save &amp; Continue →</button>
          <div id="connected-product-pill" style="display:none;align-items:center;gap:5px;background:rgba(0,212,160,.1);border:1px solid rgba(0,212,160,.3);border-radius:20px;padding:3px 10px;font-size:11px;font-weight:600;font-family:var(--sans);color:#00D4A0;cursor:pointer;white-space:nowrap;" onclick="go('baseProfile')">
            📦 <span id="connected-product-name"></span>&nbsp;<span style="font-size:9px;opacity:.6;">change</span>
          </div>
        </div>
      </div>""",
    'connected-product-pill'
)

# ── PATCH 4: HTML nav-baseProfile after nav-data ───────────────────────────
patch(
    '    <div class="conn" id="conn-1"></div>',
    """    <div class="stage" id="nav-baseProfile" onclick="go('baseProfile')">
      <div class="si">🏢</div>
      <div class="sinfo"><div class="sname">Base Profile</div><div class="sdesc">Business setup</div></div>
      <span class="sbadge br">Setup</span>
    </div>
    <div class="conn" id="conn-1"></div>""",
    'nav-baseProfile',
    1
)

# ── PATCH 5: HTML panel-baseProfile overlay ────────────────────────────────
PANEL_BP = """\
<div class="overlay" id="panel-baseProfile">
  <div class="shdr">
    <div class="shdr-left">
      <h2>🏢 Base Profile</h2>
      <p>Your business identity — feeds every stage automatically</p>
    </div>
    <div class="sacts">
      <button class="btn bp" onclick="saveBaseProfile()">Save Profile</button>
      <button class="btn bg" onclick="go('data')">✕ Close</button>
    </div>
  </div>
  <div class="s1-tabs-bar">
    <button class="s1-tab active" id="bptab-business" onclick="switchBPTab('business')">🏢 Business</button>
    <button class="s1-tab" id="bptab-products" onclick="switchBPTab('products')">📦 Products &amp; Services</button>
    <button class="s1-tab" id="bptab-brand" onclick="switchBPTab('brand')">🎨 Brand Kit</button>
  </div>

  <!-- Tab: Business -->
  <div id="bp-pane-business" class="s1-tab-pane active" style="flex:1;overflow-y:auto;padding:18px 22px;">
    <div class="dgrid">
      <div class="dcard">
        <h3>Business Info</h3>
        <div class="flbl">Business Name</div>
        <input class="fi" id="bp-business-name" placeholder="e.g. Runbase CRM">
        <div class="flbl">Industry</div>
        <select class="fsel" id="bp-industry">
          <option value="fitness">Fitness &amp; Gym</option>
          <option value="beauty">Beauty &amp; Skincare</option>
          <option value="food">Food &amp; Nutrition</option>
          <option value="fashion">Fashion &amp; Apparel</option>
          <option value="tech">Technology</option>
          <option value="saas">SaaS &amp; Software</option>
          <option value="ecommerce">Ecommerce</option>
          <option value="finance">Finance</option>
          <option value="health">Health &amp; Wellness</option>
          <option value="pets">Pets</option>
          <option value="travel">Travel</option>
          <option value="parenting">Parenting</option>
          <option value="real_estate">Real Estate</option>
          <option value="education">Education</option>
          <option value="gaming">Gaming</option>
        </select>
        <div class="flbl">Location</div>
        <input class="fi" id="bp-location" placeholder="e.g. Sydney, Australia">
        <div class="flbl">Website URL</div>
        <input class="fi" id="bp-website" placeholder="https://yourbusiness.com" onblur="scrapeWebsite(this.value)">
        <div class="flbl">Tagline</div>
        <input class="fi" id="bp-tagline" placeholder="e.g. Ads that actually convert">
        <div class="flbl">Mission Statement</div>
        <textarea class="fta" id="bp-mission" placeholder="Your business mission..." style="min-height:60px;"></textarea>
      </div>
      <div class="dcard">
        <h3>Social Links</h3>
        <div class="flbl">Instagram</div>
        <input class="fi" id="bp-instagram" placeholder="https://instagram.com/yourbrand">
        <div class="flbl">Facebook</div>
        <input class="fi" id="bp-facebook" placeholder="https://facebook.com/yourbrand">
        <div class="flbl">TikTok</div>
        <input class="fi" id="bp-tiktok" placeholder="https://tiktok.com/@yourbrand">
        <div class="flbl">LinkedIn</div>
        <input class="fi" id="bp-linkedin" placeholder="https://linkedin.com/company/yourbrand">
        <div class="flbl">YouTube</div>
        <input class="fi" id="bp-youtube" placeholder="https://youtube.com/@yourbrand">
        <button class="btn bp" style="width:100%;margin-top:8px;" onclick="analyzeBrand()">🔍 Analyze Brand</button>
        <div id="bp-brand-snapshot" style="display:none;margin-top:10px;"></div>
      </div>
    </div>
  </div>

  <!-- Tab: Products & Services -->
  <div id="bp-pane-products" class="s1-tab-pane" style="flex:1;overflow-y:auto;padding:18px 22px;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
      <span style="font-size:12px;color:var(--t2);">Add products and services. Connect one to pipeline to scope ads.</span>
      <button class="btn bp bsm" onclick="addProductCard()">+ Add Product / Service</button>
    </div>
    <div id="bp-products-list" style="display:flex;flex-direction:column;gap:12px;"></div>
    <div id="bp-products-empty" style="text-align:center;padding:30px;color:var(--t2);font-size:12px;">No products yet — click "Add Product / Service" to start.</div>
  </div>

  <!-- Tab: Brand Kit -->
  <div id="bp-pane-brand" class="s1-tab-pane" style="flex:1;overflow-y:auto;padding:18px 22px;">
    <div class="dgrid">
      <div class="dcard">
        <h3>Brand Identity</h3>
        <div class="flbl">Brand Name</div>
        <input class="fi" id="bp-brand-name" placeholder="e.g. Runbase">
        <div class="flbl">Font Style</div>
        <select class="fsel" id="bk-font">
          <option value="Modern">Modern</option>
          <option value="Classic">Classic</option>
          <option value="Bold">Bold</option>
          <option value="Playful">Playful</option>
          <option value="Minimal">Minimal</option>
        </select>
        <div class="flbl">Brand Voice / Vibe</div>
        <input class="fi" id="bp-brand-vibe" placeholder="e.g. energetic, bold, direct">
        <div class="flbl">Logo (PNG, SVG, JPG)</div>
        <div class="drop" style="padding:14px;" onclick="document.getElementById('bp-logo-upload').click()">
          <div class="drop-ic" style="font-size:20px;">🖼</div>
          <h4>Upload Logo</h4><p>Click to select file</p>
        </div>
        <input type="file" id="bp-logo-upload" accept=".png,.svg,.jpg,.jpeg" style="display:none;" onchange="handleLogoUpload(event)">
      </div>
      <div class="dcard">
        <h3>Brand Colors</h3>
        <div class="bk-palette-hdr">
          <div class="flbl" style="margin:0;">Color Palette</div>
          <button class="btn bg bsm" onclick="addBkColor()">+ Add Color</button>
        </div>
        <div id="bk-palette" style="margin-top:8px;"></div>
        <div style="margin-top:16px;">
          <div class="flbl">Primary Color Preview</div>
          <div id="bp-color-preview" style="width:100%;height:48px;border-radius:8px;background:var(--accent);border:1px solid var(--border2);margin-top:4px;"></div>
        </div>
      </div>
    </div>
  </div>
</div>
"""
patch(
    '<div class="overlay" id="panel-autoResearch">',
    PANEL_BP + '<div class="overlay" id="panel-autoResearch">',
    'panel-baseProfile HTML',
    1
)

# ── PATCH 6: HTML product filter dropdown in Ad Library ────────────────────
patch(
    """      <div class="adlib-tabs">
        <button class="adlib-tab active" id="tab-ads" onclick="switchAdlibTab('ads')">📚 Saved Ads</button>
        <button class="adlib-tab" id="tab-perf" onclick="switchAdlibTab('perf')">📊 Performance History</button>
      </div>""",
    """      <div class="adlib-tabs" style="display:flex;align-items:center;">
        <button class="adlib-tab active" id="tab-ads" onclick="switchAdlibTab('ads')">📚 Saved Ads</button>
        <button class="adlib-tab" id="tab-perf" onclick="switchAdlibTab('perf')">📊 Performance History</button>
        <div style="margin-left:auto;padding:0 14px;">
          <select id="adlib-product-filter" class="fsel" style="margin:0;font-size:11px;padding:3px 8px;" onchange="filterAdsByProduct(this.value)">
            <option value="">All Products</option>
          </select>
        </div>
      </div>""",
    'adlib product filter'
)

# ── PATCH 7: HTML product selector in Auto-Research panel ──────────────────
patch(
    """      <div class="ar-section">
        <h4>Competitors to Scrape</h4>
        <input class="fi" id="ar-competitors" placeholder="e.g. Gymshark, Huel, Athletic Greens">
      </div>""",
    """      <div class="ar-section">
        <h4>Product Focus (optional)</h4>
        <select class="fsel" id="ar-product-select" style="margin-bottom:0;" onchange="connectProductFromResearch(this.value)">
          <option value="">Select product to research (optional)</option>
        </select>
      </div>
      <div class="ar-section">
        <h4>Competitors to Scrape</h4>
        <input class="fi" id="ar-competitors" placeholder="e.g. Gymshark, Huel, Athletic Greens">
      </div>""",
    'ar product selector'
)

# ── PATCH 8: JS SQL comments before SUPA_URL ───────────────────────────────
SQL_COMMENTS = """\
// ── Product & Base Profile Schema ────────────────────────────────────────────
// Run once in Supabase SQL Editor to enable product-scoped storage.
//
// CREATE TABLE IF NOT EXISTS products (
//   id             uuid default gen_random_uuid() primary key,
//   business_id    uuid references businesses(id) on delete cascade,
//   user_id        uuid references auth.users(id) on delete cascade,
//   name           text,
//   type           text default 'product',
//   price          text,
//   description    text,
//   url            text,
//   storage_folder text,
//   created_at     timestamp with time zone default timezone('utc'::text, now())
// );
// ALTER TABLE products ENABLE ROW LEVEL SECURITY;
// CREATE POLICY "Users see own products" ON products FOR ALL USING (auth.uid() = user_id);
//
// ALTER TABLE generated_ads ADD COLUMN IF NOT EXISTS product_id uuid references products(id);
// ALTER TABLE ad_performance ADD COLUMN IF NOT EXISTS product_id uuid references products(id);
//
// CREATE TABLE IF NOT EXISTS base_profiles (
//   id             uuid default gen_random_uuid() primary key,
//   business_id    uuid references businesses(id) on delete cascade,
//   user_id        uuid references auth.users(id) on delete cascade,
//   business_name  text, industry text, location text, website text,
//   tagline        text, mission text, instagram text, facebook text,
//   tiktok         text, linkedin text, youtube text,
//   brand_snapshot jsonb,
//   updated_at     timestamp with time zone default timezone('utc'::text, now())
// );
// ALTER TABLE base_profiles ENABLE ROW LEVEL SECURITY;
// CREATE POLICY "Users see own base profiles" ON base_profiles FOR ALL USING (auth.uid() = user_id);
//
"""
patch('const SUPA_URL =', SQL_COMMENTS + 'const SUPA_URL =', 'SQL schema comments', 1)

# ── PATCH 9: STATE object — add currentProductId, products ─────────────────
patch(
    '  stagesDone: new Set(), targetCpa:null, targetRoas:null\n};',
    '  stagesDone: new Set(), targetCpa:null, targetRoas:null,\n  currentProductId: null, products: []\n};',
    'STATE additions'
)

# ── PATCH 10: STATE fallback reset — same fields ───────────────────────────
patch(
    'stagesDone: new Set(), targetCpa:null, targetRoas:null }; renderBkPalette(); return; }',
    'stagesDone: new Set(), targetCpa:null, targetRoas:null, currentProductId: null, products: [] }; renderBkPalette(); return; }',
    'STATE fallback additions'
)

# ── PATCH 11: go() — add baseProfile to overlays ──────────────────────────
patch(
    "  const overlays = ['settings','autoResearch'];",
    "  const overlays = ['settings','autoResearch','baseProfile'];",
    "go() overlays array"
)

# ── PATCH 12: go() — call loadBaseProfile ─────────────────────────────────
patch(
    "    if(name==='settings'){ populateKeyInputs(); loadKeys().then(()=>populateKeyInputs()); }",
    "    if(name==='settings'){ populateKeyInputs(); loadKeys().then(()=>populateKeyInputs()); }\n    if(name==='baseProfile'){ loadBaseProfile(); }",
    "go() loadBaseProfile call"
)

# ── PATCH 13: saveToAdLibrary() — add product_id ──────────────────────────
patch(
    "    niche:          S.niche             || ''\n  }).select().single();",
    "    niche:          S.niche             || '',\n    product_id:     S.currentProductId  || null\n  }).select().single();",
    "saveToAdLibrary product_id"
)

# ── PATCH 14: renderAdLibrary — add data-product-id attr ──────────────────
patch(
    '    return `<div class="adlib-card">',
    """    return `<div class="adlib-card" data-product-id="${ad.product_id||''}">""",
    "renderAdLibrary data-product-id"
)

# ── PATCH 15: loadAdLibrary — populate product dropdowns ──────────────────
patch(
    '  adLibrary = data || [];\n  updateAdLibBadge();\n}',
    '  adLibrary = data || [];\n  updateAdLibBadge();\n  populateProductDropdowns();\n}',
    "loadAdLibrary populate dropdowns"
)

# ── PATCH 16: All new JS functions ─────────────────────────────────────────
NEW_JS = r"""
// ── Base Profile ─────────────────────────────────────────────────────────

function switchBPTab(tab) {
  ['business','products','brand'].forEach(t => {
    const pane = document.getElementById('bp-pane-' + t);
    const btn  = document.getElementById('bptab-' + t);
    if (pane) pane.classList.toggle('active', t === tab);
    if (btn)  btn.classList.toggle('active',  t === tab);
  });
}

async function scrapeWebsite(url) {
  if (!url || !url.startsWith('http')) return;
  setSt('Scraping website…', 'run');
  try {
    const result = await ai(
      'You are a web data extractor. Return only valid JSON — no markdown fences.',
      [{ role: 'user', content: 'Extract from this business URL: name, up to 5 products/services with prices, target audience, brand tone. Return only valid JSON: {"name":"","products":[{"name":"","price":"","description":"","url":""}],"audience":"","tone":""}. URL: ' + url }]
    );
    const json = JSON.parse(result.replace(/```json\n?|```/g, '').trim());
    const nameEl = document.getElementById('bp-business-name');
    if (json.name && nameEl && !nameEl.value) nameEl.value = json.name;
    if (Array.isArray(json.products) && json.products.length) {
      json.products.slice(0, 5).forEach(p => addProductCard(p));
      switchBPTab('products');
    }
    setSt('Website scraped ✓', 'done');
  } catch(e) {
    setSt('Scrape failed', '');
  }
}

async function analyzeBrand() {
  const ig = document.getElementById('bp-instagram')?.value?.trim();
  const fb = document.getElementById('bp-facebook')?.value?.trim();
  const tk = document.getElementById('bp-tiktok')?.value?.trim();
  const li = document.getElementById('bp-linkedin')?.value?.trim();
  const yt = document.getElementById('bp-youtube')?.value?.trim();
  const snapEl = document.getElementById('bp-brand-snapshot');
  if (snapEl) { snapEl.style.display = 'block'; snapEl.innerHTML = '<div class="tdots"><span></span><span></span><span></span></div> Analyzing brand…'; }
  setSt('Analyzing brand…', 'run');
  let igData = null, fbData = null;
  if (KEYS.apify) {
    const tasks = [];
    if (ig) tasks.push(runApifyActor('apify~instagram-scraper', { directUrls: [ig], resultsLimit: 12 }, KEYS.apify).then(r => { igData = r; }).catch(() => {}));
    if (fb) tasks.push(runApifyActor('apify~facebook-pages-scraper', { startUrls: [{ url: fb }], maxPosts: 10 }, KEYS.apify).then(r => { fbData = r; }).catch(() => {}));
    await Promise.all(tasks);
  }
  const igSummary = igData
    ? JSON.stringify({ username: igData[0]?.username, biography: igData[0]?.biography, followersCount: igData[0]?.followersCount, captions: igData.slice(0,12).map(p=>p.caption).filter(Boolean), hashtags: [...new Set(igData.flatMap(p=>(p.hashtags||[])))].slice(0,20) })
    : 'No Instagram data';
  const fbSummary = fbData
    ? JSON.stringify({ name: fbData[0]?.title, about: fbData[0]?.about, likes: fbData[0]?.likes, posts: fbData.slice(0,10).map(p=>p.text).filter(Boolean) })
    : 'No Facebook data';
  try {
    const result = await ai(
      'You are a brand analyst. Return only valid JSON — no markdown fences.',
      [{ role: 'user', content: `Analyze this business based on social data.\nInstagram data: ${igSummary}\nFacebook data: ${fbSummary}\nSocial URLs: ig=${ig||'none'} fb=${fb||'none'} tk=${tk||'none'} li=${li||'none'} yt=${yt||'none'}\nReturn JSON: {"tone":"","themes":["","",""],"visual_style":"","posting_frequency":"","top_hashtags":["","",""],"audience_signals":"","ad_angles":["","",""],"instagram_followers":0,"facebook_likes":0}` }]
    );
    const snap = JSON.parse(result.replace(/```json\n?|```/g, '').trim());
    if (snapEl) {
      snapEl.innerHTML = `<div class="rcard"><div class="rcard-lbl">Brand Snapshot</div><div class="rcard-body" style="font-size:11px;line-height:1.7;"><strong>Tone:</strong> ${escHtml(snap.tone||'')}<br><strong>Themes:</strong> ${(snap.themes||[]).map(escHtml).join(' · ')}<br><strong>Visual Style:</strong> ${escHtml(snap.visual_style||'')}<br><strong>Audience:</strong> ${escHtml(snap.audience_signals||'')}<br><strong>Ad Angles:</strong> ${(snap.ad_angles||[]).map(escHtml).join(' · ')}<br><strong>Top Hashtags:</strong> ${(snap.top_hashtags||[]).map(t=>'#'+escHtml(t)).join(' ')}<br><strong>IG Followers:</strong> ${snap.instagram_followers||'—'} &middot; <strong>FB Likes:</strong> ${snap.facebook_likes||'—'}</div></div>`;
    }
    if (currentBizId && currentUser) {
      await sb.from('base_profiles').upsert({ business_id: currentBizId, user_id: currentUser.id, brand_snapshot: snap, updated_at: new Date().toISOString() }, { onConflict: 'business_id' });
    }
    setSt('Brand analyzed ✓', 'done');
  } catch(e) {
    if (snapEl) snapEl.innerHTML = '<div style="color:var(--red);font-size:11px;">⚠ Analysis failed. Check your AI key in Settings.</div>';
    setSt('Analysis failed', '');
  }
}

let _bpProductCount = 0;
function addProductCard(data) {
  data = data || {};
  const list  = document.getElementById('bp-products-list');
  const empty = document.getElementById('bp-products-empty');
  if (!list) return;
  if (list.querySelectorAll('.bp-product-card').length >= 10) { alert('Maximum 10 products / services.'); return; }
  if (empty) empty.style.display = 'none';
  const localId = 'bpp_' + Date.now() + '_' + (++_bpProductCount);
  const card = document.createElement('div');
  card.className = 'bp-product-card dcard';
  card.dataset.localId = localId;
  card.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;flex-wrap:wrap;gap:6px;">
      <div style="display:flex;gap:6px;">
        <button class="btn bg bsm bp-type-btn active" data-type="product" onclick="setBPType(this,'product')">Product</button>
        <button class="btn bg bsm bp-type-btn" data-type="service" onclick="setBPType(this,'service')">Service</button>
      </div>
      <div style="display:flex;align-items:center;gap:6px;">
        <div class="bp-connected-pill" style="display:none;background:rgba(0,212,160,.12);border:1px solid rgba(0,212,160,.3);color:#00D4A0;border-radius:10px;padding:2px 8px;font-size:10px;font-weight:700;">✓ Connected</div>
        <button class="btn bg bsm" style="color:var(--accent);border-color:rgba(0,212,160,.3);" onclick="connectProductToPipeline(this.closest('.bp-product-card').dataset.localId,this.closest('.bp-product-card').querySelector('.bp-pname').value,this.closest('.bp-product-card').querySelector('.bp-price').value)">🔗 Connect</button>
        <button class="bk-rm" onclick="removeBPProduct(this)" title="Delete">✕</button>
      </div>
    </div>
    <div class="flbl">Product / Service Name</div>
    <input class="fi bp-pname" placeholder="e.g. Protein Powder" value="${escHtml(data.name||'')}">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
      <div><div class="flbl">Price</div><input class="fi bp-price" placeholder="e.g. $49" value="${escHtml(data.price||'')}" style="margin-bottom:0;"></div>
      <div><div class="flbl">URL</div><input class="fi bp-url" placeholder="https://..." value="${escHtml(data.url||'')}" style="margin-bottom:0;" onblur="(async function(el){if(!el.value||el.value.length<5)return;const d=el.closest('.bp-product-card').querySelector('.bp-desc');if(d&&!d.value){try{const r=await ai('Return a 1-2 sentence product description only.',[{role:'user',content:'URL: '+el.value}]);if(r)d.value=r.substring(0,200);}catch(e){}}})(this)"></div>
    </div>
    <div class="flbl" style="margin-top:6px;">Description</div>
    <textarea class="fta bp-desc" placeholder="Brief product description…" style="min-height:48px;margin-bottom:4px;">${escHtml(data.description||'')}</textarea>
    <div style="font-size:10px;color:var(--t2);text-align:right;">0 ads saved</div>`;
  list.appendChild(card);
}

function setBPType(btn, type) {
  btn.closest('.bp-product-card').querySelectorAll('.bp-type-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

function removeBPProduct(btn) {
  const card = btn.closest('.bp-product-card');
  if (card) card.remove();
  const list  = document.getElementById('bp-products-list');
  const empty = document.getElementById('bp-products-empty');
  if (empty && list && !list.querySelector('.bp-product-card')) empty.style.display = 'block';
}

function handleLogoUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => { S.brandLogoUrl = e.target.result; };
  reader.readAsDataURL(file);
}

function connectProductToPipeline(localId, name, price) {
  if (!name) { alert('Enter a product name first.'); return; }
  S.currentProductId = localId;
  S.product  = name;
  S.price    = price || '';
  const dProd  = document.getElementById('d-product');
  const dPrice = document.getElementById('d-price');
  if (dProd)  dProd.value  = name;
  if (dPrice) dPrice.value = price || '';
  const pill     = document.getElementById('connected-product-pill');
  const pillName = document.getElementById('connected-product-name');
  if (pill)     pill.style.display = 'flex';
  if (pillName) pillName.textContent = name;
  document.querySelectorAll('.bp-product-card').forEach(card => {
    const cpill = card.querySelector('.bp-connected-pill');
    if (cpill) cpill.style.display = card.dataset.localId === localId ? 'inline-block' : 'none';
  });
  go('data');
}

function connectProductFromResearch(productId) {
  if (!productId) { S.currentProductId = null; return; }
  S.currentProductId = productId;
  const prod = (S.products || []).find(p => p.id === productId);
  const pill     = document.getElementById('connected-product-pill');
  const pillName = document.getElementById('connected-product-name');
  if (prod && pill && pillName) { pillName.textContent = prod.name; pill.style.display = 'flex'; }
}

async function saveBaseProfile() {
  if (!currentBizId || !currentUser) { alert('Select a client first.'); return; }
  setSt('Saving profile…', 'run');
  try {
    await sb.from('base_profiles').upsert({
      business_id:   currentBizId,
      user_id:       currentUser.id,
      business_name: document.getElementById('bp-business-name')?.value?.trim() || '',
      industry:      document.getElementById('bp-industry')?.value || '',
      location:      document.getElementById('bp-location')?.value?.trim() || '',
      website:       document.getElementById('bp-website')?.value?.trim() || '',
      tagline:       document.getElementById('bp-tagline')?.value?.trim() || '',
      mission:       document.getElementById('bp-mission')?.value?.trim() || '',
      instagram:     document.getElementById('bp-instagram')?.value?.trim() || '',
      facebook:      document.getElementById('bp-facebook')?.value?.trim() || '',
      tiktok:        document.getElementById('bp-tiktok')?.value?.trim() || '',
      linkedin:      document.getElementById('bp-linkedin')?.value?.trim() || '',
      youtube:       document.getElementById('bp-youtube')?.value?.trim() || '',
      updated_at:    new Date().toISOString()
    }, { onConflict: 'business_id' });

    const savedProducts = [];
    for (const card of document.querySelectorAll('.bp-product-card')) {
      const typeBtn = card.querySelector('.bp-type-btn.active');
      const name    = card.querySelector('.bp-pname')?.value?.trim() || '';
      if (!name) continue;
      const payload = {
        business_id: currentBizId,
        user_id:     currentUser.id,
        name,
        type:        typeBtn?.dataset?.type || 'product',
        price:       card.querySelector('.bp-price')?.value?.trim() || '',
        description: card.querySelector('.bp-desc')?.value?.trim()  || '',
        url:         card.querySelector('.bp-url')?.value?.trim()   || ''
      };
      if (card.dataset.supabaseId) payload.id = card.dataset.supabaseId;
      const { data: pData } = await sb.from('products').upsert(payload, { onConflict: 'id' }).select().single();
      if (pData) {
        card.dataset.supabaseId = pData.id;
        await sb.from('products').update({ storage_folder: 'products/' + pData.id + '/' }).eq('id', pData.id);
        if (S.currentProductId === card.dataset.localId) S.currentProductId = pData.id;
        savedProducts.push(pData);
      }
    }
    S.products = savedProducts;
    populateProductDropdowns();
    setSt('Profile saved ✓', 'done');
  } catch(e) {
    setSt('Save failed: ' + e.message, '');
  }
}

async function loadBaseProfile() {
  if (!currentBizId || !currentUser) return;
  setSt('Loading profile…', 'run');
  try {
    const [profileRes, productsRes] = await Promise.all([
      sb.from('base_profiles').select('*').eq('business_id', currentBizId).maybeSingle(),
      sb.from('products').select('*').eq('business_id', currentBizId).order('created_at', { ascending: true })
    ]);
    const p = profileRes.data;
    if (p) {
      const set = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ''; };
      set('bp-business-name', p.business_name);
      set('bp-industry',      p.industry);
      set('bp-location',      p.location);
      set('bp-website',       p.website);
      set('bp-tagline',       p.tagline);
      set('bp-mission',       p.mission);
      set('bp-instagram',     p.instagram);
      set('bp-facebook',      p.facebook);
      set('bp-tiktok',        p.tiktok);
      set('bp-linkedin',      p.linkedin);
      set('bp-youtube',       p.youtube);
    }
    const products = productsRes.data || [];
    S.products = products;
    const list  = document.getElementById('bp-products-list');
    const empty = document.getElementById('bp-products-empty');
    if (list) {
      list.innerHTML = '';
      _bpProductCount = 0;
      products.forEach(prod => {
        addProductCard({ name: prod.name, price: prod.price, description: prod.description, url: prod.url });
        const card = list.lastElementChild;
        if (card) {
          card.dataset.supabaseId = prod.id;
          const typeBtn = card.querySelector(`.bp-type-btn[data-type="${prod.type||'product'}"]`);
          if (typeBtn) { card.querySelectorAll('.bp-type-btn').forEach(b => b.classList.remove('active')); typeBtn.classList.add('active'); }
          if (S.currentProductId === prod.id) {
            const cpill = card.querySelector('.bp-connected-pill');
            if (cpill) cpill.style.display = 'inline-block';
          }
        }
      });
      if (empty) empty.style.display = products.length ? 'none' : 'block';
    }
    populateProductDropdowns();
    setSt('Ready', '');
  } catch(e) {
    setSt('Load failed', '');
  }
}

function populateProductDropdowns() {
  const products = S.products || [];
  [
    { id: 'adlib-product-filter', first: '<option value="">All Products</option>' },
    { id: 'ar-product-select',    first: '<option value="">Select product (optional)</option>' }
  ].forEach(({ id, first }) => {
    const sel = document.getElementById(id);
    if (!sel) return;
    sel.innerHTML = first + products.map(p => `<option value="${escHtml(p.id)}">${escHtml(p.name)}</option>`).join('');
    if (id === 'ar-product-select' && S.currentProductId) sel.value = S.currentProductId;
  });
}

function filterAdsByProduct(productId) {
  const grid  = document.getElementById('adlib-grid');
  const empty = document.getElementById('adlib-empty');
  if (!grid) return;
  const cards = grid.querySelectorAll('.adlib-card');
  cards.forEach(card => { card.style.display = (!productId || card.dataset.productId === productId) ? '' : 'none'; });
  if (empty) empty.style.display = [...cards].some(c => c.style.display !== 'none') ? 'none' : 'flex';
}

"""
patch('// ── Runbase logo', NEW_JS + '// ── Runbase logo', 'all new JS functions', 1)

# ── Write output ───────────────────────────────────────────────────────────
with open('/home/admin/meta-ads-agent/index.html', 'w') as f:
    f.write(html)

total = len(applied) + len(missed)
print(f'\n{"="*50}')
print(f'Patches applied: {len(applied)}/{total}')
if missed:
    print(f'MISSED: {missed}')
print(f'File lines: {html.count(chr(10))+1}')
