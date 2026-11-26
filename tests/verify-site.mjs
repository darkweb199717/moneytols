// Run: node tests/verify-site.mjs (Node.js 18+)
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const root = new URL('../', import.meta.url);
const read = p => readFileSync(new URL(p, root), 'utf8');
const routes = [
 ['debt-consolidation-loan-calculator','consolidation','Debt Consolidation Loan Calculator'],
 ['mortgage-refinance-calculator','refinance','Mortgage Refinance Calculator'],
 ['business-loan-calculator','business','Business Loan Calculator'],
 ['home-equity-loan-calculator','equity','Home Equity Loan Calculator'],
 ['life-insurance-cost-calculator','insurance','Life Insurance Cost Calculator']
];
const sitemap=read('sitemap.xml'), home=read('index.html');
assert.match(sitemap, /https:\/\/moneytols\.com\//);
for (const [slug,id,title] of routes){
 const html=read(slug+'/index.html');
 assert.ok(html.includes('<title>'+title+' | MoneyTols</title>'),slug+' title');
 assert.ok(html.includes('href="https://moneytols.com/'+slug+'/" rel="canonical"'),slug+' canonical');
 assert.ok(html.includes('id="page-'+id+'"'),slug+' content');
 assert.ok(html.includes('class="ftc-page active" id="page-'+id+'"'),slug+' active page');
 assert.equal((html.match(/class="ftc-page active"/g)||[]).length,1,slug+' duplicate active pages');
 assert.ok(sitemap.includes('https://moneytols.com/'+slug+'/'),slug+' sitemap');
 assert.ok(home.includes('href="/'+slug+'/"'),slug+' homepage link');
 assert.ok(!html.includes('abscloud.org'),slug+' no Popunder');
 assert.ok(!html.includes('a013675ad0e434ae622a2e2a19ceb1a4'),slug+' no Social Bar');
 for(const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g))JSON.parse(m[1]);
}
assert.equal((home.match(/class="tols-ad-slot tols-ad-slot--desktop-only"/g)||[]).length,1,'only one banner');
assert.equal((home.match(/<section aria-label="Sponsored offers"/g)||[]).length,5,'sponsored links preserved');
assert.ok(!home.includes('abscloud.org')&&!home.includes('a013675ad0e434ae622a2e2a19ceb1a4'),'removed page-level ads');
const payment=(p,apr,months)=>{const r=apr/1200;return r===0?p/months:p*r/(1-Math.pow(1+r,-months));};
assert.ok(Math.abs(payment(12000,0,12)-1000)<1e-6,'zero percent loan');
assert.ok(Math.abs(payment(12000,12,12)-1066.185464)<0.01,'standard amortization');
console.log('PASS: homepage, calculator SEO routes, sitemap, preserved ads and formula examples');
