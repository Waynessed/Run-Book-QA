import {test,expect} from '@playwright/test';
const fixture={status:'answered',reason:'',claims:[{text:'Check the configured audience.',citation_ids:['auth:1:checks:0']}],passages:[{id:'auth:1:checks:0',document_id:'auth',title:'Auth',version:'1',heading:'Checks',section_id:'checks',text:'Check the configured audience.'}],latency_ms:25,retrieval_mode:'keyword',model_version:'fixture',corpus_version:'fixture'};
test('supported answer opens actual source endpoint',async({page})=>{
 if(!process.env.REAL_MODEL){
  await page.route('**/readyz',r=>r.fulfill({json:{status:'ready'}}));
  await page.route('**/v1/ask',r=>r.fulfill({json:fixture}));
  await page.route('**/v1/documents/auth',r=>r.fulfill({json:{title:'Auth',version:'1',markdown:'## Checks\nCheck the configured audience.'}}));
 }
 await page.goto('/');await page.getByRole('button',{name:'Ask runbooks'}).click();
 await expect(page.locator('.claim')).not.toHaveCount(0,{timeout:250000});
 await page.locator('.citation').first().click();
 await expect(page.locator('.source blockquote')).toBeVisible();
 await expect(page.locator('.source pre')).toBeVisible();
 if(process.env.REAL_MODEL){await page.screenshot({path:'../docs/assets/final-demo.png',fullPage:true});}
});
test('unsupported question abstains',async({page})=>{
 if(!process.env.REAL_MODEL){
  await page.route('**/readyz',r=>r.fulfill({json:{status:'ready'}}));
  await page.route('**/v1/ask',r=>r.fulfill({json:{...fixture,status:'abstained',claims:[],passages:[],reason:'No supporting evidence.'}}));
 }
 await page.goto('/');await page.getByLabel('What are you investigating?').fill('What is the office Wi-Fi password?');await page.getByRole('button',{name:'Ask runbooks'}).click();
 await expect(page.getByRole('heading',{name:'Insufficient evidence'})).toBeVisible({timeout:250000});
});
test('model error is visible',async({page})=>{
 await page.route('**/v1/ask',r=>r.fulfill({status:503,json:{detail:'Local model timed out after 120 seconds'}}));
 await page.goto('/');await page.getByRole('button',{name:'Ask runbooks'}).click();
 await expect(page.getByRole('alert')).toContainText('timed out');
});

test('comparison distinguishes unreviewed scores from recorded inspection',async({page})=>{
 await page.route('**/readyz',r=>r.fulfill({json:{status:'ready'}}));
 const metrics={recall_at_5:.9,answer_correctness:null,supported_claim_rate:null,unsupported_abstention:1,answerable_coverage:.8,p95_latency_ms:40000,valid_citation_rate:1,model_errors:2,policy_rejection_attempts:2,median_latency_ms:20000,semantic_review_status:'pending'};
 let reviewed=false;
 await page.route('**/v1/evaluation/latest',r=>r.fulfill({json:{split:'development',rows:[{}],modes:{hybrid:reviewed?{...metrics,answer_correctness:.75,supported_claim_rate:.5,semantic_review_status:'reviewed',adversarial_instruction_failures:1,reviewer:'Fixture rubric reviewer'}:metrics}}}));
 await page.goto('/');
 await expect(page.locator('.evaluation')).toContainText('Unreviewed');
 await expect(page.locator('.review-provenance')).toContainText('await recorded rubric review');
 reviewed=true;await page.reload();
 await expect(page.locator('.review-provenance')).toContainText('Fixture rubric reviewer');
 await expect(page.locator('.evaluation')).toContainText('75.0%');
 await expect(page.getByRole('table',{name:'Validation and failures'})).toContainText('100.0%');
 await expect(page.getByRole('table',{name:'Validation and failures'})).toContainText('20.0s');
 await expect(page.getByRole('columnheader',{name:'Rejected directives'})).toBeVisible();
});

test('recorded preview displays saved answer, source and evaluation limits',async({page})=>{
 test.skip(!process.env.RECORDED_DEMO,'Run against the recorded preview build');
 await page.setViewportSize({width:1280,height:950});
 await page.goto('/Run-Book-QA/');
 await expect(page.getByText('Recorded recruiter preview')).toBeVisible();
 await expect(page.getByText('This static page does not generate new answers.',{exact:false})).toBeVisible();
 await page.getByRole('button',{name:'Show recorded answer'}).click();
 await expect(page.locator('.claim')).not.toHaveCount(0);
 await expect(page.locator('.review-note')).toContainText('claims supported');
 await page.screenshot({path:'../docs/assets/recorded-preview.png'});
 await page.locator('.citation').first().click();
 await expect(page.locator('.source blockquote')).toBeVisible();
 await expect(page.locator('.source pre')).toBeVisible();
 await expect(page.locator('.evaluation')).toContainText('87.5%');
 await page.locator('.source blockquote').screenshot({path:'../docs/assets/recorded-source.png'});
 await page.getByRole('button',{name:'What is the office Wi-Fi password?'}).click();
 await page.getByRole('button',{name:'Show recorded answer'}).click();
 await expect(page.getByRole('heading',{name:'Insufficient evidence'})).toBeVisible();
});
