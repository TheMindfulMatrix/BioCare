"""Create original research deliverables; never publish third-party page extracts.

Raw transient observations remain in ignored _preview. The committed output has
our analysis, source URLs and bounded transport observations, not copied articles.
"""
from pathlib import Path
from collections import Counter
import json

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
RAW=ROOT/'_preview/research-led-experience/research-raw/benchmark-observations.json'
VISUAL={1,2,23,22,31,33,34,43,44,45,47,92}
FALLBACK={
1:'https://examine.com/',21:'https://www.mayoclinic.org/',
42:'https://omegaquant.com/',46:'https://drinkag1.com/en-uk',
55:'https://www.pureencapsulationspro.com/',57:'https://www.nowfoods.com/',
58:'https://www.nordic.com/',61:'https://www.gardenoflife.com/',
65:'https://www.solgar.com/',66:'https://viridian-nutrition.com/',
78:'https://www.kleanathlete.com/',85:'https://www.metagenics.co.uk/',
89:'https://jshealthvitamins.com/',90:'https://bioptimizers.com/',100:'https://nl.iherb.com/'}

INTRO="""# The Mindful Matrix — 100-site research and experience direction

Prepared September 6, 2026. Review candidate only; production is unchanged.

## The decision

Build an **editorial research desk with a product-discovery layer**: calm mineral green, cream surfaces, spacious official product images, readable typography, and a useful Learn / Measure / Explore navigator. The business remains education first, with clearly disclosed optional manufacturer links—not a medical provider or a marketplace checkout.

The strongest transferable pattern is **question → useful explanation → inspectable evidence → optional product record → disclosed external destination**. This is a design and information-architecture recommendation, not a demonstrated conversion lift.

## What was actually examined

- **100 website entries:** 30 education/publishing references, 12 testing or measurement businesses, and 58 product/commerce references.
- **85 direct public HTML observations**, plus primary-page browser/web review for the **15 sites the bounded fetch could not access**. A 403/429/TLS error is a research-access limitation, not a failed website or business.
- **12 desktop visual deep dives:** Examine, Healthline, ConsumerLab, Labdoor, Levels, Function Health, Superpower, Thorne, Ritual, Seed, Momentous, Timeline. The other entries are structured public-content reviews, not full visual, mobile, usability, or checkout audits.
- The HTML collection was capped at 3,000,000 bytes per response. It captures navigation, education/trust/commerce routes and initial HTML—not total page weight, Core Web Vitals, traffic, or conversion.
- This is a deliberately mixed reference set, not 100 identical competitors. Clinical institutions are adjacent education/trust references. Nutri Advanced now resolves into Metagenics UK; Metagenics US and UK are regional websites of the same organization.
- Well+Good and Livestrong were replaced with Wellness Mama and Clean Eating Kitchen after their observed destination/content no longer matched the intended reference set.
- This is an observational sample, not a statistically representative market study. No paid accounts, private analytics, customer data, purchases, or lead forms were used.

The machine-readable record is [benchmark-observations-summary.json](benchmark-observations-summary.json); the original per-site judgments are [benchmark-assessments.json](benchmark-assessments.json). Source links accompany every entry below. Long third-party excerpts and raw page captures are deliberately not committed.

## Which references are strongest—and what “successful” means here

**Commercial winners and failures cannot be ranked responsibly from these observations.** We did not obtain audited revenue, traffic histories, customer acquisition costs, profit, or conversion rates. A polished home page is not proof of a profitable business. A blocked research fetch is not evidence of failure.

Some sites publish their own scale signals. During the desktop review, [Healthline](https://www.healthline.com/) displayed 50 million monthly readers and 130 medical reviewers; [ConsumerLab](https://www.consumerlab.com/) displayed more than 100,000 members and 1,400 product reviews. Those are the sites' own statements, not independently verified measurements and not a like-for-like performance ranking. Their editorial or testing credentials do not transfer to The Mindful Matrix.

### Strongest visual references, judged qualitatively

| Reference | Observed presentation strength | Appropriate adaptation | Boundary |
|---|---|---|---|
| [Seed](https://seed.com/) | Confident green product scene and distinct Shop / Science / Learn routes | Original mineral-green palette; make the product a clear object | Do not copy branding, microbiome claims, or the cookie overlay |
| [Ritual](https://ritual.com/) | Restrained color system and visible standards narrative | Fewer competing accents; readable standards and sourcing links | No borrowed clinical authority or testing badges |
| [Timeline](https://www.timeline.com/) | A memorable product macro inside a quiet editorial frame | Enlarge official product artwork and give it breathing room | Comparative efficacy claims are not transferable |
| [Function Health](https://www.functionhealth.com/) | Warm, consistent art direction with legible membership scope | Explain what an action leads to; maintain clear hierarchy | The Matrix does not provide the same clinical service |
| [Levels](https://www.levels.com/) | One strong entry task and deliberate typography | Focus the opening on a clear next step | Avoid the bandwidth and distraction of a large hero video |
| [Momentous](https://www.livemomentous.com/) | Large product-led imagery and clear goal / shop / learn navigation | Combine product clarity with a useful education route | Do not borrow athlete endorsements or performance promises |

### Strongest education-to-decision structures

| Reference | Useful pattern | Matrix implementation |
|---|---|---|
| [Examine](https://examine.com/) | Search-first research discovery | Preserve unified local search; make Library filters prominent |
| [Labdoor](https://labdoor.com/) | A clear purpose and direct route into organized comparisons | Make product records and documentation easy to inspect, without inventing rankings or laboratory testing |
| [ConsumerLab](https://www.consumerlab.com/) | An explicit testing-information service and membership boundary | Clearly distinguish public source context from product-specific substantiation |
| [Healthline](https://www.healthline.com/) | Topic-based content entry and editorial identity | Short guide preview, visible source routes and an inspectable About page |
| [OmegaQuant](https://omegaquant.com/) | Educational explanation connected to test selection | Retain the existing Know Your Number journey, its limits and optional products |

These are **reference picks for specific design jobs**, not a claim that they are the most profitable companies or that the remaining sites are unsuccessful.

## Marketing mechanisms worth learning from

1. **Answer the visitor's question before asking for a purchase.** Publishers attract topic interest; testing and product brands connect a useful explanation to a next step. The Matrix now offers Learn, Measure and Explore as separate choices, with no health assessment or stored answers.
2. **Show the evidence route near the decision.** Standards, sourcing, documentation and realistic limitations support informed decisions. We kept the source index, product documentation and manufacturer boundaries intact.
3. **Make the handoff explicit.** Some references sell directly; others refer users elsewhere. The Matrix must disclose when a manufacturer link may earn commission and that checkout happens elsewhere. Those disclosures remain visible, not hidden in the new pricing accordion.
4. **Use product imagery as information.** Official packaging is larger and easier to inspect. No generated packaging, copied competitor imagery, invented certifications or medical symbols were added.
5. **Design for discovery, not just a hero screenshot.** The visual system continues into products, Library, Evidence, guides, the testing journey and product records. Existing search, sorting, filters and dialogs remain.
6. **Keep repeat visits useful.** The current guides and source library provide real value. The unpublished K2, zinc/copper and magnesium backlog is not filled with unsourced material to make the site look larger.

These mechanisms are inferred from visible site structures. They are hypotheses to test for The Mindful Matrix, not proof that a particular layout causes sales.

## Observed friction—not “failed businesses”

- In the desktop samples, cookie overlays obscured substantial parts of the [Seed](https://seed.com/) and [Ritual](https://ritual.com/) openings. The candidate adds no tracking or consent overlay because it adds no tracking; that is not advice to hide necessary consent.
- Promotion-heavy surfaces such as [Perelel](https://perelelhealth.com/) and [Life Extension](https://www.lifeextension.com/) create competing messages. The candidate separates the primary learning action from optional kit purchase details.
- The initial HTML responses for [BulkSupplements](https://www.bulksupplements.com/) (reached the 3 MB collection cap), [Wild Nutrition](https://www.wildnutrition.com/) (2.62 MB), [Seeking Health](https://www.seekinghealth.com/) (1.88 MB) and [Naked Nutrition](https://nakednutrition.com/) (1.86 MB) illustrate complex page payloads. These are **HTML-response observations**, not full asset measurements or proven poor real-user performance. The Matrix keeps its static build and adds no framework, video, third-party font or analytics dependency.
- Large publishers and clinical sites offer far broader navigation than this small education business needs. We keep the Matrix's routes narrow instead of imitating their scale.
- Science language, testimonials, badges and celebrity imagery can look authoritative without establishing product-specific evidence. None were borrowed.

## What has been implemented in this candidate

| Research finding | Shipped review change | Preserved safeguard |
|---|---|---|
| One clear opening task | “Less noise. More clarity.” with Find your path / Library actions | No efficacy or clinical promise |
| Product imagery needs hierarchy | Larger existing official Balance kit, quiet visual frame, responsive composition | Same manufacturer destination and visible affiliate disclosure |
| Different visitors need different entries | Learn / Measure / Explore navigator with keyboard-operable buttons | All three paths remain visible without JavaScript; no health profiling or answer storage |
| Search is a first-class task | Unified search and direct Library filters | Existing relevance engine and query behavior |
| Shorter initial choice set | Three-guide home preview; all ten on the Library page | No guide removed or silently unpublished |
| Consistent secondary pages | Shared typography, cards, spacing, controls, contrast | 71 canonical public pages and current metadata |
| Prevent distracting jumps | Catalog intent rail scrolls horizontally without jumping the document | Skip link is first again; keyboard and dialog behavior checked |
| Trust must stay visible | Complete standards, manufacturer boundaries, pricing and disclosures | Protected catalog, Library, claims and triage records unchanged |

## Deliberately not added

No medical recommendation quiz, fabricated social proof, copied competitor design, dark-pattern urgency, popup email capture, automatic subscription selection, checkout flow, new health claim, unsourced article, or active analytics. No merge or deployment is part of this review.

## Measurement plan after approval

Establish a dated Search Console baseline before release, then compare at least two equivalent 28-day windows for organic impressions, clicks, CTR, queries and landing pages. Search Console does **not** measure all site visitors, product clicks, purchases or revenue; seasonality and content changes can confound comparisons.

If later authorized with an appropriate privacy design, separately measure anonymous navigation steps such as Library → product record → manufacturer handoff. External purchases require partner-side reporting and cannot be inferred from an outbound click. Do not collect health answers, personal information, or activate the dormant analytics implementation as part of this redesign.

Success should mean easier task completion, reliable mobile/keyboard use, retained trust, and eventually measured business outcomes—not simply a larger hero or an unsupported “conversion optimized” label.

## Complete 100-site review

**Scope key:** “HTML” means bounded public-document and route inspection. “Primary-page fallback” means the public page was read with web/browser tooling after the scripted fetch was blocked. “Desktop visual” means the rendered desktop page was also personally inspected. Watch-outs are design risks or transfer limitations unless explicitly described as an observed issue; they are not declarations that a business failed.
"""

