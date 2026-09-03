import assert from 'node:assert/strict';
import test from 'node:test';

import {
   applyKeepOverrideButtonState,
   getKeepOverrideButtonState,
} from '../../scripts/itinerary/panel/components/removedItemsPopupKeepButtonState.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';

test('getKeepOverrideButtonState returns keep labels for unselected items', () => {
   assert.deepEqual(getKeepOverrideButtonState(false), {
      selected: false,
      textContent: APP_STRINGS.itinerary.removedItems.keepInItinerary,
      title: '',
      ariaPressed: 'false',
   });
});

test('getKeepOverrideButtonState returns remove labels for selected items', () => {
   assert.deepEqual(getKeepOverrideButtonState(true), {
      selected: true,
      textContent: APP_STRINGS.itinerary.dayPlanner.remove,
      title: APP_STRINGS.itinerary.removedItems.removeFromItineraryHint,
      ariaPressed: 'true',
   });
});

test('applyKeepOverrideButtonState syncs button presentation', () => {
   const button = createDomNode('button', 'itin-removed-keep-btn');

   applyKeepOverrideButtonState(button, getKeepOverrideButtonState(false));

   assert.equal(
      button.textContent,
      APP_STRINGS.itinerary.removedItems.keepInItinerary
   );
   assert.equal(button.getAttribute('aria-pressed'), 'false');
   assert.equal(button.classList.contains('is-selected'), false);

   applyKeepOverrideButtonState(button, getKeepOverrideButtonState(true));

   assert.equal(button.textContent, APP_STRINGS.itinerary.dayPlanner.remove);
   assert.equal(button.getAttribute('aria-pressed'), 'true');
   assert.equal(button.classList.contains('is-selected'), true);
   assert.equal(
      button.title,
      APP_STRINGS.itinerary.removedItems.removeFromItineraryHint
   );
});
