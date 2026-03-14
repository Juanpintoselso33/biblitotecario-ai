import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\web\votometro.html', encoding='utf-8') as f:
    c = f.read()

orig = len(c)
done = []

# BUG 1: FECHA_REF dinámica rompe el counter de "Actualizado hace X días"
# Solución: mantener FECHA_REF = new Date() para temporal weighting,
#           añadir ULTIMA_ACTUALIZACION para el counter
c = c.replace(
    "const FECHA_REF = new Date(); // dinámica — ponderación se recalcula con el calendario real",
    "const FECHA_REF = new Date(); // dinámica — ponderación temporal recalculada en tiempo real\n"
    "const ULTIMA_ACTUALIZACION = new Date('2026-03-01'); // última encuesta agregada manualmente",
    1
)
done.append('BUG1a: añade ULTIMA_ACTUALIZACION')

c = c.replace(
    "const diasDesdeRef = Math.floor((new Date() - FECHA_REF) / 864e5);",
    "const diasDesdeRef = Math.floor((new Date() - ULTIMA_ACTUALIZACION) / 864e5);",
    1
)
done.append('BUG1b: diasDesdeRef usa ULTIMA_ACTUALIZACION')

# BUG 2: footer date hardcodeada
old_footer = "document.getElementById('footerSources').innerHTML = `Actualizado: 1 de marzo de 2026 · "
new_footer = ("document.getElementById('footerSources').innerHTML = "
              "`Actualizado: ${ULTIMA_ACTUALIZACION.toLocaleDateString('es-AR',{day:'numeric',month:'long',year:'numeric'})} · ")
if old_footer in c:
    c = c.replace(old_footer, new_footer, 1)
    done.append('BUG2: footer date dinámico')
else:
    done.append('BUG2: footer NOT FOUND')

# BUG 3: Giacobbe warning nunca dispara con cap al 20%
# El warning threshold estaba en >25% pero el cap lo reduce a 20%
# Nuevo approach: mostrar info de qué consultora tiene más peso post-cap
old_warn_header = '// GIACOBBE CONCENTRATION WARNING\n(function() {\n'
new_warn_header = '// CONCENTRACIÓN POR CONSULTORA — info post-cap\n(function() {\n'
if old_warn_header in c:
    c = c.replace(old_warn_header, new_warn_header, 1)
    done.append('BUG3a: renombra warning header')

old_warn_body = ("    const giacP = encuestas.filter(e => e.consultora === 'Giacobbe');\n"
                 "    const totalW = encuestas.reduce((s,e)=>s+e.peso,0);\n"
                 "    const giacW = giacP.reduce((s,e)=>s+e.peso,0);\n"
                 "    const pct = totalW > 0 ? (giacW/totalW*100) : 0;\n"
                 "    if (pct > 25) {\n"
                 "        const note = document.createElement('div');\n"
                 "        note.style.cssText = 'font-size:11px;color:#92400E;background:#FEF3C7;border:1px solid #F59E0B;'+\n"
                 "            'border-radius:6px;padding:8px 12px;margin-top:8px;';\n"
                 "        note.innerHTML = '&#9888; <strong>Concentración Giacobbe: ' + pct.toFixed(0) + '%</strong> '+\n"
                 "            'del peso total del modelo proviene de Giacobbe. Alta dependencia de una sola consultora.';\n"
                 "        const tbl = document.getElementById('pollsTableBody');\n"
                 "        if (tbl && tbl.parentElement) tbl.parentElement.parentElement.appendChild(note);\n"
                 "    }\n"
                 "})();")
new_warn_body = ("    const allW = encuestas.reduce((s,e)=>s+e.peso,0);\n"
                 "    const byC = {};\n"
                 "    encuestas.forEach(e=>{ byC[e.consultora]=(byC[e.consultora]||0)+e.peso; });\n"
                 "    const top = Object.entries(byC).sort((a,b)=>b[1]-a[1])[0];\n"
                 "    if (top && (top[1]/allW*100) > 15) {\n"
                 "        const note = document.createElement('div');\n"
                 "        note.style.cssText = 'font-size:11px;color:#1D4ED8;background:#EFF6FF;border:1px solid #93C5FD;border-radius:6px;padding:8px 12px;margin-top:8px;';\n"
                 "        note.innerHTML = '&#9432; Cap de peso activo: <strong>' + top[0] + '</strong> concentra el ' +\n"
                 "            (top[1]/allW*100).toFixed(0) + '% del peso tras aplicar el límite del 20% por consultora.';\n"
                 "        const tbl = document.getElementById('pollsTableBody');\n"
                 "        if (tbl && tbl.parentElement) tbl.parentElement.parentElement.appendChild(note);\n"
                 "    }\n"
                 "})();")
if old_warn_body in c:
    c = c.replace(old_warn_body, new_warn_body, 1)
    done.append('BUG3b: warning threshold ajustado para funcionar con cap 20%')
else:
    done.append('BUG3b: NOT FOUND')

with open(r'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\web\votometro.html', 'w', encoding='utf-8') as f:
    f.write(c)

for d in done:
    print(f'  {d}')
print(f'File: {len(c)} chars (era {orig})')
