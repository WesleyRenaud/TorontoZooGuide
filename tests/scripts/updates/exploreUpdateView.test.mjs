import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreUpdateView } from '../../../scripts/updates/exploreUpdateView.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateUpdateCard_TestUpdate_ExpectCard', () => {
   const card = ExploreUpdateView.createUpdateCard({
      type: 'Animal Closure',
      title: 'Lion exhibit closed',
      description: 'Maintenance',
   }, true);

   assert.equal(card.className, 'explore-update-card');
   assert.equal(card.hidden, false);
   assert.match(card.textContent, /Lion exhibit closed/);
   assert.match(card.textContent, /Maintenance/);
   assert.match(card.textContent, /Animal Closure/);
});
