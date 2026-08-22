#!/usr/bin/env python3
"""Report horizontally overflowing elements for one local page."""
import argparse
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument("url");p.add_argument("--width",type=int,default=375);p.add_argument("--height",type=int,default=812);a=p.parse_args()
with sync_playwright() as api:
    browser=api.chromium.launch();page=browser.new_page(viewport={"width":a.width,"height":a.height});page.goto(a.url,wait_until="networkidle")
    print(page.evaluate("""()=>({overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,elements:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>document.documentElement.clientWidth+1||r.left<-1}).map(e=>({tag:e.tagName,cls:e.className,right:e.getBoundingClientRect().right,left:e.getBoundingClientRect().left})).slice(0,20)})"""));browser.close()
