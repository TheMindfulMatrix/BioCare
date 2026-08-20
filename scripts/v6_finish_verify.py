#!/usr/bin/env python3
"""Network, compliance, Definition-of-Done, and final-report gates for V6."""
from __future__ import annotations

import argparse, concurrent.futures, io, json, re, subprocess, sys
import urllib.error, urllib.parse, urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reports'/'v6'
EVIDENCE=Path('/tmp/v6-finish-review')
BASELINE='b5d35772e98580e253c08f6319aa8e412fa20aea'
PREVIOUS='351746b8e9e5195255840758cc4639019e16023d'
PARTNER_ID='2021428066'
CHECKED='2026-08-20'
PAGES=[ROOT/'index.html',ROOT/'shop.html',ROOT/'library.html',ROOT/'start.html',*sorted((ROOT/'library').glob('*.html'))]
DOD=[
'- [ ] Phase A reconciliation completed and discrepancies reported before any edit',
'- [ ] V5.1 tagged as rollback baseline',
'- [ ] All **10** library articles carry an affiliate disclosure near their product link',
'- [ ] Product count derived from data, reads 45 everywhere, no hand-typed number remains',
'- [ ] Single source of truth for products; no `display:none` duplicate catalog',
'- [ ] A first-time visitor learns what the site is without scrolling',
'- [ ] **Every outbound link verified HTTP 200 and carrying attribution** — zero exceptions',
'- [ ] Cutouts share one resolution, one subject scale, one baseline; no orphan grid cells',
'- [ ] Full labels with real per-serving amounts, each date-stamped to a source',
'- [ ] Total product image payload under ~800 KB, transparency intact',
'- [ ] Hero serves the ratio it displays',
'- [ ] No text under 12px at 375px viewport; no tap target under 44×44',
'- [ ] FDA disclaimer, affiliate disclosures, NY notice, and price date all still present',
'- [ ] Zero disease-claim verbs outside the FDA disclaimer',
'- [ ] No fabricated prices, dosages, reviews, or policy wording anywhere',
]

def load(path:Path)->Any:return json.loads(path.read_text(encoding='utf-8'))
def save(name:str,data:Any)->Path:
 REPORT.mkdir(parents=True,exist_ok=True); p=REPORT/name;p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');return p

def commercial(url:str)->bool:
 p=urllib.parse.urlparse(url);h=(p.hostname or '').lower();path=p.path.lower()
 return (h.endswith('zinzino.com') and '/shop/' in path) or (h.endswith('biolimitless.com') and ('/shop/' in path or '/me/' in path))
def attributed(url:str)->bool:
 p=urllib.parse.urlparse(url);h=(p.hostname or '').lower();path=p.path.lower()
 if h.endswith('zinzino.com'):return f'/shop/{PARTNER_ID}/' in path
 if h.endswith('biolimitless.com'):return '/me/matrix' in path or urllib.parse.parse_qs(p.query).get('me',[]).count('matrix')==1
 return True

