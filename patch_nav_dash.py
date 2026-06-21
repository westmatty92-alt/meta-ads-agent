#!/usr/bin/env python3
"""Command 1: Nav reorder + Dashboard restructure."""

with open('/home/admin/meta-ads-agent/index.html', 'r') as f:
    html = f.read()

applied = []; missed = []

def patch(old, new, label, count=1):
    global html
    if old not in html:
        missed.append(label); print(f'MISS: {label!r}')
        return
    html = html.replace(old, new, count)
    applied.append(label); print(f'OK:   {label}')

# ═══════════════════════════════════════════════════════════════
# PART 0 — ID renames (cascade-safe: do once each)
# ═══════════════════════════════════════════════════════════════

# adlib → adLibrary (nav ID, panel ID, badge, onclick, go() case)
patch("id=\"nav-adlib\"",            "id=\"nav-adLibrary\"",      "rename nav-adlib→adLibrary")
patch("id=\"panel-adlib\"",          "id=\"panel-adLibrary\"",    "rename panel-adlib→adLibrary")
patch("id=\"badge-adlib\"",          "id=\"badge-adLibrary\"",    "rename badge-adlib HTML")
patch("onclick=\"go('adlib')\"",     "onclick=\"go('adLibrary')\"","rename onclick go(adlib)")
patch("if(name==='adlib'){",         "if(name==='adLibrary'){",   "rename go() adlib case")
patch("'badge-adlib')",              "'badge-adLibrary')",        "rename badge-adlib JS ref 1")

# dash → dashboard (nav ID, panel ID, badge, onclick, go() case)
patch("id=\"nav-dash\"",             "id=\"nav-dashboard\"",      "rename nav-dash→dashboard")
patch("id=\"panel-dash\"",           "id=\"panel-dashboard\"",    "rename panel-dash→dashboard")
patch("id=\"badge-dash\"",           "id=\"badge-dashboard\"",    "rename badge-dash HTML")
patch("onclick=\"go('dash')\"",      "onclick=\"go('dashboard')\"","rename onclick go(dash)")
patch("if(name==='dash'){",          "if(name==='dashboard'){",   "rename go() dash case")

# ═══════════════════════════════════════════════════════════════
# PART 1 — Replace entire <nav class="pipe"> block
# ═══════════════════════════════════════════════════════════════

OLD_NAV = """  <nav class="pipe">
    <div class="pipe-label">Pipeline</div>
    <div class="stage active" id="nav-data" onclick="go('data')">
      <div class="si">📊</div>
      <div class="sinfo"><div class="sname">1. Setup</div><div class="sdesc">Client data</div></div>
      <span class="sbadge br" id="badge-data">Start</span>
    </div>
    <div class="stage" id="nav-baseProfile" onclick="go('baseProfile')">
      <div class="si">🏢</div>
      <div class="sinfo"><div class="sname">Base Profile</div><div class="sdesc">Business setup</div></div>
      <span class="sbadge br">Setup</span>
    </div>
    <div class="conn" id="conn-1"></div>
    <div class="stage locked" id="nav-audit" onclick="go('audit')">
      <div class="si">🔍</div>
      <div class="sinfo"><div class="sname">2. Audit</div><div class="sdesc">50-check analysis</div></div>
      <span class="sbadge bl" id="badge-audit">Locked</span>
    </div>
    <div class="conn" id="conn-2"></div>
    <div class="stage locked" id="nav-research" onclick="go('research')">
      <div class="si">🔬</div>
      <div class="sinfo"><div class="sname">3. Research</div><div class="sdesc">Market + competitor</div></div>
      <span class="sbadge bl" id="badge-research">Locked</span>
    </div>
    <div class="conn" id="conn-3"></div>
    <div class="stage locked" id="nav-build" onclick="go('build')">
      <div class="si">⚡</div>
      <div class="sinfo"><div class="sname">4. Ad Builder</div><div class="sdesc">100/100 creative</div></div>
      <span class="sbadge bl" id="badge-build">Locked</span>
    </div>
    <div class="conn" id="conn-4"></div>
    <div class="stage locked" id="nav-visual" onclick="go('visual')">
      <div class="si">🎨</div>
      <div class="sinfo"><div class="sname">5. Visual + Prompt</div><div class="sdesc">Concept + image gen</div></div>
      <span class="sbadge bl" id="badge-visual">Locked</span>
    </div>

    <div style="margin-top:auto;padding:12px 0 0;">
      <button class="run-all" onclick="runAll()" id="run-all">▶ Run Full Pipeline</button>
      <div style="border-top:1px solid var(--border);margin:6px 0;"></div>
      <div class="stage" id="nav-adLibrary" onclick="go('adLibrary')">
        <div class="si">📚</div>
        <div class="sinfo"><div class="sname">Ad Library</div><div class="sdesc">Saved ad packages</div></div>
        <span class="sbadge bl" id="badge-adLibrary"></span>
      </div>
      <div class="stage" id="nav-dashboard" onclick="go('dashboard')">
        <div class="si">📊</div>
        <div class="sinfo"><div class="sname">Dashboard</div><div class="sdesc">Campaign analytics</div></div>
        <span class="sbadge bl" id="badge-dashboard"></span>
      </div>
      <div class="stage" id="nav-autoResearch" onclick="go('autoResearch')">
        <div class="si">🤖</div>
        <div class="sinfo"><div class="sname">Auto-Research</div><div class="sdesc">Reddit + Ad Library</div></div>
        <span class="sbadge br">Apify</span>
      </div>
      <div class="stage" id="nav-settings" onclick="go('settings')">
        <div class="si">⚙️</div>
        <div class="sinfo"><div class="sname">Settings</div><div class="sdesc">API keys</div></div>
        <span class="sbadge bl">Keys</span>
      </div>
      <div class="ctx-box" id="ctx-box" style="display:none;">
        <h4>Client Context</h4>
        <div class="ctx-row"><span>Client</span><span class="ctx-val" id="ctx-biz">—</span></div>
        <div class="ctx-row"><span>Score</span><span class="ctx-val" id="ctx-score">—</span></div>
        <div class="ctx-row"><span>Product</span><span class="ctx-val" id="ctx-prod">—</span></div>
        <div class="ctx-row"><span>Stages</span><span class="ctx-val" id="ctx-stgs">0 / 5</span></div>
      </div>
    </div>
  </nav>"""

