import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreEventView } from '../../../scripts/updates/exploreEventView.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEventCard_TestActiveAndInactive_ExpectCard', () => {
   const active = ExploreEventView.createEventCard({
      name: 'Fireworks',
      start_date: '2026-09-08',
      end_date: '2026-09-08',
      description: 'Night show',
   }, true);
   const inactive = ExploreEventView.createEventCard({
      name: 'Talk',
      start_date: '2026-09-09',
      end_date: '2026-09-09',
   }, false);

   assert.equal(active.className, 'explore-update-card explore-event-card');
   assert.equal(active.hidden, false);
   assert.match(active.textContent, /Fireworks/);
   assert.match(active.textContent, /Night show/);
   assert.equal(inactive.hidden, true);
});
