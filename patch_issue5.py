import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\web\votometro.html'
with open(path, encoding='utf-8') as f:
    c = f.read()
orig = len(c)
done = []

# ─────────────────────────────────────────────────────────────────────────────
# CHANGE 1: Insert Villarruel panel HTML after the firstRoundAnalysis section
# (after </section> that closes the Primera Vuelta card, before the Ballotage section)
# ─────────────────────────────────────────────────────────────────────────────

ANCHOR_HTML = '''                    <!-- Analysis box -->
                    <div id="firstRoundAnalysis" style="margin-top: 18px; padding: 18px 20px; background: var(--celeste-pale); border: 1px solid var(--border-subtle); border-radius: 10px; font-size: 14px; color: var(--text-secondary); line-height: 1.7;"></div>
                </section>

                <!-- ========== BALLOTAGE — DISEÑO DIFERENCIADO ========== -->'''

VILLARRUEL_PANEL = '''                    <!-- Analysis box -->
                    <div id="firstRoundAnalysis" style="margin-top: 18px; padding: 18px 20px; background: var(--celeste-pale); border: 1px solid var(--border-subtle); border-radius: 10px; font-size: 14px; color: var(--text-secondary); line-height: 1.7;"></div>
                </section>

                <!-- ========== VILLARRUEL COMO CANDIDATA — ISSUE #5 ========== -->
                <section id="villarruelPanel" style="margin-bottom: 28px; border-radius: 16px; overflow: hidden; box-shadow: var(--shadow-lg); border: 1px solid #78350f;">
                    <!-- Panel header -->
                    <details>
                        <summary style="background: linear-gradient(135deg, #1c1917 0%, #292524 100%); padding: 20px 28px; display: flex; align-items: center; gap: 14px; cursor: pointer; list-style: none; outline: none; user-select: none;">
                            <span style="display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:50%;background:rgba(251,191,36,0.2);color:#fbbf24;font-size:15px;border:1px solid rgba(251,191,36,0.4);flex-shrink:0;">★</span>
                            <div style="flex:1;">
                                <div style="font-family:'DM Serif Display',serif;font-size:19px;font-weight:400;color:#fde68a;margin:0;">Escenario con Villarruel como candidata</div>
                                <div style="font-size:11px;color:rgba(253,230,138,0.6);margin-top:2px;text-transform:uppercase;letter-spacing:1.5px;">Análisis de impacto en primera vuelta · CB Global feb-2026</div>
                            </div>
                            <span id="villarruelToggleIcon" style="font-size:12px;color:#fbbf24;text-transform:uppercase;letter-spacing:1px;font-weight:700;padding:5px 14px;border:1px solid rgba(251,191,36,0.4);border-radius:100px;background:rgba(251,191,36,0.1);">▼ Ver escenario</span>
                        </summary>

                        <div style="background: #1c1917; border-top: 1px solid #78350f; padding: 24px 28px;">

                            <!-- Toggle switch row -->
                            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;margin-bottom:24px;padding:14px 18px;background:#292524;border-radius:10px;border:1px solid #44403c;">
                                <div>
                                    <div style="font-size:14px;font-weight:700;color:#fde68a;margin-bottom:3px;">Villarruel se presenta como candidata independiente</div>
                                    <div style="font-size:12px;color:#a8a29e;">CB Global feb-2026: 5.2% intención de voto (piso 4.1% · techo 19.4%)</div>
                                </div>
                                <label style="display:inline-flex;align-items:center;gap:10px;cursor:pointer;">
                                    <span style="font-size:12px;color:#a8a29e;" id="villToggleLabel">Desactivado</span>
                                    <div style="position:relative;width:48px;height:26px;">
                                        <input type="checkbox" id="villarruelToggle" style="opacity:0;width:0;height:0;position:absolute;" onchange="runVillarruelScenario()">
                                        <span id="villSliderTrack" style="position:absolute;inset:0;border-radius:13px;background:#44403c;transition:background 0.3s;cursor:pointer;"></span>
                                        <span id="villSliderThumb" style="position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#a8a29e;transition:all 0.3s;cursor:pointer;"></span>
                                    </div>
                                </label>
                            </div>

                            <!-- Results: side by side -->
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px;" id="villResultsGrid">

                                <!-- Sin Villarruel -->
                                <div style="background:#292524;border:1px solid #44403c;border-radius:12px;padding:18px;text-align:center;">
                                    <div style="font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#a8a29e;margin-bottom:12px;font-weight:700;">Sin Villarruel · Escenario base</div>
                                    <div style="display:flex;flex-direction:column;gap:8px;">
                                        <div>
                                            <div style="font-size:11px;color:#78716c;margin-bottom:2px;">LLA (Milei)</div>
                                            <div id="villBaseLLA" style="font-family:'JetBrains Mono',monospace;font-size:28px;font-weight:700;color:#c084fc;">—</div>
                                        </div>
                                        <div style="height:1px;background:#44403c;"></div>
                                        <div id="villBaseResult" style="font-size:13px;font-weight:600;color:#a8a29e;padding:6px 0;">—</div>
                                        <div>
                                            <div style="font-size:10px;color:#78716c;margin-bottom:2px;">1ª Vuelta directa</div>
                                            <div id="villBaseP1V" style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;color:#fbbf24;">—</div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Con Villarruel -->
                                <div style="background:#1c1917;border:2px solid #92400e;border-radius:12px;padding:18px;text-align:center;transition:border-color 0.3s;" id="villAltCard">
                                    <div style="font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#fbbf24;margin-bottom:12px;font-weight:700;">Con Villarruel · Escenario alternativo</div>
                                    <div style="display:flex;flex-direction:column;gap:8px;" id="villAltContent">
                                        <div style="text-align:center;color:#57534e;padding:20px 0;font-size:13px;">Activar toggle para calcular</div>
                                    </div>
                                </div>

                            </div>

                            <!-- Comparison bar -->
                            <div id="villCompBar" style="display:none;margin-bottom:16px;padding:14px 18px;background:#292524;border-radius:10px;border:1px solid #44403c;">
                                <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#a8a29e;font-weight:700;margin-bottom:10px;">Impacto sobre probabilidad de 1ª vuelta directa</div>
                                <div style="display:flex;align-items:center;gap:12px;">
                                    <span style="font-size:11px;color:#a8a29e;min-width:90px;">Sin Villarruel</span>
                                    <div style="flex:1;height:24px;background:#3f3f46;border-radius:12px;overflow:hidden;">
                                        <div id="villBaseBar" style="height:100%;background:linear-gradient(90deg,#7c3aed,#a78bfa);border-radius:12px;transition:width 0.8s ease-out;width:0%;display:flex;align-items:center;padding:0 8px;">
                                            <span id="villBaseBarLabel" style="font-size:10px;font-weight:700;color:white;"></span>
                                        </div>
                                    </div>
                                </div>
                                <div style="display:flex;align-items:center;gap:12px;margin-top:8px;">
                                    <span style="font-size:11px;color:#fbbf24;min-width:90px;">Con Villarruel</span>
                                    <div style="flex:1;height:24px;background:#3f3f46;border-radius:12px;overflow:hidden;">
                                        <div id="villAltBar" style="height:100%;background:linear-gradient(90deg,#b45309,#fbbf24);border-radius:12px;transition:width 0.8s ease-out;width:0%;display:flex;align-items:center;padding:0 8px;">
                                            <span id="villAltBarLabel" style="font-size:10px;font-weight:700;color:white;"></span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Footnote -->
                            <div style="font-size:11px;color:#57534e;border-top:1px solid #292524;padding-top:12px;line-height:1.6;">
                                <strong style="color:#78716c;">Metodología:</strong> LLA_adj = LLA_media − 5.2pp (puntos transferidos a Villarruel).
                                Se aplican los mismos umbrales constitucionales: Art. 97 (≥45%) y Art. 98 (≥40% con +10pp sobre PJ).
                                Simulación Monte Carlo 10.000 iteraciones con σ=6.5%, correlación LLA-PJ ρ=−0.7.
                                Fuente: CB Global Data, febrero 2026.
                            </div>

                        </div>
                    </details>
                </section>

                <!-- ========== BALLOTAGE — DISEÑO DIFERENCIADO ========== -->'''

