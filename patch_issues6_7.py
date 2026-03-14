import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\web\votometro.html'
with open(path, encoding='utf-8') as f:
    c = f.read()
orig = len(c)
done = []

# ─────────────────────────────────────────────────────────────────────────────
# ISSUE #7 — Divergence badge + ISSUE #6 — Filter panel
# Insertion point: between card-header closing </div> and the overflow-x div
# that wraps the polls table.
#
# We replace the closing </div> of the card-header + opening of the table
# wrapper with: badge HTML + filter panel HTML + original table wrapper.
# ─────────────────────────────────────────────────────────────────────────────

# ── ISSUE #7 ─────────────────────────────────────────────────────────────────
# Badge showing divergence (range) of LLA across the last 6 polls.
# Inserted as a <div id="polls-divergence-badge"> right after card-header
# closes and before the filter panel (which is inserted by issue #6).
# The badge is populated by JS added at the end of the POLLS TABLE render block.

OLD_CARD_HEADER_END = '</div>\n                    <div style="overflow-x: auto; max-height: 650px; overflow-y: auto;">'

NEW_CARD_HEADER_END = (
    '</div>\n'
    # ── Issue #7 badge (populated by JS below) ──────────────────────────────
    '                    <div id="polls-divergence-badge" style="margin-bottom:12px;"></div>\n'
    # ── Issue #6 filter panel ───────────────────────────────────────────────
    '                    <div id="polls-filter-panel" style="\n'
    '                        display:flex; flex-wrap:wrap; gap:12px; align-items:center;\n'
    '                        padding:12px 14px; margin-bottom:14px;\n'
    '                        background:var(--bg-secondary); border:1px solid var(--border-subtle);\n'
    '                        border-radius:10px;\n'
    '                    ">\n'
    '                        <!-- Calidad -->\n'
    '                        <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">\n'
    '                            <span style="font-size:10px;font-weight:700;text-transform:uppercase;\n'
    '                                letter-spacing:.8px;color:var(--text-muted);">Calidad</span>\n'
    '                            <div style="display:flex;gap:4px;">\n'
    '                                <button class="pf-btn pf-active" data-filter="calidad" data-val="todas"\n'
    '                                    onclick="pollsFilter(\'calidad\',\'todas\',this)">Todas</button>\n'
    '                                <button class="pf-btn" data-filter="calidad" data-val="A"\n'
    '                                    onclick="pollsFilter(\'calidad\',\'A\',this)">Solo A</button>\n'
    '                                <button class="pf-btn" data-filter="calidad" data-val="AB"\n'
    '                                    onclick="pollsFilter(\'calidad\',\'AB\',this)">Solo A+B</button>\n'
    '                            </div>\n'
    '                        </div>\n'
    '                        <!-- Período -->\n'
    '                        <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">\n'
    '                            <span style="font-size:10px;font-weight:700;text-transform:uppercase;\n'
    '                                letter-spacing:.8px;color:var(--text-muted);">Período</span>\n'
    '                            <div style="display:flex;gap:4px;">\n'
    '                                <button class="pf-btn pf-active" data-filter="periodo" data-val="todos"\n'
    '                                    onclick="pollsFilter(\'periodo\',\'todos\',this)">Todos</button>\n'
    '                                <button class="pf-btn" data-filter="periodo" data-val="30"\n'
    '                                    onclick="pollsFilter(\'periodo\',\'30\',this)">Últ. 30d</button>\n'
    '                                <button class="pf-btn" data-filter="periodo" data-val="60"\n'
    '                                    onclick="pollsFilter(\'periodo\',\'60\',this)">Últ. 60d</button>\n'
    '                                <button class="pf-btn" data-filter="periodo" data-val="90"\n'
    '                                    onclick="pollsFilter(\'periodo\',\'90\',this)">Últ. 90d</button>\n'
    '                            </div>\n'
    '                        </div>\n'
    '                        <!-- Tipo -->\n'
    '                        <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">\n'
    '                            <span style="font-size:10px;font-weight:700;text-transform:uppercase;\n'
    '                                letter-spacing:.8px;color:var(--text-muted);">Tipo</span>\n'
    '                            <div style="display:flex;gap:4px;">\n'
    '                                <button class="pf-btn pf-active" data-filter="tipo" data-val="todos"\n'
    '                                    onclick="pollsFilter(\'tipo\',\'todos\',this)">Todos</button>\n'
    '                                <button class="pf-btn" data-filter="tipo" data-val="espacio"\n'
    '                                    onclick="pollsFilter(\'tipo\',\'espacio\',this)">Espacio</button>\n'
    '                                <button class="pf-btn" data-filter="tipo" data-val="candidato"\n'
    '                                    onclick="pollsFilter(\'tipo\',\'candidato\',this)">Candidato</button>\n'
    '                            </div>\n'
    '                        </div>\n'
    '                    </div>\n'
    # ── Original table wrapper ──────────────────────────────────────────────
    '                    <div style="overflow-x: auto; max-height: 650px; overflow-y: auto;">'
)

