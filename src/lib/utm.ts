const ATTRIBUTION_QUERY_KEYS = ['yclid', 'ymclid'] as const;

/** Append utm_* and attribution query params from the landing page URL to outbound app links. */
export function appendAttributionParams(baseUrl: string, searchParams: URLSearchParams): string {
  try {
    const url = new URL(baseUrl);
    for (const [key, value] of searchParams.entries()) {
      if (key.startsWith('utm_') && !url.searchParams.has(key)) {
        url.searchParams.set(key, value);
      }
    }
    for (const key of ATTRIBUTION_QUERY_KEYS) {
      const value = searchParams.get(key);
      if (value && !url.searchParams.has(key)) {
        url.searchParams.set(key, value);
      }
    }
    return url.toString();
  } catch {
    return baseUrl;
  }
}

export const appendUtm = appendAttributionParams;

export function isAppUrl(href: string): boolean {
  return href.startsWith('https://app.qrstars.ru');
}

export const REVIEWS_LANDING_SLUGS = new Set([
  'qr-kod-dlya-yandeks-kart',
  'qr-kod-dlya-2gis',
  'qr-kod-dlya-otzyvov',
  'qr-kod-dlya-salona-krasoty',
  'qr-kod-dlya-stomatologii',
  'qr-kod-dlya-avtoservisa',
]);

export const MENU_LANDING_SLUGS = new Set(['qr-kod-dlya-restorana']);

export const MENU_LANDING_PATHS = new Set([
  '/qr-menu.html',
  '/qr-kod-dlya-restorana.html',
  '/blog/qr-kod-dlya-menu-restorana.html',
]);

/** Register URL for menu intent pages with campaign-specific utm_content. */
export function menuRegisterUrl(
  content: string,
  searchParams: URLSearchParams,
  medium: 'seo' | 'cpc' = 'seo',
): string {
  const base = `https://app.qrstars.ru/register?utm_source=qrstars&utm_medium=${medium}&utm_campaign=menu_search&utm_content=${content}`;
  return appendAttributionParams(base, searchParams);
}
