"""Bounded read-only benchmark collection. No accounts, bypasses, or traffic estimates."""
import argparse, concurrent.futures, datetime, json, re, time, urllib.request, urllib.error
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

BASE = Path(__file__).resolve().parent
class Surface(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip=0; self.title=False; self.heading=None; self.anchor=None
        self.text=[]; self.titles=[]; self.headings=[]; self.links=[]; self.images=0
        self.image_alt_missing=0; self.descriptions=[]; self.forms=0; self.scripts=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in ("script","style","noscript"): self.skip+=1
        if tag=="script": self.scripts+=1
        if tag=="form": self.forms+=1
        if tag=="title": self.title=True
        if re.fullmatch("h[1-3]",tag): self.heading=[tag,[]]
        if tag=="a": self.anchor=[a.get("href",""),[]]
        if tag=="img":
            self.images+=1
            if "alt" not in a: self.image_alt_missing+=1
        if tag=="meta" and a.get("name","").lower()=="description": self.descriptions.append(a.get("content",""))
    def handle_endtag(self,tag):
        if tag in ("script","style","noscript"): self.skip=max(0,self.skip-1)
        if tag=="title": self.title=False
        if self.heading and tag==self.heading[0]:
            self.headings.append({"level":tag,"text":" ".join(self.heading[1])[:160]});self.heading=None
        if tag=="a" and self.anchor:
            self.links.append({"href":self.anchor[0],"label":" ".join(self.anchor[1])[:100]});self.anchor=None
    def handle_data(self,data):
        if self.skip:return
        data=re.sub(r"\s+"," ",data).strip()
        if not data:return
        self.text.append(data)
        if self.title:self.titles.append(data)
        if self.heading:self.heading[1].append(data)
        if self.anchor:self.anchor[1].append(data)
def fetch(url):
    request=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; MindfulMatrixDesignReview/1.0; public-page research)"})
    with urllib.request.urlopen(request,timeout=22) as response:
        content=response.read(3_000_000); return response.status,response.url,content
def inspect(row):
    result={**row,"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"business_performance":"Not verified; no revenue/conversion inference"}
    try:
        start=time.monotonic();status,url,raw=fetch(row["url"]);p=Surface();p.feed(raw.decode("utf-8",errors="replace"))
        text=" ".join(p.text); links=[]
        for link in p.links:
            href=urljoin(url,link["href"])
            if href.startswith("https://") and link["label"] and (href,link["label"]) not in [(x["href"],x["label"]) for x in links]: links.append({**link,"href":href})
        result.update(status=status,final_url=url,fetch_seconds=round(time.monotonic()-start,2),html_bytes=len(raw),title=" ".join(p.titles),description=p.descriptions[:1],headings=p.headings[:20],images_in_initial_html=p.images,images_missing_alt_attribute=p.image_alt_missing,scripts_in_initial_html=p.scripts,forms_in_initial_html=p.forms,word_count=len(text.split()))
        categories={"education":r"learn|science|research|education|article|blog|journal|guide|evidence|knowledge",
                    "commerce":r"shop|product|buy|subscribe|membership|join|test|supplement|compare|pricing",
                    "trust":r"about|editorial|review|quality|transparen|disclos|certif|medical|expert|mission",
                    "acquisition":r"quiz|newsletter|email|sign.up|subscribe|podcast|instagram|tiktok|youtube|refer|reward"}
        for category,pattern in categories.items():result[category+"_routes"]=[x for x in links if re.search(pattern,x["label"],re.I)][:8]
        # Internal inspection only. Raw excerpts must not enter the review report.
        result["sample_text"]=text[:3500]
        result["scope"]="Initial public HTML only; no rendered/mobile or commercial-success conclusion"
        result["status_note"]="Accessible" if len(text.split())>100 else "Thin/JS-dependent response; insufficient evidence"
        if re.search(r"verify you are human|just a moment|access denied|captcha",text[:500],re.I): result["status_note"]="Access challenge; not bypassed"
    except Exception as e:result.update(status_note="Unavailable to this research fetch; not evidence of business failure",error=str(e)[:240])
    return result
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--ids',help='Comma-separated IDs for a bounded refresh')
    parser.add_argument('--seed',type=Path,help='Earlier local raw observations to preserve')
    args=parser.parse_args()
    roster=json.loads((BASE/"benchmark-roster.json").read_text(encoding="utf-8"))
    results=json.loads(args.seed.read_text(encoding='utf-8')) if args.seed else []
    selected={int(i) for i in args.ids.split(',')} if args.ids else {r['id'] for r in roster}
    results=[r for r in results if r['id'] not in selected]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for result in pool.map(inspect,[r for r in roster if r['id'] in selected]):
            results.append(result);print(f'{result["id"]:03} {result["name"]}: {result["status_note"]}',flush=True)
    output = BASE.parents[1] / '_preview/research-led-experience/research-raw'
    output.mkdir(parents=True, exist_ok=True)
    (output/"benchmark-observations.json").write_text(json.dumps(sorted(results,key=lambda r:r['id']),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Completed",len(results),"distinct website attempts")
