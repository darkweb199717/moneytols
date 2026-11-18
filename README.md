# MoneyTols — Adsterra v2.2 (PRE-DEPLOYMENT REVIEW)

This package includes the full site (`index.html`), `favicon.ico` and `images/`.
No live website or GitHub repository was changed.

## Code-level changes

- The two `bauval.org` URLs are consolidated in `MONEYTOLS_AD_SOURCES`; they match the code snippets supplied by the site owner.
- Existing banner, Native Banner and page-level units are tagged at runtime with `data-moneytols-ad-role` (banner, banner-options, native, page-level). This distinguishes non-banner page scripts when testing banner settings.
- Page-level scripts are protected against accidental duplicate injection. Both URLs and IDs remain unchanged.
- Native slots are initialized only if the expected container is present.
- No changes to calculator functions, ad placement counts, styling, frequency caps, or sponsored links.

## MUST VERIFY IN THE ADSTERRA DASHBOARD BEFORE DEPLOYING

Open Adsterra > Websites > moneytols.com > Get Code for each ad unit. Compare the exact URL, ad key and status:

- 728x90 iframe: `https://bauval.org/22/de92a391780c180a5e472f0280631943` (user-supplied snippet)
- Native Banner: `https://bauval.org/21/fbb9b329ee7b2d4250e4a39a44b8fd66` (user-supplied snippet)
- Existing page-level script 1: `https://gigglehiccup.com/a0/13/67/a013675ad0e434ae622a2e2a19ceb1a4.js` (NOT dashboard verified)
- Existing page-level script 2: `https://gigglehiccup.com/88/fe/24/88fe24305dd70c11f5ee2fb12de9239a.js` (NOT dashboard verified)

Do not publish unless the URLs and IDs are confirmed by the site owner inside their Adsterra account. A URL appearing in the HTML or matching a user message does not prove that the network currently authorizes it. Ad network script domains can change.

## QA instructions

- Test a desktop width > 767px and a mobile width <= 767px. Hidden banner slots should make no requests.
- When testing iframe `atOptions`, include only dynamically created script elements marked `data-moneytols-ad-role="banner"`, not `page-level` or `native` scripts. A page-level script seeing the last banner's global options is not an actual key/size mismatch.
- Verify native and banner rendering with a real browser and network access, and confirm they generate Adsterra impressions. Static checks do not confirm ad network delivery.
- Verify the two page-level units in the Adsterra dashboard and inspect user experience and applicable privacy/consent settings.

## Static checks performed

- Inline JS syntax via Node.js `--check`
- JSON-LD parsed successfully
- 63 existing ad slots, 9 Native Banner placeholders, 5 sponsored offer bars, 9 page sections
- No duplicate DOM IDs
