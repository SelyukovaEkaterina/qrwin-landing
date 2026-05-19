import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://qrstars.ru',
  integrations: [tailwind()],
  trailingSlash: 'never',
  build: {
    format: 'file',
  },
});
