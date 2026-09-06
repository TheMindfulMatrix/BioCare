"""Export the candidate's canonical pages/assets with GitHub/Linux text bytes."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.site_paths import audited_page_paths
from scripts.daily_audit import asset_paths,build_bytes

def main():
    output=ROOT/'_preview/research-led-experience/production-style'
    pages=audited_page_paths(ROOT)
    paths={p or 'index.html' for p in pages}
    paths.update(asset_paths(ROOT,pages))
    paths.update({'robots.txt','sitemap.xml','CNAME'})
    for relative in sorted(paths):
        target=output/relative
        assert target.resolve().is_relative_to(output.resolve())
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(build_bytes(ROOT/relative))
    print(json.dumps({'exported_files':len(paths),'text_line_endings':'LF, matching existing audit build_bytes and GitHub Linux checkout'}))

if __name__=='__main__':main()