NEW_NAV = """  <nav class="pipe">
    <!-- ── TOOLS section ─────────────────────────────── -->
    <div class="pipe-label">Tools</div>
    <div class="stage" id="nav-baseProfile" onclick="go('baseProfile')">
      <div class="si">🏢</div>
      <div class="sinfo"><div class="sname">Base Profile</div><div class="sdesc">Business setup</div></div>
      <span class="sbadge br">Setup</span>
    </div>
    <div class="stage" id="nav-dashboard" onclick="go('dashboard')">
      <div class="si">📊</div>
      <div class="sinfo"><div class="sname">Dashboard</div><div class="sdesc">Campaign analytics</div></div>
      <span class="sbadge bl" id="badge-dashboard"></span>
    </div>
    <div class="stage" id="nav-autoResearch" onclick="go('autoResearch')">
      <div class="si">🤖</div>
      <div class="sinfo"><div class="sname">Auto-Research</div><div class="sdesc">Reddit + Ad Library</div></div>
      <span class="sbadge br">Apify</span>
    </div>
    <div class="stage" id="nav-adLibrary" onclick="go('adLibrary')">
      <div class="si">📚</div>
      <div class="sinfo"><div class="sname">Ad Library</div><div class="sdesc">Saved ad packages</div></div>
      <span class="sbadge bl" id="badge-adLibrary"></span>
    </div>
    <!-- ── PIPELINE section ───────────────────────────── -->
    <div style="border-top:1px solid var(--border);margin:6px 8px 2px;"></div>
    <div class="pipe-label">Pipeline</div>
    <div class="stage active" id="nav-data" onclick="go('data')">
      <div class="si">📊</div>
      <div class="sinfo"><div class="sname">1. Setup</div><div class="sdesc">Client data</div></div>
      <span class="sbadge br" id="badge-data">Start</span>
    </div>
    <div class="conn" id="conn-1"></div>
    <div class="stage locked" id="nav-audit" onclick="go('audit')">
      <div class="si">🔍</div>
      <div class="sinfo"><div class="sname">2. Audit</div><div class="sdesc">50-check analysis</div></div>
      <span class="sbadge bl" id="badge-audit">Locked</span>
    </div>
    <div class="conn" id="conn-2"></div>
    <div class="stage locked" id="nav-research" onclick="go('research')">
      <div class="si">🔬</div>
      <div class="sinfo"><div class="sname">3. Research</div><div class="sdesc">Market + competitor</div></div>
      <span class="sbadge bl" id="badge-research">Locked</span>
    </div>
    <div class="conn" id="conn-3"></div>
    <div class="stage locked" id="nav-build" onclick="go('build')">
      <div class="si">⚡</div>
      <div class="sinfo"><div class="sname">4. Ad Builder</div><div class="sdesc">100/100 creative</div></div>
      <span class="sbadge bl" id="badge-build">Locked</span>
    </div>
    <div class="conn" id="conn-4"></div>
    <div class="stage locked" id="nav-visual" onclick="go('visual')">
      <div class="si">🎨</div>
      <div class="sinfo"><div class="sname">5. Visual + Prompt</div><div class="sdesc">Concept + image gen</div></div>
      <span class="sbadge bl" id="badge-visual">Locked</span>
    </div>
    <!-- ── Bottom ─────────────────────────────────────── -->
    <div style="margin-top:auto;padding:12px 0 0;">
      <button class="run-all" onclick="runAll()" id="run-all">▶ Run Full Pipeline</button>
      <div style="border-top:1px solid var(--border);margin:6px 0;"></div>
      <div class="stage" id="nav-settings" onclick="go('settings')">
        <div class="si">⚙️</div>
        <div class="sinfo"><div class="sname">Settings</div><div class="sdesc">API keys</div></div>
        <span class="sbadge bl">Keys</span>
      </div>
      <div class="ctx-box" id="ctx-box" style="display:none;">
        <h4>Client Context</h4>
        <div class="ctx-row"><span>Client</span><span class="ctx-val" id="ctx-biz">—</span></div>
        <div class="ctx-row"><span>Score</span><span class="ctx-val" id="ctx-score">—</span></div>
        <div class="ctx-row"><span>Product</span><span class="ctx-val" id="ctx-prod">—</span></div>
        <div class="ctx-row"><span>Stages</span><span class="ctx-val" id="ctx-stgs">0 / 5</span></div>
      </div>
    </div>
  </nav>"""

