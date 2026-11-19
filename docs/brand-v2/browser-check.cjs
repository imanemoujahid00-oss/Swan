const {chromium}=require('/Users/imanemoujahid/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
const out=__dirname;
const checks=[],failures=[],network=[];
function assert(c,m){if(!c) throw Error(m);checks.push(m);}
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:fs.existsSync(chromium.executablePath())?chromium.executablePath():'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--no-sandbox']});
 for(const width of [1440,390]){
  const context=await browser.newContext({viewport:{width,height:width===390?844:1000},deviceScaleFactor:1,ignoreHTTPSErrors:true,reducedMotion:"reduce"});
  const page=await context.newPage();page.on('pageerror',e=>failures.push(e.message));
  page.on('requestfailed',r=>network.push({url:r.url(),error:r.failure()?.errorText}));
  await page.goto('http://127.0.0.1:8080/',{waitUntil:'networkidle'});
  await page.evaluate(()=>document.fonts.ready);
  const loadedFaces=await page.evaluate(()=>Array.from(document.fonts).filter(f=>f.status==='loaded').map(f=>f.family));
  assert(loadedFaces.includes('Bebas Neue') && loadedFaces.includes('Barlow'),`Actual Google Font faces loaded ${width}`);
  assert(await page.evaluate(()=>document.fonts.check('30px "Bebas Neue"')&&document.fonts.check('16px Barlow')),`Fonts loaded ${width}`);
  async function view(name){await page.locator(`#frame[data-view="${name}"]`).waitFor();await page.waitForTimeout(50);}
  async function capture(name){
   await page.mouse.move(0,0);
   const metrics=await page.evaluate(()=>{
    const b=document.querySelector('.brand-word').getBoundingClientRect(),reset=document.querySelector('#reset').getBoundingClientRect(),header=document.querySelector('.header').getBoundingClientRect();
    return {width:innerWidth,scroll:document.documentElement.scrollWidth,brand:{left:b.left,right:b.right,height:b.height},reset:{left:reset.left},header:{left:header.left,right:header.right},fonts:{heading:getComputedStyle(document.querySelector('h1')).fontFamily,body:getComputedStyle(document.body).fontFamily}};
   });
   assert(metrics.scroll<=width,`No horizontal overflow ${name} ${width}`);
   assert(metrics.brand.right<metrics.reset.left && metrics.brand.left>=metrics.header.left && metrics.brand.right<=metrics.header.right,`Wordmark contained without overlap ${name} ${width}`);
   const contrasts=await page.locator('.primary').evaluateAll(nodes=>nodes.map(n=>{const s=getComputedStyle(n);return {color:s.color,background:s.backgroundColor,size:parseFloat(s.fontSize),weight:parseFloat(s.fontWeight)}}));
   function luminance(colour){const c=colour.match(/\d+(?:\.\d+)?/g).slice(0,3).map(v=>+v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722;}
   for(const style of contrasts){const a=luminance(style.color),b=luminance(style.background),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);const large=(style.weight>=700&&style.size>=18.667)||style.size>=24;assert(ratio>=(large?3:4.5),`Primary button contrast AA ${name} ${width}`);}
   await page.screenshot({path:path.join(out,'screenshots',`${name}-${width}.png`),fullPage:true});
   checks.push({screen:name,width,metrics});
  }
  await capture('welcome');
  const concerns=['Acne-prone skin and blemishes','Dryness and skin barrier','Sensitive or easily irritated skin'];
  for(let i=0;i<concerns.length;i++){
   await page.locator('#reset').click();await view('welcome');await page.getByRole('button',{name:'Build my routine',exact:true}).click();await view('adult');
   if(i===0) await capture('profile-first');
   // Exercise required-answer validation before filling the first question.
   if(i===0){await page.locator('#next').click();assert((await page.locator('#error').innerText()).includes('Choose an answer'),`Required answer validation ${width}`);}
   await page.getByRole('radio',{name:'Yes',exact:true}).check();await page.locator('#next').click();await view('safety');
   await page.getByRole('checkbox',{name:'None of the above',exact:true}).check();await page.locator('#next').click();await view('concerns');
   await page.locator('label.option').filter({has:page.locator('strong',{hasText:concerns[i]})}).locator('input').check();
   await page.locator('#next').click();
   if(i===0){await view('blemishes');await page.getByRole('radio',{name:'Several small spots or clogged pores',exact:true}).check();await page.locator('#next').click();}
   await view('skin');await page.getByRole('radio',{name:i===1?'Dry':i===0?'Oily':'Normal',exact:true}).check();await page.locator('#next').click();await view('reactivity');
   await page.getByRole('radio',{name:'No',exact:true}).check();await page.locator('#next').click();await view('cleanser');
   if(i===0){await page.locator('label.option').filter({has:page.locator('strong',{hasText:'No preference'})}).locator('input').check();await capture('profile-last');}
   await page.locator('#next').click();await view('review');await page.getByRole('button',{name:'See my routine',exact:true}).click();await view('results');
   await page.locator('#routine-output .routine article').first().waitFor();
   assert(await page.locator('#routine-output article').count()===3,`Three routine products ${concerns[i]} ${width}`);
   assert((await page.locator('#routine-output').innerText()).toLowerCase().includes('facial sunscreen'),`Sunscreen returned ${concerns[i]} ${width}`);
   if(i===0){
    await page.waitForFunction(()=>Array.from(document.querySelectorAll('.purchase-preview img')).every(i=>i.complete),{timeout:15000}).catch(()=>{});
    await capture('routine');
   }
  }
  // A referral screen through the actual form, then return with answers retained.
  await page.locator('#reset').click();await view('welcome');await page.getByRole('button',{name:'Build my routine',exact:true}).click();await view('adult');
  await page.getByRole('radio',{name:'No',exact:true}).check();await page.locator('#next').click();await view('guidance');
  assert((await page.locator('#screen').innerText()).includes('18 or over'),`Under-18 referral preserved ${width}`);await capture('referral');
  await page.getByRole('button',{name:'Edit my answers',exact:true}).click();await view('adult');
  assert(await page.getByRole('radio',{name:'No',exact:true}).isChecked(),`Edit retains answer ${width}`);
  for(const [flag,expected] of [
   ['I use a prescribed skincare treatment','prescribing clinician'],
   ['I am pregnant or breastfeeding','pregnancy or breastfeeding'],
   ['I have a sudden, severe, painful, or unusual skin change','healthcare professional'],
   ['I have a known allergy to a skincare ingredient','specific ingredient allergy']
  ]){
   await page.locator('#reset').click();await view('welcome');await page.getByRole('button',{name:'Build my routine',exact:true}).click();await view('adult');
   await page.getByRole('radio',{name:'Yes',exact:true}).check();await page.locator('#next').click();await view('safety');
   await page.getByRole('checkbox',{name:flag,exact:true}).check();await page.locator('#next').click();await view('guidance');
   assert((await page.locator('#screen').innerText()).includes(expected),`Referral ${flag} ${width}`);
  }
  await context.close();
 }
 await browser.close();
 fs.writeFileSync(path.join(out,'browser-checks.json'),JSON.stringify({checks,failures,network},null,2));
 assert(failures.length===0,'No browser JavaScript errors');
 console.log(JSON.stringify({checks:checks.length,screenshots:10,failures,network},null,2));
})().catch(e=>{console.error(e);process.exit(1)});
