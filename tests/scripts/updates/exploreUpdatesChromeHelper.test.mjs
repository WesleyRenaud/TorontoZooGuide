import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreUpdatesChromeHelper } from '../../../scripts/updates/exploreUpdatesChromeHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateArrowButton_TestConfig_ExpectButton', () => {
   let clicks = Position.FIRST;
   const label = 'Next update';
   const symbol = '>';

   const buttonEl = ExploreUpdatesChromeHelper.createArrowButton({
      label,
      symbol,
      onClick: () => { clicks += 1; },
   });
   buttonEl.click();

   assert.equal(buttonEl.type, 'button');
   assert.equal(buttonEl.className, 'explore-update-arrow');
   assert.equal(buttonEl.textContent, symbol);
   assert.equal(buttonEl.getAttribute('aria-label'), label);
   assert.equal(clicks, Position.SECOND);
});