patch(OLD_NAV, NEW_NAV, 'nav reorder')

# ═══════════════════════════════════════════════════════════════
# PART 2 — Replace dashboard panel HTML
# ═══════════════════════════════════════════════════════════════

OLD_DASH = """    <div class="spanel" id="panel-dashboard">
      <div class="shdr">
        <div class="shdr-left"><h2>📊 Dashboard</h2><p>Live campaign analytics · pulled from performance history &amp; GHL</p></div>
        <div class="sacts">
          <button class="btn bp bsm" id="dash-sync-btn" onclick="syncFromGHL()">🔄 Sync from GHL</button>
          <button class="btn bg bsm" onclick="go('data')">← Pipeline</button>
        </div>
      </div>
      <div class="dash-sync-bar">
        <span class="dash-timestamp" id="dash-last-sync">Last synced: never</span>
        <span id="dash-sync-msg" style="font-size:11px;color:var(--green);display:none;"></span>
      </div>
      <div class="dash-body">
        <div id="dash-empty" class="dash-empty-state">
          <div class="big">📊</div>
          <h3>No performance data yet</h3>
          <p style="font-size:12px;">Upload a CSV in Stage 1, or click <strong>Sync from GHL</strong> to pull your campaign data.</p>
        </div>
        <div id="dash-content" style="display:none;">
          <!-- Metrics row -->
          <div id="dash-metrics" class="metrics-row"></div>
          <!-- Charts 2×2 grid -->
          <div id="dash-charts" class="charts-grid"></div>
          <!-- Campaigns table -->
          <div style="margin-bottom:24px;">
            <div class="dash-section-hdr">
              <span>Campaign Performance</span>
              <span id="camp-count" style="font-size:10px;color:var(--t2);"></span>
            </div>
            <div style="overflow-x:auto;">
              <table class="perf-table" id="camp-table">
                <thead><tr id="camp-thead"></tr></thead>
                <tbody id="camp-tbody"></tbody>
              </table>
            </div>
          </div>
          <!-- AI Suggestions -->
          <div style="margin-bottom:24px;">
            <div class="dash-section-hdr">
              <span>🤖 AI Suggestions</span>
              <button class="btn bp bsm" id="ai-sugg-btn" onclick="getAISuggestions()">🤖 Analyze &amp; Suggest</button>
            </div>
            <div id="ai-sugg-container" style="color:var(--t2);font-size:12px;text-align:center;padding:18px;">Click "Analyze &amp; Suggest" to get AI-powered recommendations for your campaigns.</div>
          </div>
        </div>
      </div>
    </div>"""

