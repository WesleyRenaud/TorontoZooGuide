import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreUpdateView } from '../../../scripts/updates/exploreUpdateView.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateUpdateCard_TestUpdate_ExpectCard', () => {
   const type = 'Animal Closure';
   const title = 'Lion exhibit closed';
   const description = 'Maintenance';

   const card = ExploreUpdateView.createUpdateCard({
      type,
      title,
      description,
   }, true);

   assert.equal(card.className, 'explore-update-card');
   assert.equal(card.hidden, false);
   assert.match(card.textContent, new RegExp(title));
   assert.match(card.textContent, new RegExp(description));
   assert.match(card.textContent, new RegExp(type));
});
