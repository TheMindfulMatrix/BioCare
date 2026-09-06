const {test} = require('node:test');
const assert = require('node:assert/strict');
const M = require('../assets/js/growth-measurement.js');

test('disabled and transport-missing states never emit', () => {
  let calls=0;
  assert.equal(M.createTracker({send:()=>calls++}).track('page_view',{}),false);
  assert.equal(M.createTracker({enabled:true}).active,false);
  assert.equal(calls,0);
});
test('sensitive input never reaches the allowlisted payload', () => {
  const payload=M.event('manufacturer_click',{pathname:'/products/biolimitless-vitamin-d3-k2.html',search:'?q=private-health-detail&utm_source=instagram&utm_campaign=private-name',referrer:'https://example.com/patient?email=private@example.com',merchant:'zinzino',email:'private@example.com',product:'secret',testResult:4});
  assert.deepEqual(payload,{action:'manufacturer_click',section:'products',source:'instagram',merchant:'zinzino'});
  assert.equal(Object.isFrozen(payload),true);
});
test('raw search terms and unknown campaign values are discarded',()=>{
  assert.equal(M.source('?utm_source=private@example.com',''),'direct_or_unknown');
  assert.equal(M.source('?q=private','https://google.com/search?q=private'),'google');
  assert.equal(M.source('','https://google.com.evil.example/'),'other_referral');
});
test('root and legacy-subpath routes map only to broad groups',()=>{
  assert.equal(M.section('/BioCare/library/health-topic.html'),'library');
  assert.equal(M.section('/know-your-number.html'),'journeys');
  assert.equal(M.section('/private-person'),'other');
  assert.equal(M.section('/about.html'),'business');
});
test('unknown actions, merchants and fake purchase events are rejected',()=>{
  assert.equal(M.event('purchase',{}),null);
  assert.equal(M.event('subscription_confirmed',{}),null);
  assert.equal(M.event('manufacturer_click',{merchant:'other'}),null);
});
test('repeated page views and accidental rapid clicks are deduplicated',()=>{
  let clock=0; const payloads=[];
  const tracker=M.createTracker({enabled:true,send:p=>payloads.push(p),now:()=>clock});
  assert.equal(tracker.track('page_view',{pathname:'/'}),true);
  clock=2000; assert.equal(tracker.track('page_view',{pathname:'/'}),false);
  assert.equal(tracker.track('contact_click',{}),true);
  assert.equal(tracker.track('contact_click',{}),false);
  clock+=1500; assert.equal(tracker.track('contact_click',{}),true);
  assert.equal(payloads.length,3);
});
test('transport failures are contained without retries or logging private data',async()=>{
  assert.equal(M.createTracker({enabled:true,send:()=>{throw Error('offline')}}).track('page_view',{}),false);
  assert.equal(M.createTracker({enabled:true,send:()=>Promise.reject(Error('offline'))}).track('page_view',{}),true);
  await new Promise(resolve=>setImmediate(resolve));
});
test('a disabled binding attaches no handlers',()=>{
  const doc={addEventListener:()=>{throw Error('unexpected listener')}};
  assert.equal(M.bind(doc).active,false);
});
test('active document binding is idempotent and sends no destination URLs',()=>{
  const handlers={}, out=[];
  const doc={referrer:'https://threads.com/@test',defaultView:{location:{pathname:'/products/private.html',search:'?q=private',href:'https://themindfulmatrixhealth.com/products/private.html',origin:'https://themindfulmatrixhealth.com'}},addEventListener:(name,fn)=>handlers[name]=fn};
  const first=M.bind(doc,{enabled:true,send:p=>out.push(p)});
  assert.equal(M.bind(doc,{enabled:true,send:()=>{throw Error('duplicate')}}),first);
  handlers.click({target:{closest:()=>({href:'https://www.zinzino.com/shop/123?private=yes',relList:{contains:()=>true}})}});
  assert.equal(out.length,2);
  assert.deepEqual(out[1],{action:'manufacturer_click',section:'products',source:'threads',merchant:'zinzino'});
});