NEW_DASH = """    <div class="spanel" id="panel-dashboard">
      <!-- Header with product + period selectors -->
      <div class="shdr">
        <div class="shdr-left">
          <h2>📊 Dashboard</h2>
          <p>Campaign performance across all products</p>
        </div>
        <div class="sacts" style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
          <select id="dash-product-select" class="fsel" style="margin:0;font-size:11px;padding:3px 8px;" onchange="switchDashView(this.value)">
            <option value="">All Products</option>
          </select>
          <select id="dash-period-select" class="fsel" style="margin:0;font-size:11px;padding:3px 8px;">
            <option value="week">This Week</option>
            <option value="month" selected>This Month</option>
            <option value="quarter">This Quarter</option>
            <option value="year">This Year</option>
            <option value="all">All Time</option>
          </select>
          <button class="btn bp bsm" id="dash-sync-btn" onclick="syncFromGHL()">🔄 Sync from GHL</button>
          <button class="btn bg bsm" onclick="go('data')">← Pipeline</button>
        </div>
      </div>
      <div class="dash-sync-bar">
        <span class="dash-timestamp" id="dash-last-sync">Last synced: never</span>
        <span id="dash-sync-msg" style="font-size:11px;color:var(--green);display:none;"></span>
      </div>

      <!-- VIEW A: All Products (default) -->
      <div class="dash-view-all dash-body" id="dash-view-all">
        <div id="dash-empty" class="dash-empty-state">
          <div class="big">📊</div>
          <h3>No performance data yet</h3>
          <p style="font-size:12px;">Upload a CSV in Stage 1, or click <strong>Sync from GHL</strong> to pull your campaign data.</p>
        </div>
        <div id="dash-content" style="display:none;">
          <div id="dash-metrics" class="metrics-row"></div>
          <div id="dash-charts" class="charts-grid"></div>
          <div style="margin-bottom:24px;">
            <div class="dash-section-hdr">
              <span>Campaign Performance</span>
              <span id="camp-count" style="font-size:10px;color:var(--t2);"></span>
            </div>
            <div style="overflow-x:auto;">
              <table class="perf-table" id="camp-table">
                <thead><tr id="camp-thead"></tr></thead>
                <tbody id="camp-tbody"></tbody>
              </table>
            </div>
          </div>
          <div style="margin-bottom:24px;">
            <div class="dash-section-hdr">
              <span>🤖 AI Suggestions</span>
              <button class="btn bp bsm" id="ai-sugg-btn" onclick="getAISuggestions()">🤖 Analyze &amp; Suggest</button>
            </div>
            <div id="ai-sugg-container" style="color:var(--t2);font-size:12px;text-align:center;padding:18px;">Click "Analyze &amp; Suggest" to get AI-powered recommendations for your campaigns.</div>
          </div>
        </div>
      </div>

      <!-- VIEW B: Single Product (hidden by default) -->
      <div class="dash-view-product" id="dash-view-product" style="display:none;flex:1;flex-direction:column;overflow:hidden;">
        <!-- Product header card -->
        <div class="dash-product-header" style="margin:14px 22px 0;flex-shrink:0;">
          <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap;">
            <div>
              <div id="dash-prod-name" style="font-family:var(--display);font-size:20px;font-weight:800;color:var(--text);letter-spacing:-.3px;line-height:1.2;">—</div>
              <div style="display:flex;align-items:center;gap:8px;margin-top:6px;flex-wrap:wrap;">
                <span id="dash-prod-type-badge" style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;background:var(--s3);border-radius:4px;padding:2px 7px;color:var(--t2);">Product</span>
                <span id="dash-prod-price" style="font-size:12px;color:var(--t2);"></span>
                <span id="dash-prod-connected" style="display:none;font-size:10px;font-weight:700;color:#00D4A0;background:rgba(0,212,160,.1);border:1px solid rgba(0,212,160,.3);border-radius:10px;padding:2px 8px;">✓ Active in Pipeline</span>
              </div>
            </div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;">
              <div class="mcard mc-neutral" style="min-width:90px;padding:10px 14px;">
                <div class="mcard-lbl">Total Spend</div>
                <div class="mcard-val gnum" id="dash-prod-spend">—</div>
              </div>
              <div class="mcard mc-neutral" style="min-width:90px;padding:10px 14px;">
                <div class="mcard-lbl">Ads Generated</div>
                <div class="mcard-val gnum" id="dash-prod-ad-count">—</div>
              </div>
              <div class="mcard mc-neutral" style="min-width:90px;padding:10px 14px;">
                <div class="mcard-lbl">Last Audit</div>
                <div class="mcard-val gnum" id="dash-prod-audit-score">—</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 6-tab bar -->
        <div class="dash-product-tabs" style="margin:14px 22px 0;flex-shrink:0;">
          <button class="dash-product-tab active" id="dash-ptab-perf"         onclick="switchDashProductTab('perf')">📈 Performance</button>
          <button class="dash-product-tab"         id="dash-ptab-period"       onclick="switchDashProductTab('period')">📅 vs Last Period</button>
          <button class="dash-product-tab"         id="dash-ptab-report"       onclick="switchDashProductTab('report')">📋 Report</button>
          <button class="dash-product-tab"         id="dash-ptab-improvements" onclick="switchDashProductTab('improvements')">💡 Improvements</button>
          <button class="dash-product-tab"         id="dash-ptab-adlib"        onclick="switchDashProductTab('adlib')">📚 Ad Library</button>
          <button class="dash-product-tab"         id="dash-ptab-metadata"     onclick="switchDashProductTab('metadata')">🗂 Metadata</button>
        </div>

        <!-- Tab pane scroll area -->
        <div style="flex:1;overflow-y:auto;padding:16px 22px;">

          <!-- TAB 1: Performance (default) -->
          <div id="dash-pane-perf" class="dash-ptab-pane">
            <div class="metrics-row" id="dash-prod-metrics" style="margin-bottom:14px;"></div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
              <div class="flbl" style="margin:0;white-space:nowrap;">Filter by Ad:</div>
              <select id="dash-ad-select" class="fsel" style="margin:0;flex:1;" onchange="onDashAdSelected(this.value)">
                <option value="">All Ads for this Product</option>
              </select>
            </div>
            <div style="margin-bottom:16px;">
              <div class="dash-section-hdr"><span>Campaign Performance</span></div>
              <div style="overflow-x:auto;">
                <table class="perf-table" id="dash-prod-camp-table">
                  <thead><tr id="dash-prod-camp-thead"></tr></thead>
                  <tbody id="dash-prod-camp-tbody"></tbody>
                </table>
              </div>
            </div>
            <div class="dash-skeleton" id="dash-perf-skeleton">Performance data loads here once you have ad_performance records linked to this product</div>
          </div>

          <!-- TAB 2: vs Last Period -->
          <div id="dash-pane-period" class="dash-ptab-pane" style="display:none;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
              <div class="flbl" style="margin:0;">Compare:</div>
              <select class="fsel" id="dash-period-compare" style="margin:0;">
                <option value="wow">Week over Week</option>
                <option value="mom" selected>Month over Month</option>
                <option value="yoy">Year over Year</option>
              </select>
            </div>
            <div class="dash-skeleton">Period comparison loads here in Command 2</div>
          </div>

          <!-- TAB 3: Report -->
          <div id="dash-pane-report" class="dash-ptab-pane" style="display:none;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
              <div class="flbl" style="margin:0;">Report Period:</div>
              <select class="fsel" id="dash-report-period" style="margin:0;">
                <option value="week">This Week</option>
                <option value="month" selected>This Month</option>
                <option value="quarter">This Quarter</option>
                <option value="year">This Year</option>
              </select>
            </div>
            <div class="dash-skeleton">Formatted report generates here in Command 2</div>
          </div>

          <!-- TAB 4: Improvements -->
          <div id="dash-pane-improvements" class="dash-ptab-pane" style="display:none;">
            <div class="dash-skeleton">AI improvement analysis loads here in Command 2</div>
          </div>

          <!-- TAB 5: Ad Library (functional) -->
          <div id="dash-pane-adlib" class="dash-ptab-pane" style="display:none;">
            <div class="adlib-empty" id="dash-prod-adlib-empty" style="display:none;">
              <div class="big">📚</div>
              <h3>No ads generated yet for this product</h3>
              <p style="font-size:12px;">Complete Stage 5 to save your first ad for this product.</p>
            </div>
            <div class="adlib-grid" id="dash-prod-adlib-grid"></div>
          </div>

          <!-- TAB 6: Metadata (functional) -->
          <div id="dash-pane-metadata" class="dash-ptab-pane" style="display:none;">
            <div class="dcard" style="max-width:540px;">
              <h3>Product Details</h3>
              <div class="flbl">Name</div>
              <div id="dash-meta-name" style="font-size:13px;margin-bottom:8px;">—</div>
              <div class="flbl">Type</div>
              <div id="dash-meta-type" style="font-size:13px;margin-bottom:8px;">—</div>
              <div class="flbl">Price</div>
              <div id="dash-meta-price" style="font-size:13px;margin-bottom:8px;">—</div>
              <div class="flbl">Description</div>
              <div id="dash-meta-desc" style="font-size:13px;margin-bottom:8px;color:var(--t2);">—</div>
              <div class="flbl">URL</div>
              <div id="dash-meta-url" style="font-size:13px;margin-bottom:8px;word-break:break-all;">—</div>
              <div class="flbl">Storage Folder</div>
              <div id="dash-meta-folder" style="font-size:11px;color:var(--t2);font-family:var(--mono);margin-bottom:12px;">—</div>
              <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
                <span class="sbadge br" id="dash-meta-ad-count">0 ads</span>
                <span class="sbadge br" id="dash-meta-perf-count">0 performance records</span>
              </div>
              <button class="btn bg bsm" onclick="go('baseProfile')">✏ Edit in Base Profile</button>
            </div>
          </div>

        </div><!-- end tab scroll area -->
      </div><!-- end VIEW B -->

    </div>"""