if ANCHOR_HTML in c:
    c = c.replace(ANCHOR_HTML, VILLARRUEL_PANEL, 1)
    done.append('OK  [1] Panel HTML de Villarruel insertado despues de firstRoundAnalysis')
else:
    done.append('FAIL [1] No se encontro el anchor HTML para insertar el panel Villarruel')

# ─────────────────────────────────────────────────────────────────────────────
# CHANGE 2: Insert runVillarruelScenario() JS function before closing </script>
# ─────────────────────────────────────────────────────────────────────────────

ANCHOR_JS = '''// Restore saved preference on load
(function() {
    const saved = localStorage.getItem('cigob_theme');'''

VILLARRUEL_JS = '''// ── VILLARRUEL SCENARIO (Issue #5) ──────────────────────────────────────────
// Datos base: CB Global Data feb-2026
// Villarruel intención: 5.2% (piso 4.1%, techo 19.4%)
const VILL_PCT = 5.2;    // puntos que Villarruel toma de LLA
const VILL_SIGMA = 6.5;  // mismo sigma calibrado que el modelo base
const VILL_SIM = 10000;

function runVillarruelScenario() {
    const toggle = document.getElementById('villarruelToggle');
    const label  = document.getElementById('villToggleLabel');
    const track  = document.getElementById('villSliderTrack');
    const thumb  = document.getElementById('villSliderThumb');
    const altCard = document.getElementById('villAltCard');
    const compBar = document.getElementById('villCompBar');

    // --- populate base scenario (always) ---
    // media.LLA and pMilei1 are already computed in the outer Monte Carlo scope
    const baseLLA = media.LLA;
    const basePJ  = media.PJ;
    const baseP1V = pMilei1; // already a percentage (0-100)

    document.getElementById('villBaseLLA').textContent  = baseLLA.toFixed(1) + '%';
    document.getElementById('villBaseP1V').textContent  = baseP1V.toFixed(1) + '%';

    // base result label
    const df_base = baseLLA - basePJ;
    let baseLabel;
    if (baseLLA >= 45) {
        baseLabel = 'Gana 1ª vuelta (Art. 97)';
    } else if (baseLLA >= 40 && df_base > 10) {
        baseLabel = 'Posible 1ª vuelta (Art. 98)';
    } else {
        baseLabel = 'Ballotage probable';
    }
    document.getElementById('villBaseResult').textContent = baseLabel;

    if (!toggle.checked) {
        // toggle off — reset alt card
        label.textContent = 'Desactivado';
        track.style.background = '#44403c';
        thumb.style.left = '3px';
        thumb.style.background = '#a8a29e';
        altCard.style.borderColor = '#92400e';
        compBar.style.display = 'none';
        document.getElementById('villAltContent').innerHTML =
            '<div style="text-align:center;color:#57534e;padding:20px 0;font-size:13px;">Activar toggle para calcular</div>';
        return;
    }

    // toggle on
    label.textContent = 'Activado';
    track.style.background = '#b45309';
    thumb.style.left = '25px';
    thumb.style.background = '#fbbf24';
    altCard.style.borderColor = '#fbbf24';

    // --- compute adjusted scenario ---
    const adjLLA = baseLLA - VILL_PCT;   // LLA loses 5.2pp to Villarruel
    const adjPJ  = basePJ;               // PJ unchanged
    const df_adj = adjLLA - adjPJ;

    // Re-run Monte Carlo with adjusted LLA mean
    // Reuse seeded PRNG state — reset seed to same date so results are reproducible
    function hashStr(s) { let h=0; for(let i=0;i<s.length;i++){h=Math.imul(31,h)+s.charCodeAt(i)|0;} return h>>>0; }
    let rng = hashStr('vill-' + FECHA_REF.getFullYear() + '-' + FECHA_REF.getMonth() + '-' + FECHA_REF.getDate());
    function rand() { let t=rng+=0x6D2B79F5; t=Math.imul(t^t>>>15,t|1); t^=t+Math.imul(t^t>>>7,t|61); return((t^t>>>14)>>>0)/4294967296; }
    function randn2() { let u=rand()||1e-10, v=rand(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }

    const RHO = -0.7;
    let winAdj1 = 0;
    for (let i = 0; i < VILL_SIM; i++) {
        const z1 = randn2(), z2 = randn2();
        const lla = adjLLA + z1 * VILL_SIGMA;
        const pj  = adjPJ  + (RHO * z1 + Math.sqrt(1 - RHO * RHO) * z2) * VILL_SIGMA;
        const diff = lla - pj;
        if (lla >= 45 || (lla >= 40 && diff > 10)) winAdj1++;
    }
    const pAdj1V = (winAdj1 / VILL_SIM * 100);

    // result label for adjusted scenario
    let adjLabel;
    if (adjLLA >= 45) {
        adjLabel = 'Gana 1ª vuelta (Art. 97)';
    } else if (adjLLA >= 40 && df_adj > 10) {
        adjLabel = 'Posible 1ª vuelta (Art. 98)';
    } else {
        adjLabel = 'Ballotage probable';
    }

    // Color for adjusted 1V probability (amber/red scale based on change)
    const delta = pAdj1V - baseP1V;
    const deltaStr = delta >= 0 ? ('+' + delta.toFixed(1)) : delta.toFixed(1);
    const deltaColor = delta < -2 ? '#f87171' : delta > 2 ? '#4ade80' : '#fbbf24';

    // Render alt card content
    document.getElementById('villAltContent').innerHTML = `
        <div>
            <div style="font-size:11px;color:#78716c;margin-bottom:2px;">LLA (Milei adj.)</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:28px;font-weight:700;color:#fb923c;">${adjLLA.toFixed(1)}%</div>
        </div>
        <div style="font-size:11px;color:#78716c;">Villarruel: <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:#fbbf24;">${VILL_PCT.toFixed(1)}%</span>
            &nbsp;·&nbsp; Combinado: <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:#a78bfa;">${(adjLLA+VILL_PCT).toFixed(1)}%</span></div>
        <div style="height:1px;background:#44403c;"></div>
        <div style="font-size:13px;font-weight:600;color:#fbbf24;padding:4px 0;">${adjLabel}</div>
        <div>
            <div style="font-size:10px;color:#78716c;margin-bottom:2px;">1ª Vuelta directa</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;color:#fbbf24;">${pAdj1V.toFixed(1)}%</div>
        </div>
        <div style="font-size:11px;padding:6px 10px;border-radius:6px;background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.2);">
            Variacion vs base: <span style="font-family:'JetBrains Mono',monospace;font-weight:700;color:${deltaColor};">${deltaStr}pp</span>
        </div>
    `;

    // Comparison bar
    compBar.style.display = 'block';
    const maxPct = Math.max(baseP1V, pAdj1V, 1);
    const baseW  = (baseP1V  / 100 * 100).toFixed(1);
    const altW   = (pAdj1V   / 100 * 100).toFixed(1);
    document.getElementById('villBaseBarLabel').textContent = baseP1V.toFixed(1) + '%';
    document.getElementById('villAltBarLabel').textContent  = pAdj1V.toFixed(1) + '%';
    setTimeout(() => {
        document.getElementById('villBaseBar').style.width = baseW + '%';
        document.getElementById('villAltBar').style.width  = altW  + '%';
    }, 100);
}

// Initialize base values on page load (before toggle is touched)
document.addEventListener('DOMContentLoaded', function() {
    // Defer until after the Monte Carlo block has run (it's synchronous, so this fires after)
    setTimeout(runVillarruelScenario, 50);
});

// ── END VILLARRUEL SCENARIO ──────────────────────────────────────────────────

// Restore saved preference on load
(function() {
    const saved = localStorage.getItem('cigob_theme');'''

if ANCHOR_JS in c:
    c = c.replace(ANCHOR_JS, VILLARRUEL_JS, 1)
    done.append('OK  [2] Funcion JS runVillarruelScenario() insertada antes del cierre de script')
else:
    done.append('FAIL [2] No se encontro el anchor JS para insertar la funcion Villarruel')

# ─────────────────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────────────────
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('patch_issue5.py — Resultados:')
for d in done:
    print(f'  {d}')
print(f'Archivo: {len(c):,} chars (era {orig:,}, delta {len(c)-orig:+,})')
