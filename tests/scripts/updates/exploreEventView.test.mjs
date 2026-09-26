import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreEventView } from '../../../scripts/updates/exploreEventView.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateEventCard_TestActive_ExpectVisibleCard', () => {
   const name = 'Fireworks';
   const description = 'Night show';

   const card = ExploreEventView.createEventCard({
      name,
      start_date: '2026-09-08',
      end_date: '2026-09-08',
      description,
   }, true);

   assert.equal(card.className, 'explore-update-card explore-event-card');
   assert.equal(card.hidden, false);
   assert.match(card.textContent, new RegExp(name));
   assert.match(card.textContent, new RegExp(description));
});


test('Test_CreateEventCard_TestInactive_ExpectHidden', () => {
   const name = 'Talk';

   const card = ExploreEventView.createEventCard({
      name,
      start_date: '2026-09-09',
      end_date: '2026-09-09',
   }, false);

   assert.equal(card.hidden, true);
});