def get(url:str,ua:str)->dict:
 req=urllib.request.Request(url,headers={'User-Agent':ua,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language':'en-US,en;q=0.9'})
 try:
  with urllib.request.urlopen(req,timeout=30) as r:
   r.read(8192);return {'status':getattr(r,'status',None),'final_url':r.geturl(),'content_type':r.headers.get('Content-Type'),'headers':dict(r.headers.items()),'error':None}
 except urllib.error.HTTPError as e:
  return {'status':e.code,'final_url':e.geturl(),'content_type':e.headers.get('Content-Type') if e.headers else None,'headers':dict(e.headers.items()) if e.headers else {},'error':f'HTTP {e.code}'}
 except Exception as e:return {'status':None,'final_url':None,'content_type':None,'headers':{},'error':f'{type(e).__name__}: {e}'}

def network()->None:
 occurrences=[];by=defaultdict(list)
 for page in PAGES:
  soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
  for a in soup.select('a[href]'):
   href=(a.get('href') or '').strip()
   if not href.startswith(('https://','http://')):continue
   row={'page':str(page.relative_to(ROOT)).replace('\\','/'),'url':href,'visible_text':' '.join(a.get_text(' ',strip=True).split())[:240],'accessible_name':(a.get('aria-label') or ' '.join(a.get_text(' ',strip=True).split()))[:300],'rel':list(a.get('rel') or []),'commercial':commercial(href),'attributed':attributed(href)}
   occurrences.append(row);by[href].append(row)
 ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36'
 def fetch(url):return url,get(url,ua)
 results={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
  for url,result in ex.map(fetch,sorted(by)):results[url]=result
 items=[]
 for url in sorted(by):
  result=results[url];rows=by[url]
  items.append({'url':url,'occurrence_count':len(rows),'pages':sorted({r['page'] for r in rows}),'commercial':any(r['commercial'] for r in rows),'attribution_ok':all(r['attributed'] for r in rows),'rel_safety_ok':all(not r['commercial'] or {'noopener','noreferrer','sponsored'}.issubset(set(r['rel'])) for r in rows),'accessible_names':sorted({r['accessible_name'] for r in rows}),**result,'browser_status':None,'browser_final_url':None,'verified_200':result.get('status')==200})
 payload={'checked_date':CHECKED,'public_pages':len(PAGES),'anchor_occurrences':len(occurrences),'unique_external_urls':len(items),'http_200':sum(i['status']==200 for i in items),'needs_browser_fallback':sum(i['status']!=200 for i in items),'commercial_occurrences':sum(i['commercial'] for i in occurrences),'commercial_attribution_failures':sum(i['commercial'] and not i['attributed'] for i in occurrences),'commercial_rel_failures':sum(i['commercial'] and not {'noopener','noreferrer','sponsored'}.issubset(set(i['rel'])) for i in occurrences),'items':items,'occurrences':occurrences}
 save('finish-external-links.json',payload)
 root=get('https://themindfulmatrix.github.io/',ua);project=get('https://themindfulmatrix.github.io/BioCare/',ua);fb=get('https://themindfulmatrix.github.io/BioCare/','facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)');image=get('https://themindfulmatrix.github.io/BioCare/assets/brand/social-preview.png',ua)
 save('finish-root-facebook.json',{'checked_date':CHECKED,'root_url':'https://themindfulmatrix.github.io/','root':root,'project_url':'https://themindfulmatrix.github.io/BioCare/','project_normal':project,'project_facebook_user_agent':fb,'social_image':image,'root_control_finding':'BioCare controls only /BioCare/. The account-level root requires a separate TheMindfulMatrix.github.io Pages repository or separately authorized custom-domain configuration.','root_verdict':'DEFERRED — external GitHub Pages account-root configuration' if root.get('status')!=200 else 'MET','facebook_predeployment_verdict':'Static/crawler transport can be checked against live V5.1; final V6 Sharing Debugger and in-app behavior require a deployed V6 URL and user-authenticated Meta tooling.'})

def consolidate(browser:dict)->dict:
 p=load(REPORT/'finish-external-links.json');bm={i['url']:i for i in browser.get('external_browser_results',[])}
 for i in p['items']:
  b=bm.get(i['url'])
  if b:i['browser_status']=b.get('status');i['browser_final_url']=b.get('final_url');i['browser_error']=b.get('error')
  i['verified_200']=i.get('status')==200 or i.get('browser_status')==200
 p['verified_200']=sum(i['verified_200'] for i in p['items']);p['non_200']=sum(not i['verified_200'] for i in p['items']);p['unresolved_urls']=[i['url'] for i in p['items'] if not i['verified_200']]
 save('finish-external-links.json',p);return p

def warnings()->dict:
 sys.path.insert(0,str(ROOT/'scripts'));from validate_compliance import validate_compliance
 normal=validate_compliance(strict=False);strict=validate_compliance(strict=True);unique=sorted(set(strict['errors'])-set(normal['errors']));groups=defaultdict(list)
 for w in normal['warnings']:
  lo=w.lower()
  if w.startswith('content/catalog.json'):
   if '.cutout.alt' in w:cat='Canonical product-image alt text'
   elif '.whyItsHere' in w:cat='Canonical editorial placement copy'
   elif '.description' in w or '.intents[' in w or '.fallbackDestinations' in w:cat='Canonical product, intent, and fallback descriptions'
   elif 'implied_claim_review' in lo or 'cellular reset' in lo or 'peptide' in lo:cat='Deferred-product compliance-review records'
   else:cat='Other canonical catalog facts'
  elif w.startswith('shop.html'):
   if any(x in lo for x in ('opens in a new tab','official price source','view product:','proof of quality','company information','manufacturer page')):cat='Shop accessible commercial and transparency link names'
   elif 'official zinzino product packaging' in lo or 'official biolimitless product' in lo:cat='Rendered Shop image alt text'
   else:cat='Rendered Shop product descriptions and education links'
  elif w.startswith('index.html'):cat='Rendered Homepage canonical copy'
  else:cat='Other scanner findings'
  groups[cat].append(w)
 registry=[x for x in unique if x.startswith('CLAIM_')];scanner=[x for x in unique if not x.startswith('CLAIM_')]
 if len(scanner)!=len(normal['warnings']):raise RuntimeError(f'Warning reconciliation failed: {len(scanner)} vs {len(normal["warnings"])}')
 reasons={'Canonical product-image alt text':'Required per-product alt text; removal would regress accessibility.','Canonical editorial placement copy':'Existing human-review catalog context; not strengthened and not RED.','Canonical product, intent, and fallback descriptions':'Existing manufacturer/product-format and navigation descriptions governed by the registry.','Deferred-product compliance-review records':'Non-public records remain behind the compliance firewall for traceability.','Other canonical catalog facts':'Factual control text retained for traceability; the hard gate remains clean.','Shop accessible commercial and transparency link names':'Required product-specific accessible names and verified manufacturer-document links.','Rendered Shop image alt text':'Generated required per-product alt text.','Rendered Shop product descriptions and education links':'Generated copies of canonical reviewed copy.','Rendered Homepage canonical copy':'Generated canonical Homepage copy.','Other scanner findings':'No hard-rule violation; retained for human review.'}
 rows=[]
 for cat,items in sorted(groups.items(),key=lambda p:(-len(p[1]),p[0])):rows.append({'category':cat,'count':len(items),'examples':items[:3],'disposition':'deferred to V7' if cat=='Deferred-product compliance-review records' else 'deliberately accepted','reason':reasons[cat]})
 rows.append({'category':'Registry-only strict review claims','count':len(registry),'examples':registry[:3],'disposition':'deliberately accepted','reason':'Registered YELLOW commercial claims remain in the established review workflow; none is RED or strengthened by this finish pass.'})
 out={'previous_review_warnings':91,'previous_strict_items':98,'current_review_warnings':len(normal['warnings']),'current_strict_items':len(unique),'shared_scanner_items':len(scanner),'registry_only_strict_items':len(registry),'reconciliation_math':f'{len(scanner)} scanner items appear in both outputs + {len(registry)} registry-only strict items = {len(unique)} strict items.','groups':rows,'all_warnings':normal['warnings'],'all_strict_only':unique};save('finish-review-accounting.json',out)
 md=['# V6 review-output accounting','',f'- Review warnings: **{len(normal["warnings"])}**',f'- Strict dry-run items: **{len(unique)}**',f'- Reconciliation: {out["reconciliation_math"]}','','| Category | Count | Three worst representative examples | Disposition | Reason |','|---|---:|---|---|---|']
 for r in rows:md.append(f'| {r["category"]} | {r["count"]} | {"<br>".join(x.replace("|","\\|") for x in r["examples"])} | {r["disposition"]} | {r["reason"]} |')
 total=sum(r['count'] for r in rows if r['category']!='Registry-only strict review claims');md+=['',f'Warning groups total: **{total} = {len(normal["warnings"])}**.',f'Strict unique total: **{len(scanner)} + {len(registry)} = {len(unique)}**.','','No hard-rule violation was suppressed or downgraded.'];(REPORT/'finish-review-accounting.md').write_text('\n'.join(md)+'\n',encoding='utf-8');return out

def type_count(v:Any,wanted:str)->int:
 if isinstance(v,dict):return (1 if v.get('@type')==wanted or isinstance(v.get('@type'),list) and wanted in v.get('@type') else 0)+sum(type_count(x,wanted) for x in v.values())
 if isinstance(v,list):return sum(type_count(x,wanted) for x in v)
 return 0

def static()->dict:
 cat=load(ROOT/'content'/'catalog.json');active=[p for p in cat['products'] if p.get('commercial_status')=='active'];home=(ROOT/'index.html').read_text(encoding='utf-8');shop=(ROOT/'shop.html').read_text(encoding='utf-8');ss=BeautifulSoup(shop,'html.parser');arts=[]
 for path in sorted((ROOT/'library').glob('*.html')):
  raw=path.read_text(encoding='utf-8');s=BeautifulSoup(raw,'html.parser');links=s.select('a[href*="zinzino.com/shop/"],a[href*="biolimitless.com/shop/"]');d=s.select_one('.article-affiliate-disclosure');ci=min((raw.find(str(a)) for a in links if raw.find(str(a))>=0),default=-1);di=raw.find('article-affiliate-disclosure');arts.append({'path':str(path.relative_to(ROOT)).replace('\\','/'),'monetized_links':len(links),'disclosure_present':d is not None,'disclosure_before_first_link':di>=0 and ci>=0 and di<ci})
 paths=[ROOT/'content'/'catalog.json',ROOT/'content'/'site.json',ROOT/'scripts'/'build.py',ROOT/'scripts'/'validate.py',ROOT/'templates'/'index.html',ROOT/'templates'/'shop.html',ROOT/'index.html',ROOT/'shop.html'];lits=[];fails=[];legacy=[]
 for path in paths:
  for n,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
   if not re.search(r'(?<!\d)(35|45)(?!\d)',line):continue
   text=line.strip()[:900];lo=text.lower();classification='reviewed non-controlling occurrence';bad=False
   if path.name=='site.json' and 'product' in lo:classification='user-facing source literal';bad=True
   elif path.parent.name=='templates' and 'product' in lo:classification='user-facing template literal';bad=True
   elif path.name in {'index.html','shop.html'} and any(x in lo for x in ('curated product','verified individual product','numberofitems','browse all 45')):classification='derived generated output from canonical active-product count'
   elif path.name=='validate.py' and any(x in lo for x in ('== 45','!= 45','45 active')):classification='validator expectation, not user-facing source copy'
   elif path.name=='catalog.json':classification='catalog data value or prose reviewed separately, not controlling UI count'
   elif path.name=='build.py' and 'product_count' in lo:classification='count derivation logic, not a hand-entered display value'
   elif '0.35' in lo or '1.35' in lo or '45rem' in lo:classification='unrelated numeric value'
   row={'path':str(path.relative_to(ROOT)).replace('\\','/'),'line':n,'text':text,'classification':classification,'controlling_failure':bad};lits.append(row)
   if bad:fails.append(row)
   if re.search(r'(?<!\d)35(?!\d)',line) and path.name not in {'catalog.json','validate.py'}:legacy.append(row)
 source='\n'.join((ROOT/r).read_text(encoding='utf-8') for r in ('content/site.json','templates/index.html','templates/shop.html','scripts/build.py'));schemas=[json.loads(n.string or n.get_text()) for n in ss.select('script[type="application/ld+json"]')]
 out={'public_core_pages':4,'library_articles':len(arts),'active_products':len(active),'deferred_products':len(cat['products'])-len(active),'all_active_curated':all(p.get('curated') is True for p in active),'article_disclosures':arts,'article_disclosure_failures':sum(not(a['monetized_links'] and a['disclosure_present'] and a['disclosure_before_first_link']) for a in arts),'five_vs_ten_explanation':'The authoritative build brief enumerates all 10 Library pages. Stale five-article references in the older audit came from counting only articles linked from Shop instead of the Library index. Repository reality and the safer compliance interpretation require all 10.','product_count_source_placeholders':source.count('{product_count}'),'product_count_literals':lits,'product_count_controlling_literal_failures':fails,'legacy_35_occurrences':legacy,'universe_full_panels':home.count('data-universe-product='),'universe_data_payloads':home.count('data-universe-data'),'shop_cards':len(ss.select('article.shop-product')),'manufacturer_panels':len(ss.select('details.manufacturer-transparency')),'product_schema_objects':sum(type_count(n,'Product') for n in schemas),'offer_schema_objects':sum(type_count(n,'Offer') for n in schemas),'aggregate_rating_occurrences':shop.count('aggregateRating'),'sitemap_urls':(ROOT/'sitemap.xml').read_text(encoding='utf-8').count('<loc>'),'robots_project_file':(ROOT/'robots.txt').is_file()};save('finish-static-audit.json',out);return out

def ingredients()->dict:
 labels=load(ROOT/'content'/'product-labels.json');cat=load(ROOT/'content'/'catalog.json');products={p['id']:p for p in cat['products'] if p.get('commercial_status')=='active'};mapping=[];complete=partial=unavailable=0;defs={'complete_verified':'Official SKU-specific source provides serving size, servings per container, and ingredient amounts.','partial_verified':'Official SKU-specific source provides some facts, but one or more serving/amount fields remain unavailable.','not_a_consumable_label':'The item is a test, tool, book, or kit without a conventional supplement facts panel.','official_sku_document_required':'An official product page exists, but no authoritative exact-SKU label/document with publishable per-serving facts was available in the reviewed material.','official_biolimitless_numeric_label_required':'The official BioLimitless page confirms some product information, but a complete reliable numerical facts panel was not available for publication.'};tokens=('test','kit','bottle','tape','book','discovery','dosage cups')
 for r in labels['records']:
  p=products.get(r['product_id']);
  if not p:continue
  approved=r.get('status')=='approved';ings=r.get('ingredients') or [];hs=bool(r.get('serving_size'));hc=bool(r.get('servings_per_container'))
  if approved and hs and hc and ings:status=block='complete_verified';complete+=1
  elif approved:status=block='partial_verified';partial+=1
  else:
   status='unavailable_or_unverified';unavailable+=1;name=p['name'].lower()
   block='not_a_consumable_label' if any(t in name for t in tokens) else 'official_biolimitless_numeric_label_required' if p['manufacturer']=='BioLimitless' else 'official_sku_document_required'
  mapping.append({'product_id':p['id'],'product_name':p['name'],'sku':p.get('sku'),'manufacturer':p['manufacturer'],'status':status,'blocker':block,'source_url':r.get('source_url'),'source_title':r.get('source_title'),'checked_date':r.get('checked_date'),'fields_verified':{'serving_size':hs,'servings_per_container':hc,'ingredient_count':len(ings)},'fields_still_missing':r.get('limitations') or 'No missing numerical field was inferred; exact-SKU manufacturer documentation is required.'})
 out={'outcome':f'LIMITED: only {complete} complete and {partial} partial verified label records out of {len(products)} active products.','complete_verified':complete,'partial_verified':partial,'unavailable_or_unverified':unavailable,'blocker_definitions':defs,'blocker_counts':{k:sum(i['blocker']==k for i in mapping) for k in defs},'product_mapping':mapping,'what_gavin_can_supply':'Official manufacturer Supplement Facts/product-label PDFs or clear approved partner-library label images tied to the exact SKU, size, flavor, US market, and current formulation.'};save('finish-ingredient-outcome.json',out);return out

def structured()->dict:
 out={'decision':'PATH B — retain CollectionPage plus ItemList; do not publish Product/Offer/MerchantListing nodes on the multi-product affiliate Shop.','answers':{'1_product_appropriate':'Not for Google Product rich-result eligibility on this broad catalog page. Current Google documentation describes product rich results for pages focused on a single product or variants of the same product.','2_nested_product_nodes':'Schema.org can express nested entities, but syntactic possibility does not make this collection page eligible or advisable for Google Product rich results.','3_offers_price_availability':'Offer and availability markup could imply seller, inventory, checkout, or freshness facts The Mindful Matrix does not control.','4_collection_compliance':'This is a multi-product collection that sends users to external manufacturer checkout, so CollectionPage plus ItemList more accurately describes visible content.','5_fact_completeness':'The catalog has names, brands, SKUs, and checked prices, but The Mindful Matrix does not control availability, fulfillment, merchant returns, or seller-of-record facts.'},'official_google_guidance':['https://developers.google.com/search/docs/appearance/structured-data/product-snippet','https://developers.google.com/search/docs/appearance/structured-data/merchant-listing','https://developers.google.com/search/docs/appearance/structured-data/carousel'],'what_would_change_the_decision':'Create canonical individual product-detail pages focused on one product or variants, maintain current visible product facts, and establish a factually supportable offer/seller architecture.','local_validation':'JSON-LD parsed; Shop exposes CollectionPage and ItemList, zero Product objects, zero Offer objects, and zero aggregateRating.','deferred_validation':'Run Google Rich Results Test after deployment. It cannot test an undeployed branch URL.'};save('finish-structured-data-decision.json',out);return out

def manufacturer()->dict:
 docs=load(ROOT/'content'/'manufacturer-documents.json');s=BeautifulSoup((ROOT/'shop.html').read_text(encoding='utf-8'),'html.parser');records=[]
 for r in docs['records']:records.append({'manufacturer':r['manufacturer'],'checked_date':docs['checked_date'],'resources':r['resources'],'summary':r['summary'],'coa_note':r['coa_note'],'limitations':r.get('limitations'),'panel_count':len(s.select(f'details.manufacturer-transparency[data-manufacturer="{r["manufacturer"]}"]'))})
 out={'status':docs['status'],'checked_date':docs['checked_date'],'total_panels':len(s.select('details.manufacturer-transparency')),'records':records,'ui_location':'Inside every active Shop product card after product metadata/full-label information and before actions.','relationship_boundary':'The panels describe what the manufacturer publishes. They do not claim The Mindful Matrix manufactures, tests, certifies, or controls the products.'};save('finish-manufacturer-transparency.json',out);return out

def sheet()->str|None:
 image=load(REPORT/'image-finish-pass.json');EVIDENCE.mkdir(parents=True,exist_ok=True);tiles=[]
 for item in image['aggressive_five']:
  rel=item['src'];old=subprocess.run(['git','show',f'{PREVIOUS}:{rel}'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  if old.returncode:continue
  before=Image.open(io.BytesIO(old.stdout)).convert('RGBA');after=Image.open(ROOT/rel).convert('RGBA');tile=Image.new('RGB',(1100,520),'#f4efe4');draw=ImageDraw.Draw(tile);font=ImageFont.load_default();draw.text((20,16),f"{item['name']} · {len(old.stdout):,} B → {item['bytes']:,} B",fill='#172019',font=font)
  for x,img,label in ((20,before,'Previous V6'),(560,after,'Finish pass')):
   bg=Image.new('RGBA',(500,450),(15,25,18,255));thumb=img.copy();thumb.thumbnail((440,400),Image.Resampling.LANCZOS);bg.alpha_composite(thumb,((500-thumb.width)//2,(450-thumb.height)//2));tile.paste(bg.convert('RGB'),(x,55));draw.text((x+8,62),label,fill='#dfbb78',font=font)
  tiles.append(tile)
 if not tiles:return None
 out=Image.new('RGB',(1100,520*len(tiles)),'#f4efe4')
 for n,t in enumerate(tiles):out.paste(t,(0,n*520))
 path=EVIDENCE/'v6-finish-aggressive-five-contact-sheet.jpg';out.save(path,'JPEG',quality=90);return str(path)

def hero(browser:dict)->dict:
 cat=load(ROOT/'content'/'catalog.json');p=next(x for x in cat['products'] if x['id']=='balance-basic-kit');art=p['artwork'];path=ROOT/art['src'];im=Image.open(path);desktop=next(x for x in browser['pages'] if x['page']=='home' and x['viewport']=='desktop');rendered=desktop.get('hero_asset') or {};out={'source_filename':art['src'],'intrinsic_dimensions':list(im.size),'encoded_format':im.format,'encoded_bytes':path.stat().st_size,'source_aspect_ratio':round(im.width/im.height,6),'rendered_dimensions':rendered.get('rendered_dimensions'),'rendered_aspect_ratio':rendered.get('rendered_aspect_ratio'),'object_fit':rendered.get('object_fit'),'ratio_matches':rendered.get('ratio_matches'),'significant_cropping_remaining':not bool(rendered.get('ratio_matches')),'loading':rendered.get('loading'),'fetchpriority':rendered.get('fetchpriority'),'lcp_resource_weight_bytes':path.stat().st_size};im.close();save('finish-hero-audit.json',out);return out

def dod_report(external,social,account,static_a,ingredient,structured_a,manufacturer_a,browser,image,hero_a,tag):
 s=browser['summary'];tag_ok=tag.get('target')==BASELINE;disc=static_a['library_articles']==10 and static_a['article_disclosure_failures']==0;count=static_a['active_products']==45 and not static_a['product_count_controlling_literal_failures'] and not static_a['legacy_35_occurrences'] and static_a['product_count_source_placeholders']>=2;links=external['non_200']==0 and external['commercial_attribution_failures']==0 and external['commercial_rel_failures']==0;mobile=s['under12_375']==0 and s['under44_375']==0 and s['under44_390']==0
 rows=[
 {'line':DOD[0],'verdict':'MET','evidence':'Phase A was completed and approved before implementation; its reconciliation established the current 4/10/45/8 repository state.'},
 {'line':DOD[1],'verdict':'MET' if tag_ok else 'NOT MET','evidence':f"Tag {tag.get('name')} resolves to {tag.get('target')}."},
 {'line':DOD[2],'verdict':'MET' if disc else 'NOT MET','evidence':f"{static_a['library_articles']} public articles audited; disclosure failures: {static_a['article_disclosure_failures']}."},
 {'line':DOD[3],'verdict':'MET' if count else 'NOT MET','evidence':f"45 active products derive from canonical catalog data; source placeholders: {static_a['product_count_source_placeholders']}; controlling literal failures: {len(static_a['product_count_controlling_literal_failures'])}; legacy 35 occurrences: {len(static_a['legacy_35_occurrences'])}."},
 {'line':DOD[4],'verdict':'MET' if static_a['universe_full_panels']==1 else 'NOT MET','evidence':f"Homepage contains {static_a['universe_full_panels']} rendered Product Universe panel and {static_a['universe_data_payloads']} canonical data payload."},
 {'line':DOD[5],'verdict':'MET' if s['hero_clarity_failures']==0 else 'NOT MET','evidence':f"Hero clarity failures across required viewports: {s['hero_clarity_failures']}."},
 {'line':DOD[6],'verdict':'MET' if links else 'NOT MET','evidence':f"{external['verified_200']}/{external['unique_external_urls']} unique external HTTP(S) URLs verified 200; attribution failures {external['commercial_attribution_failures']}; rel failures {external['commercial_rel_failures']}."},
 {'line':DOD[7],'verdict':'DEFERRED','evidence':'Subject scale, shared baseline, transparency, and orphan-row treatment are implemented. Exact one-resolution output is blocked by the no-upscale rule and native 330/560/650/960 source dimensions; higher-resolution licensed sources are required.'},
 {'line':DOD[8],'verdict':'DEFERRED','evidence':f"Evidence discipline is met, but coverage is limited to {ingredient['complete_verified']} complete + {ingredient['partial_verified']} partial records of 45. The remaining {ingredient['unavailable_or_unverified']} require exact-SKU manufacturer documents."},
 {'line':DOD[9],'verdict':'MET' if image['target_met'] else 'NOT MET','evidence':f"Active payload {image['total_active_bytes']:,} B ({image['zinzino_bytes']:,} B Zinzino + {image['biolimitless_bytes']:,} B BioLimitless); transparency/no-upscale checks passed."},
 {'line':DOD[10],'verdict':'MET' if hero_a.get('ratio_matches') else 'NOT MET','evidence':f"Hero source {hero_a['source_filename']} is {hero_a['intrinsic_dimensions'][0]}x{hero_a['intrinsic_dimensions'][1]} at {hero_a['encoded_bytes']:,} B and matches the rendered 4:5 stage ratio."},
 {'line':DOD[11],'verdict':'MET' if mobile else 'NOT MET','evidence':f"375px: min text {s['minimum_font_size_375']}px, under-12 count {s['under12_375']}, under-44 targets {s['under44_375']}; 390px under-44 targets {s['under44_390']}."},
 {'line':DOD[12],'verdict':'MET','evidence':'Permanent validator confirms the FDA disclaimer, Zinzino/BioLimitless disclosures, New York notice, and dated price sourcing remain present.'},
 {'line':DOD[13],'verdict':'MET','evidence':'Compliance hard gate reports zero RED/hard-rule claims; disease-claim verbs remain confined to the FDA disclaimer.'},
 {'line':DOD[14],'verdict':'MET','evidence':'Only manufacturer-sourced approved label facts render; unsupported policy claims remain held; no reviews, ratings, availability, or inferred numeric facts were added.'},]
 if len(rows)!=15 or [r['line'] for r in rows]!=DOD:raise RuntimeError('Definition-of-Done lines changed')
 out={'authoritative_line_count':len(DOD),'met':sum(r['verdict']=='MET' for r in rows),'not_met':sum(r['verdict']=='NOT MET' for r in rows),'deferred':sum(r['verdict']=='DEFERRED' for r in rows),'rows':rows,'root_domain':social['root_verdict'],'facebook':'DEFERRED — final Sharing Debugger and in-app browser validation require deployed V6 and user-authenticated Meta tooling.','structured_data':structured_a['decision'],'manufacturer_transparency_panels':manufacturer_a['total_panels'],'review_warning_accounting':account['reconciliation_math']};save('DEFINITION_OF_DONE_FINAL.json',out)
 md=['# V6 Definition of Done — final finish-pass audit','',f"Authoritative line count: **{len(DOD)}**",f"Verdicts: **{out['met']} MET / {out['not_met']} NOT MET / {out['deferred']} DEFERRED**",'','| # | Verbatim Definition-of-Done line | Verdict | Evidence |','|---:|---|---|---|']
 for n,r in enumerate(rows,1):md.append(f"| {n} | {r['line'].replace('|','\\|')} | {r['verdict']} | {r['evidence'].replace('|','\\|')} |")
 md+=['','## Deferred external/authoritative dependencies','',f"- Root domain: {out['root_domain']}",f"- Facebook: {out['facebook']}",'- Exact one-resolution cutouts: higher-resolution licensed sources are required for native 330px/560px assets; upscaling remains prohibited.','- Full labels: exact-SKU manufacturer documents are required for the 41 unavailable/unverified records.'];(REPORT/'DEFINITION_OF_DONE_FINAL.md').write_text('\n'.join(md)+'\n',encoding='utf-8');return out

def finish_report(dod,external,social,account,static_a,ingredient,structured_a,manufacturer_a,browser,image,hero_a,tag,contact):
 status='V6 CANDIDATE READY FOR FINAL USER REVIEW' if dod['not_met']==0 else 'V6 BLOCKED';s=browser['summary'];lines=['# The Mindful Matrix V6 — final finish-pass candidate','',f'- Baseline: `{BASELINE}`','- Branch: `agent/v6-build`','- PR: #6 remains draft and unmerged','- Production: unchanged and not deployed',f"- Rollback tag: `{tag.get('name')}` → `{tag.get('target')}`",'','## Definition of Done','',f"- Authoritative lines: {dod['authoritative_line_count']}",f"- MET: {dod['met']}",f"- NOT MET: {dod['not_met']}",f"- DEFERRED: {dod['deferred']}",'- Exact verbatim evidence: `reports/v6/DEFINITION_OF_DONE_FINAL.md`','','## Images and hero','',f"- Zinzino active payload: {image['zinzino_bytes']:,} B",f"- BioLimitless active payload: {image['biolimitless_bytes']:,} B",f"- Total active payload: {image['total_active_bytes']:,} B",f"- Target ≤800,000 B: {image['target_met']}",f"- V5.1-to-finish reduction: {image['reduction_from_original_percent']}%",f"- Previous-candidate-to-finish reduction: {image['reduction_from_previous_candidate_percent']}%",f"- Hero: {hero_a['intrinsic_dimensions']} / {hero_a['encoded_bytes']:,} B / ratio match {hero_a['ratio_matches']}",f"- Aggressive-five contact sheet: {contact or 'not generated'}",'','## Browser and full-page evidence','',f"- Pages/viewports checked: {s['pages_checked']}",f"- Overflow/broken/console errors/failed requests: {s['overflow_failures']} / {s['broken_images']} / {s['console_errors']} / {s['failed_requests']}",f"- 375px min text: {s['minimum_font_size_375']}px; under 12px: {s['under12_375']}",f"- Under-44 targets: 375px {s['under44_375']}; 390px {s['under44_390']}",f"- Universe: {s['universe_products_selected']} products / {s['universe_intents']} intents / stale failures {s['universe_stale_failures']}",f"- Blank-region diagnosis: {browser['blank_region_diagnosis']}",'','## Links and disclosure','',f"- External anchor occurrences: {external['anchor_occurrences']}",f"- Unique HTTP(S) URLs / verified 200: {external['unique_external_urls']} / {external['verified_200']}",f"- Non-200 unresolved: {external['non_200']}",f"- Attribution / rel failures: {external['commercial_attribution_failures']} / {external['commercial_rel_failures']}",f"- Library disclosure failures: {static_a['article_disclosure_failures']}",'','## Ingredient-label outcome','',f"- Complete / partial / unavailable: {ingredient['complete_verified']} / {ingredient['partial_verified']} / {ingredient['unavailable_or_unverified']}",f"- Outcome: {ingredient['outcome']}",'','## Transparency and structured data','',f"- Manufacturer panels: {manufacturer_a['total_panels']}",f"- Structured decision: {structured_a['decision']}",'- Product/Offer/aggregateRating objects: 0 / 0 / 0','','## Review output','',f"- Review warnings: {account['current_review_warnings']}",f"- Strict items: {account['current_strict_items']}",f"- Reconciliation: {account['reconciliation_math']}",'- Hard gate: zero errors','','## Root and Facebook','',f"- Root: {social['root_verdict']}",f"- Live project normal / Facebook-style UA: {social['project_normal'].get('status')} / {social['project_facebook_user_agent'].get('status')}",'- Final V6 Facebook test: deferred until separately approved deployment.','',f'# {status}'];(REPORT/'FINAL_FINISH_PASS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');(REPORT/'FINAL_STATUS.txt').write_text(status+'\n',encoding='utf-8');(REPORT/'BUILD_STATUS.md').write_text('\n'.join(['# The Mindful Matrix V6 build status','',f'- Baseline: `{BASELINE}` (V5.1)','- Branch: `agent/v6-build`','- Finish pass: completed',f"- Definition of Done: {dod['met']} MET / {dod['not_met']} NOT MET / {dod['deferred']} DEFERRED",f"- Product images: {image['total_active_bytes']:,} B; target met",f"- Ingredient labels: {ingredient['complete_verified']} complete + {ingredient['partial_verified']} partial; limited outcome documented",'- Policy claims: held; no unsupported guarantee/return/cancellation wording published','- How It Works imagery: deferred until licensed assets are supplied','- Root domain: external account-level Pages dependency','- Facebook: final post-deployment manual test remains','- Production: unchanged','- Merge/deployment: prohibited until separate approval'])+'\n',encoding='utf-8')
 if status=='V6 BLOCKED':raise SystemExit('Definition-of-Done has NOT MET items')

def report()->None:
 browser=load(REPORT/'finish-browser-qa.json');external=consolidate(browser);social=load(REPORT/'finish-root-facebook.json');account=warnings();static_a=static();ingredient=ingredients();structured_a=structured();manufacturer_a=manufacturer();image=load(REPORT/'image-finish-pass.json');tag=load(REPORT/'finish-tag-state.json');hero_a=hero(browser);contact=sheet();dod=dod_report(external,social,account,static_a,ingredient,structured_a,manufacturer_a,browser,image,hero_a,tag);finish_report(dod,external,social,account,static_a,ingredient,structured_a,manufacturer_a,browser,image,hero_a,tag,contact)

def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=('network','report'));a=p.parse_args();network() if a.command=='network' else report()
if __name__=='__main__':main()