patch(OLD_DASH, NEW_DASH, 'dashboard panel HTML')

# ═══════════════════════════════════════════════════════════════
# PART 3 — CSS additions
# ═══════════════════════════════════════════════════════════════

NEW_CSS = """\
/* ── Dashboard product view ── */
.dash-skeleton{background:var(--s2);border-radius:8px;padding:40px;text-align:center;color:var(--t2);font-size:12px;border:1px dashed var(--border2);}
.dash-product-header{background:var(--surface);border:1px solid var(--border2);border-radius:10px;padding:16px 20px;}
.dash-product-tabs{display:flex;gap:0;border-bottom:1px solid var(--border);overflow-x:auto;}
.dash-product-tab{padding:8px 16px;font-size:12px;font-weight:600;cursor:pointer;border:none;background:transparent;color:var(--t2);font-family:var(--sans);border-bottom:2px solid transparent;margin-bottom:-1px;white-space:nowrap;transition:all .15s;flex-shrink:0;}
.dash-product-tab.active{color:var(--accent);border-bottom-color:var(--accent);}
.dash-product-tab:hover:not(.active){color:var(--text);}
.dash-view-all{}
.dash-view-product{display:none;}
"""
patch('</style>', NEW_CSS + '</style>', 'dashboard CSS')

# ═══════════════════════════════════════════════════════════════
# PART 4 — Update go() for dashboard loading
# ═══════════════════════════════════════════════════════════════

