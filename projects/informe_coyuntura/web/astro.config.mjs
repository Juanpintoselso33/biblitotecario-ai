import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://juanpintoselso33.github.io',
  base: '/biblitotecario-ai/informe',
  outDir: '../../../web/informe',
  build: { format: 'directory', assets: '_assets' },
});