def main():
    raw=json.loads(RAW.read_text(encoding='utf-8'))
    roster=json.loads((HERE/'benchmark-roster.json').read_text(encoding='utf-8'))
    notes={item['id']:item for item in json.loads((HERE/'benchmark-assessments.json').read_text(encoding='utf-8'))}
    by_id={item['id']:item for item in raw}
    assert len(roster)==len(by_id)==len(notes)==100
    assert set(by_id)==set(notes)==set(range(1,101))
    sections=[INTRO]
    summaries=[]
    names={'education-publisher':'Education and publishing references','testing-platform':'Testing and measurement references','education-led-brand':'Product and commerce references'}
    last=None
    for item in roster:
        row=by_id[item['id']]; note=notes[item['id']]
        scope=['HTML' if row.get('status')==200 else 'Primary-page fallback']
        if item['id'] in VISUAL:scope.append('Desktop visual')
        source=FALLBACK.get(item['id'],row.get('final_url',item['url']))
        summary={**item,'source_url':source,'checked_utc':row['checked_utc'],'review_scope':scope,
            'scripted_fetch_status':row.get('status'),'scripted_fetch_error':row.get('error'),
            'html_bytes':row.get('html_bytes'),'html_capture_cap_bytes':3000000,
            'images_in_initial_html':row.get('images_in_initial_html'),
            'scripts_in_initial_html':row.get('scripts_in_initial_html'),
            'performance_verdict':'Not established; HTML bytes are not full payload or Core Web Vitals',
            'business_outcome':'Unverified; no revenue, profitability, or conversion data',
            'strength':note['strength'],'watchout':note['watchout'],'application':note['application']}
        summaries.append(summary)
        if item['cohort']!=last:
            sections.append('\n### '+names.get(item['cohort'],item['cohort'])+'\n')
            last=item['cohort']
        sections.append(f"\n#### {item['id']:03d}. [{item['name']}]({source})\n\nScope: {' + '.join(scope)}.\n\n- **Strength:** {note['strength']}\n- **Watch-out / transfer limit:** {note['watchout']}\n- **Matrix application:** {note['application']}\n")
    sections.append('\n## Review integrity\n\nThis is original analysis linked to primary public sources. No competitor article, packaging, visual identity, ranking, certification or customer testimonial has been copied into the website. Raw excerpts remain outside version control and outside the public build. The separate QA report documents the candidate’s measured behavior and its remaining inherited editorial-review obligations.\n')
    (HERE/'RESEARCH_REPORT.md').write_text('\n'.join(sections),encoding='utf-8',newline='\n')
    (HERE/'benchmark-observations-summary.json').write_text(json.dumps(summaries,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'sites':len(summaries),'html':sum(r.get('status')==200 for r in raw),'fallback':len(FALLBACK),'desktop_visual':len(VISUAL),'cohorts':dict(Counter(x['cohort'] for x in roster))}))

if __name__=='__main__':main()