patch(
    "if(name==='dashboard'){ loadPerfData().then(()=>{ renderDashboard(); updateDashTimestamp(); }); }",
    "if(name==='dashboard'){ loadPerfData().then(()=>{ renderDashboard(); updateDashTimestamp(); }); populateProductDropdowns(); }",
    "go() dashboard add populateProductDropdowns"
)

# ═══════════════════════════════════════════════════════════════
# PART 5 — Add currentDashProductId to globals
# ═══════════════════════════════════════════════════════════════

patch(
    'let perfData = [];',
    'let perfData = [];\nlet currentDashProductId = null;',
    'add currentDashProductId global'
)

# ═══════════════════════════════════════════════════════════════
# PART 6 — Update populateProductDropdowns to include dash-product-select
# ═══════════════════════════════════════════════════════════════

patch(
    """  [
    { id: 'adlib-product-filter', first: '<option value="">All Products</option>' },
    { id: 'ar-product-select',    first: '<option value="">Select product (optional)</option>' }
  ].forEach(({ id, first }) => {""",
    """  [
    { id: 'adlib-product-filter', first: '<option value="">All Products</option>' },
    { id: 'ar-product-select',    first: '<option value="">Select product (optional)</option>' },
    { id: 'dash-product-select',  first: '<option value="">All Products</option>' }
  ].forEach(({ id, first }) => {""",
    'populateProductDropdowns add dash-product-select'
)