if OLD_CARD_HEADER_END in c:
    c = c.replace(OLD_CARD_HEADER_END, NEW_CARD_HEADER_END, 1)
    done.append('Issue #6 + #7 (partial): filter panel + divergence badge placeholder inserted before polls table')
else:
    done.append('FALLO Issue #6/#7: no se encontró el punto de inserción (card-header end + overflow div)')

# ─────────────────────────────────────────────────────────────────────────────
# ISSUE #6 — Filter logic (CSS + JS)
# Append pill button CSS and the pollsFilter() + renderPollsTable() functions
# right after the existing POLLS TABLE render block ends (after the forEach loop).
#
# We also append the divergence badge JS here (Issue #7).
#
# Anchor: the last line of the polls forEach block writes to pollsBody.innerHTML
# and ends with the weight bar markup. We look for the closing of that block:
# "});\n\n// CONCENTRACIÓN" which is the next comment after the polls loop.
# ─────────────────────────────────────────────────────────────────────────────

OLD_AFTER_POLLS_LOOP = '});\n\n// CONCENTRACIÓN POR CONSULTORA'

NEW_AFTER_POLLS_LOOP = (
    '});\n\n'
    '// ── ISSUE #6: Filter state & re-render ─────────────────────────────────\n'
    '(function() {\n'
    '    // Inject pill button CSS once\n'
    '    const pfStyle = document.createElement(\'style\');\n'
    '    pfStyle.textContent = `\n'
    '        .pf-btn {\n'
    '            padding: 5px 12px;\n'
    '            border-radius: 20px;\n'
    '            border: 1px solid var(--border-subtle);\n'
    '            background: var(--bg-card);\n'
    '            color: var(--text-secondary);\n'
    '            font-size: 11px;\n'
    '            font-weight: 600;\n'
    '            cursor: pointer;\n'
    '            transition: all 0.18s;\n'
    '            white-space: nowrap;\n'
    '        }\n'
    '        .pf-btn:hover:not(.pf-active) {\n'
    '            border-color: #7c3aed;\n'
    '            color: #7c3aed;\n'
    '        }\n'
    '        .pf-btn.pf-active {\n'
    '            background: #7c3aed;\n'
    '            border-color: #7c3aed;\n'
    '            color: #ffffff;\n'
    '        }\n'
    '    `;\n'
    '    document.head.appendChild(pfStyle);\n'
    '\n'
    '    // Filter state\n'
    '    const pfState = { calidad: \'todas\', periodo: \'todos\', tipo: \'todos\' };\n'
    '\n'
    '    // Render only the table rows based on current filter state\n'
    '    function renderFilteredRows() {\n'
    '        const now = new Date();\n'
    '        const body = document.getElementById(\'pollsTableBody\');\n'
    '        const maxP = Math.max(...encuestas.map(e => e.peso));\n'
    '        let filtered = encuestas.filter(e => {\n'
    '            // Calidad filter\n'
    '            if (pfState.calidad === \'A\' && e.calidad !== \'A\') return false;\n'
    '            if (pfState.calidad === \'AB\' && e.calidad !== \'A\' && e.calidad !== \'B\') return false;\n'
    '            // Período filter\n'
    '            if (pfState.periodo !== \'todos\') {\n'
    '                const days = parseInt(pfState.periodo, 10);\n'
    '                const cutoff = new Date(now.getTime() - days * 86400000);\n'
    '                if (new Date(e.fecha) < cutoff) return false;\n'
    '            }\n'
    '            // Tipo filter\n'
    '            if (pfState.tipo !== \'todos\' && e.tipo !== pfState.tipo) return false;\n'
    '            return true;\n'
    '        });\n'
    '        body.innerHTML = filtered.map(e => {\n'
    '            const f = new Date(e.fecha);\n'
    '            const fs = f.toLocaleDateString(\'es-AR\', { day: \'2-digit\', month: \'short\', year: \'2-digit\' });\n'
    '            const pp = (e.peso / maxP * 100).toFixed(0);\n'
    '            const badgeColor = e.calidad === \'A\' ? \'#16A34A\' : e.calidad === \'B\' ? \'#D97706\' : \'#6B7280\';\n'
    '            const badgeBg   = e.calidad === \'A\' ? \'#F0FDF4\' : e.calidad === \'B\' ? \'#FFFBEB\' : \'#F3F4F6\';\n'
    '            const tipoColor = e.tipo === \'candidato\' ? \'#92400E\' : \'#1D4ED8\';\n'
    '            const tipoBg    = e.tipo === \'candidato\' ? \'#FEF3C7\' : \'#EFF6FF\';\n'
    '            const tipoBd    = e.tipo === \'candidato\' ? \'#F59E0B44\' : \'#93C5FD44\';\n'
    '            const tipoLbl   = e.tipo === \'candidato\' ? \'C\' : \'E\';\n'
    '            const tipoTitle = e.tipo === \'candidato\'\n'
    '                ? \'Encuesta por candidato (incluye Villarruel)\'\n'
    '                : \'Encuesta por espacio (LLA como partido)\';\n'
    '            const pi = e.pesoInfo;\n'
    '            const tooltip = `${e.consultora} · ${e.fecha}\\nTemporal: ${pi.wT.toFixed(3)} × Calidad: ${pi.wC.toFixed(2)} × Sesgo: ${pi.wS.toFixed(2)} × Medio: ${pi.wM.toFixed(2)} × Metodología: ${pi.wMe.toFixed(2)}\\nPeso total: ${(e.peso * 100).toFixed(1)}%`;\n'
    '            return `<tr title="${tooltip}">`\n'
    '                + `<td><div style="font-weight:600;font-size:12px;">${e.consultora}`\n'
    '                + ` <span style="font-size:10px;font-weight:700;padding:1px 6px;border-radius:4px;background:${badgeBg};color:${badgeColor};border:1px solid ${badgeColor}33;">${e.calidad || \'?\'}</span>`\n'
    '                + ` <span title="${tipoTitle}" style="font-size:9px;font-weight:700;padding:1px 4px;border-radius:3px;background:${tipoBg};color:${tipoColor};border:1px solid ${tipoBd};cursor:help;">${tipoLbl}</span>`\n'
    '                + `</div><div style="font-size:10px;color:var(--text-muted);">n=${e.muestra}</div></td>`\n'
    '                + `<td style="font-size:12px;color:var(--text-muted);">${fs}</td>`\n'
    '                + `<td style="font-weight:600;color:var(--lla-color);">${e.LLA.toFixed(1)}</td>`\n'
    '                + `<td style="font-weight:600;color:var(--peronismo-color);">${e.PJ.toFixed(1)}</td>`\n'
    '                + `<td><div class="weight-bar"><div class="weight-fill" style="width:${pp}%;"></div></div>`\n'
    '                + `<span style="font-size:10px;color:var(--text-muted);">${(e.peso * 100).toFixed(0)}%</span></td>`\n'
    '                + `</tr>`;\n'
    '        }).join(\'\');\n'
    '    }\n'
    '\n'
    '    // Expose globally so onclick handlers can call it\n'
    '    window.pollsFilter = function(dimension, val, btnEl) {\n'
    '        pfState[dimension] = val;\n'
    '        // Toggle active class within the button group\n'
    '        const group = btnEl.parentElement;\n'
    '        group.querySelectorAll(\'.pf-btn\').forEach(b => b.classList.remove(\'pf-active\'));\n'
    '        btnEl.classList.add(\'pf-active\');\n'
    '        renderFilteredRows();\n'
    '    };\n'
    '\n'
    '    // ── ISSUE #7: Divergence badge ──────────────────────────────────────\n'
    '    (function renderDivergenceBadge() {\n'
    '        const last6 = encuestas.slice(0, 6);\n'
    '        if (last6.length < 2) return;\n'
    '        const llaVals = last6.map(e => e.LLA);\n'
    '        const range = Math.round((Math.max(...llaVals) - Math.min(...llaVals)) * 10) / 10;\n'
    '        const highDispersion = range > 8;\n'
    '        const badge = document.getElementById(\'polls-divergence-badge\');\n'
    '        if (!badge) return;\n'
    '        badge.innerHTML = `<span style="\n'
    '            display:inline-flex; align-items:center; gap:6px;\n'
    '            padding:5px 12px; border-radius:20px; font-size:12px; font-weight:600;\n'
    '            background:${highDispersion ? \'#854d0e22\' : \'#14532d22\'};\n'
    '            color:${highDispersion ? \'#ca8a04\' : \'#16a34a\'};\n'
    '            border:1px solid ${highDispersion ? \'#ca8a0444\' : \'#16a34a44\'};\n'
    '        ">${highDispersion ? \'⚠ Alta dispersión\' : \'✓ Baja dispersión\'}: ${range}pp entre consultoras (últimas 6)</span>`;\n'
    '    })();\n'
    '\n'
    '    // Run initial render (replaces the static forEach above for filter support)\n'
    '    // The initial full render was already done by the forEach loop above;\n'
    '    // this IIFE only sets up re-render logic for subsequent filter clicks.\n'
    '    // We re-render now so the rows are managed by renderFilteredRows from the start.\n'
    '    renderFilteredRows();\n'
    '})();\n'
    '\n'
    '// CONCENTRACIÓN POR CONSULTORA'
)

if OLD_AFTER_POLLS_LOOP in c:
    c = c.replace(OLD_AFTER_POLLS_LOOP, NEW_AFTER_POLLS_LOOP, 1)
    done.append('Issue #6 + #7 (JS): filter logic, renderFilteredRows(), pollsFilter(), divergence badge JS injected after polls forEach loop')
else:
    done.append('FALLO Issue #6/#7 (JS): no se encontró el cierre del forEach loop de encuestas')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('=== patch_issues6_7.py aplicado ===')
for d in done:
    print(f'  ✓ {d}')
print(f'File: {len(c)} chars (era {orig}, delta +{len(c)-orig})')
