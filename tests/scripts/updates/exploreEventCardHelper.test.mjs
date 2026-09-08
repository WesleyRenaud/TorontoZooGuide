import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreEventCardHelper } from '../../../scripts/updates/exploreEventCardHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateEventTitleEl_TestLinkedEvent_ExpectAnchorAndLocation', () => {
   const titleEl = ExploreEventCardHelper.createEventTitleEl({
      name: 'Fireworks',
      location: 'Main Entrance',
      link: 'https://example.test/event',
   });

   assert.equal(titleEl.className, 'explore-update-title');
   assert.equal(titleEl.children[0].tagName.toUpperCase(), 'A');
   assert.equal(titleEl.children[0].href, 'https://example.test/event');
   assert.equal(titleEl.children[0].textContent, 'Fireworks');
   assert.match(titleEl.textContent, /Main Entrance/);
});

test('Test_CreateEventTitleEl_TestPlainEvent_ExpectTextOnly', () => {
   const titleEl = ExploreEventCardHelper.createEventTitleEl({ name: 'Talk' });
   assert.equal(titleEl.textContent, 'Talk');
});
