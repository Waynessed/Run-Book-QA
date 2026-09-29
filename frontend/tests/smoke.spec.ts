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
