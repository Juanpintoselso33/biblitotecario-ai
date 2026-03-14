const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const URL = 'https://juanpintoselso33.github.io/biblitotecario-ai/votometro.html';
const OUT = 'C:\Users\trico\OneDrive\UBA\Analisis CIGOB\output\review_screenshots';

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  const errors = [];
  const warnings = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
    if (msg.type() === 'warning') warnings.push(msg.text());
  });
  page.on('pageerror', err => errors.push('PAGE ERROR: ' + err.message));

  console.log('Cargando página...');
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  // Screenshot 1: hero / resultados principales
  await page.screenshot({ path: path.join(OUT, '01_hero.png'), fullPage: false });
  console.log('✓ Screenshot 01_hero');

  // Screenshot 2: página completa
  await page.screenshot({ path: path.join(OUT, '02_full.png'), fullPage: true });
  console.log('✓ Screenshot 02_full');

  // Check elementos clave
  const checks = [
    { sel: '#pollsTableBody', label: 'Tabla de encuestas (pollsTableBody)' },
    { sel: '#polls-filter-panel', label: 'Panel de filtros (#6)' },
    { sel: '#polls-divergence-badge', label: 'Badge divergencia (#7)' },
    { sel: 'a[href][target="_blank"]', label: 'Links a fuentes (#8)' },
    { sel: 'details', label: 'Panel colapsable Villarruel (#5)' },
    { sel: '#footerSources', label: 'Footer con fecha' },
  ];

  console.log('\n=== CHECKS DE ELEMENTOS ===');
  for (const c of checks) {
    const el = await page.$(c.sel);
    if (el) {
      const visible = await el.isVisible();
      console.log(`  ${visible ? '✓' : '⚠ HIDDEN'} ${c.label}`);
    } else {
      console.log(`  ✗ MISSING ${c.label}`);
    }
  }

  // Check footer date
  const footer = await page.$eval('#footerSources', el => el.innerText).catch(() => 'N/A');
  console.log(`\n  Footer text: "${footer.substring(0, 80)}"`);

  // Check días desde actualización
  const diasEl = await page.$('#diasDesdeRef');
  if (!diasEl) {
    // try to find it via text
    const bodyText = await page.evaluate(() => document.body.innerText);
    const match = bodyText.match(/Actualizado hace (\d+) días?/);
    console.log(`  Counter días: ${match ? match[0] : 'no encontrado'}`);
  }

  // Screenshot 3: tabla de encuestas (scroll down)
  const tabla = await page.$('#pollsTableBody');
  if (tabla) {
    await tabla.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUT, '03_tabla.png'), fullPage: false });
    console.log('✓ Screenshot 03_tabla');
  }

  // Screenshot 4: panel Villarruel
  const details = await page.$('details');
  if (details) {
    await details.evaluate(el => el.open = true);
    await details.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUT, '04_villarruel.png'), fullPage: false });
    console.log('✓ Screenshot 04_villarruel');
  }

  // Test filtros
  const filterBtns = await page.$$('#polls-filter-panel button');
  console.log(`\n  Botones de filtro encontrados: ${filterBtns.length}`);

  // Check divergence badge text
  const badge = await page.$('#polls-divergence-badge');
  if (badge) {
    const txt = await badge.innerText();
    console.log(`  Badge divergencia: "${txt}"`);
  }

  // Scroll to top, screenshot final state
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(300);

  // Mobile screenshot
  await page.setViewportSize({ width: 390, height: 844 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT, '05_mobile.png'), fullPage: false });
  console.log('✓ Screenshot 05_mobile');

  console.log('\n=== ERRORES JS ===');
  if (errors.length === 0) console.log('  Ninguno ✓');
  else errors.forEach(e => console.log('  ✗ ' + e));

  console.log('\n=== WARNINGS JS ===');
  if (warnings.length === 0) console.log('  Ninguno ✓');
  else warnings.slice(0, 10).forEach(w => console.log('  ⚠ ' + w));

  await browser.close();
  console.log(`\nScreenshots en: ${OUT}`);
})();
