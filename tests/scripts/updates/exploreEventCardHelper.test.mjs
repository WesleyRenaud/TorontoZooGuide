import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreEventCardHelper } from '../../../scripts/updates/exploreEventCardHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateEventTitleEl_TestLinkedEvent_ExpectAnchorAndLocation', () => {
   const name = 'Fireworks';
   const location = 'Main Entrance';
   const link = 'https://example.test/event';

   const titleEl = ExploreEventCardHelper.createEventTitleEl({
      name,
      location,
      link,
   });
   const anchor = titleEl.children.at(Position.FIRST);

   assert.equal(titleEl.className, 'explore-update-title');
   assert.equal(anchor.tagName.toUpperCase(), 'A');
   assert.equal(anchor.href, link);
   assert.equal(anchor.textContent, name);
   assert.match(titleEl.textContent, new RegExp(location));
});


test('Test_CreateEventTitleEl_TestPlainEvent_ExpectTextOnly', () => {
   const name = 'Talk';

   const titleEl = ExploreEventCardHelper.createEventTitleEl({ name });

   assert.equal(titleEl.textContent, name);
});