# ═══════════════════════════════════════════════════════════════
# PART 7 — New JS functions (insert before // ── Base Profile section)
# ═══════════════════════════════════════════════════════════════

NEW_JS = r"""
// ── Dashboard Product View ────────────────────────────────────

function switchDashView(productId) {
  currentDashProductId = productId || null;
  const viewAll  = document.getElementById('dash-view-all');
  const viewProd = document.getElementById('dash-view-product');
  if (!productId) {
    if (viewAll)  viewAll.style.display  = '';
    if (viewProd) viewProd.style.display = 'none';
  } else {
    if (viewAll)  viewAll.style.display  = 'none';
    if (viewProd) viewProd.style.display = 'flex';
    loadProductDashboard(productId);
    populateDashAdSelector(productId);
  }
}

function switchDashProductTab(tabName) {
  const tabs = ['perf','period','report','improvements','adlib','metadata'];
  tabs.forEach(t => {
    const pane = document.getElementById('dash-pane-' + t);
    const btn  = document.getElementById('dash-ptab-' + t);
    if (pane) pane.style.display = t === tabName ? '' : 'none';
    if (btn)  btn.classList.toggle('active', t === tabName);
  });
}

async function loadProductDashboard(productId) {
  if (!currentBizId || !currentUser || !productId) return;
  console.log('[loadProductDashboard] productId:', productId);
  try {
    // Populate product header from S.products cache
    const prod = (S.products || []).find(p => p.id === productId);
    if (prod) {
      const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val ?? '—'; };
      set('dash-prod-name',   prod.name);
      set('dash-prod-price',  prod.price || '');
      set('dash-meta-name',   prod.name);
      set('dash-meta-type',   prod.type  || '—');
      set('dash-meta-price',  prod.price || '—');
      set('dash-meta-desc',   prod.description || '—');
      set('dash-meta-url',    prod.url   || '—');
      set('dash-meta-folder', prod.storage_folder || ('products/' + productId + '/'));
      const typeEl = document.getElementById('dash-prod-type-badge');
      if (typeEl) typeEl.textContent = prod.type || 'Product';
      const connEl = document.getElementById('dash-prod-connected');
      if (connEl) connEl.style.display = S.currentProductId === productId ? 'inline-block' : 'none';
    }

    // Parallel DB queries
    const [perfRes, adsRes] = await Promise.all([
      sb.from('ad_performance').select('*').eq('business_id', currentBizId).eq('product_id', productId),
      sb.from('generated_ads').select('*').eq('product_id', productId).order('created_at', { ascending: false })
    ]);

    const prodPerf = perfRes.data  || [];
    const prodAds  = adsRes.data   || [];
    console.log('[loadProductDashboard] perf rows:', prodPerf.length, '| ads:', prodAds.length);

    // Quick-stat header cards
    const totSpend = prodPerf.reduce((s, r) => s + (r.spend || 0), 0);
    const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    setEl('dash-prod-spend',    totSpend ? '$' + totSpend.toFixed(2) : '—');
    setEl('dash-prod-ad-count', prodAds.length || '—');
    setEl('dash-meta-ad-count',   prodAds.length  + ' ads');
    setEl('dash-meta-perf-count', prodPerf.length + ' performance records');

    // Performance tab metrics
    const metricsEl = document.getElementById('dash-prod-metrics');
    const skeletonEl = document.getElementById('dash-perf-skeleton');
    if (metricsEl) {
      if (prodPerf.length) {
        const totImpr   = prodPerf.reduce((s, r) => s + (r.impressions || 0), 0);
        const totClicks = prodPerf.reduce((s, r) => s + (r.clicks      || 0), 0);
        const totConv   = prodPerf.reduce((s, r) => s + (r.conversions || 0), 0);
        const avgCTR    = totImpr ? totClicks / totImpr * 100 : 0;
        const avgCPA    = totConv ? totSpend  / totConv       : 0;
        const roasRows  = prodPerf.filter(r => r.roas != null);
        const avgROAS   = roasRows.length ? roasRows.reduce((s, r) => s + (r.roas || 0), 0) / roasRows.length : 0;
        const cards = [
          { lbl: 'Spend',    val: '$' + totSpend.toFixed(2),              cls: 'mc-neutral' },
          { lbl: 'Avg CTR',  val: avgCTR.toFixed(2) + '%',                cls: avgCTR >= 2 ? 'mc-green' : avgCTR >= 1 ? 'mc-yellow' : 'mc-red' },
          { lbl: 'Avg CPA',  val: avgCPA  ? '$' + avgCPA.toFixed(2)  : '—', cls: 'mc-neutral' },
          { lbl: 'Avg ROAS', val: avgROAS ? avgROAS.toFixed(2) + 'x' : '—', cls: avgROAS >= 3 ? 'mc-green' : avgROAS >= 1.5 ? 'mc-yellow' : avgROAS > 0 ? 'mc-red' : 'mc-neutral' },
        ];
        metricsEl.innerHTML = cards.map(c => `<div class="mcard ${c.cls}"><div class="mcard-lbl">${c.lbl}</div><div class="mcard-val gnum">${c.val}</div></div>`).join('');
        if (skeletonEl) skeletonEl.style.display = 'none';
      } else {
        metricsEl.innerHTML = '';
        if (skeletonEl) { skeletonEl.style.display = ''; skeletonEl.textContent = 'No performance data yet for this product. Link ad_performance records to this product_id to see data here.'; }
      }
    }

    // Ad Library tab
    const adlibGrid  = document.getElementById('dash-prod-adlib-grid');
    const adlibEmpty = document.getElementById('dash-prod-adlib-empty');
    if (adlibGrid) {
      if (!prodAds.length) {
        adlibGrid.innerHTML = '';
        if (adlibEmpty) adlibEmpty.style.display = 'flex';
      } else {
        if (adlibEmpty) adlibEmpty.style.display = 'none';
        const scoreColor = s => !s ? 'var(--t2)' : s >= 80 ? 'var(--green)' : s >= 60 ? 'var(--yellow)' : 'var(--red)';
        adlibGrid.innerHTML = prodAds.map(ad => {
          const hook = escHtml((ad.hook || '').substring(0, 120));
          const date = ad.created_at ? new Date(ad.created_at).toLocaleDateString() : '';
          const sc   = ad.score;
          return `<div class="adlib-card"><div class="adlib-card-top"><span class="adlib-score" style="color:${scoreColor(sc)};">${sc != null ? sc + '/100' : '—'}</span><span class="adlib-date">${date}</span></div><div class="adlib-hook">${hook}${(ad.hook||'').length > 120 ? '…' : ''}</div><div class="adlib-actions"><button class="btn bg" onclick="viewFullAd('${escHtml(ad.id)}')">View</button><button class="btn bg" onclick="copyAdCopy('${escHtml(ad.id)}')">Copy</button><button class="btn bp" onclick="useAdAsStartingPoint('${escHtml(ad.id)}')">Use</button></div></div>`;
        }).join('');
      }
    }
  } catch(e) {
    console.error('[loadProductDashboard] Error:', e);
  }
}

async function populateDashAdSelector(productId) {
  const sel = document.getElementById('dash-ad-select');
  if (!sel || !productId) return;
  try {
    const { data } = await sb.from('generated_ads')
      .select('id, hook, created_at')
      .eq('product_id', productId)
      .order('created_at', { ascending: false });
    const ads = data || [];
    sel.innerHTML = '<option value="">All Ads for this Product</option>' +
      ads.map(ad => {
        const label = (ad.hook || 'Untitled ad').substring(0, 40) + ((ad.hook||'').length > 40 ? '…' : '');
        return `<option value="${escHtml(ad.id)}">${escHtml(label)}</option>`;
      }).join('');
  } catch(e) {
    console.error('[populateDashAdSelector] Error:', e);
  }
}

function onDashAdSelected(adId) {
  console.log('[onDashAdSelected] adId:', adId || 'all — filtering in Command 2');
  // Command 2 will implement per-ad performance filtering
}

"""
patch('// ── Base Profile ─────────────────────────────────────────────────────────', NEW_JS + '// ── Base Profile ─────────────────────────────────────────────────────────', 'new JS functions', 1)

# ═══════════════════════════════════════════════════════════════
# Write + report
# ═══════════════════════════════════════════════════════════════
with open('/home/admin/meta-ads-agent/index.html', 'w') as f:
    f.write(html)

total = len(applied) + len(missed)
print(f'\n{"="*55}')
print(f'Patches: {len(applied)}/{total} applied')
if missed:
    print(f'MISSED:  {missed}')
print(f'File lines: {html.count(chr(10))+1}')
