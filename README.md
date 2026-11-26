# MoneyTols

MoneyTols is a free collection of five financial planning calculators. The site uses its existing single-file HTML design as a **shared template**: every calculator URL contains its own `index.html` copy so it can be loaded directly on static hosting, without server rewrites.

## Pages

- `/` — homepage and calculator navigation
- `/debt-consolidation-loan-calculator/`
- `/mortgage-refinance-calculator/`
- `/business-loan-calculator/`
- `/home-equity-loan-calculator/`
- `/life-insurance-cost-calculator/`

Each calculator URL has a page-specific title, meta description, canonical, social sharing information, visible active calculator, and structured data. `sitemap.xml` enumerates these URLs.

## Advertising

Only one **728×90 banner slot** remains on the homepage; the site's existing five sponsored-offer link sections are preserved. The old Popunder and Social Bar integrations are removed. Banner loading, if available, still depends on the advertising network and browser. Avoid duplicating the banner script.

## Quality checks

Run `node tests/verify-site.mjs` on Node.js 18+ after editing the site.

Checks cover page metadata, sitemap links, active calculator pages, removal of old ad scripts, preserved banner/sponsored sections, JSON-LD parseability and example payment math. These are **smoke checks**, not complete browser, accessibility or financial-formula validation.

After merging and deployment, manually test all five URLs, back/forward navigation, mobile responsiveness, page source, ad display, calculation error states and Google Search Console indexing. Confirm that all new calculator URL paths serve 200 responses instead of a fallback or 404.

### Keep copies in sync

Because each calculator route currently carries a full HTML document, any future styling, calculator logic or privacy changes should be applied consistently to all six HTML files. For a future refactor, consider a shared build process to generate pages from one template.

## Financial information

Calculations are illustrative and are not financial, lending, legal or insurance advice. Sources linked on the pages provide general consumer information but do not endorse MoneyTols. No named expert review or editorial certification is claimed.

## Existing assets

Preserve `favicon.ico`, `images/` and `robots.txt`. Verify production social preview image responses and dimensions before releasing.
