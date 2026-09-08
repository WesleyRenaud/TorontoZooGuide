import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreUpdatesChromeHelper } from '../../../scripts/updates/exploreUpdatesChromeHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateArrowButton_TestConfig_ExpectButton', () => {
   let clicks = 0;
   const buttonEl = ExploreUpdatesChromeHelper.createArrowButton({
      label: 'Next update',
      symbol: '>',
      onClick: () => { clicks += 1; },
   });

   assert.equal(buttonEl.type, 'button');
   assert.equal(buttonEl.className, 'explore-update-arrow');
   assert.equal(buttonEl.textContent, '>');
   assert.equal(buttonEl.getAttribute('aria-label'), 'Next update');
   buttonEl.click();
   assert.equal(clicks, 1);
});
