import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupKeepButtonStore } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupKeepButtonStore.js';
import { Strings } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';

test('Test_GetKeepOverrideButtonState_TestUnselected_ExpectKeepLabels', () => {
   assert.deepEqual(RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState(false), {
      selected: false,
      textContent: Strings.itinerary.removedItems.keepInItinerary,
      title: '',
      ariaPressed: 'false',
   });
});

test('Test_GetKeepOverrideButtonState_TestSelected_ExpectRemoveLabels', () => {
   assert.deepEqual(RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState(true), {
      selected: true,
      textContent: Strings.itinerary.dayPlanner.remove,
      title: Strings.itinerary.removedItems.removeFromItineraryHint,
      ariaPressed: 'true',
   });
});

test('Test_ApplyKeepOverrideButtonState_TestToggle_ExpectSyncedPresentation', () => {
   const button = createDomNode('button', 'itin-removed-keep-btn');

   RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState(button, RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState(false));

   assert.equal(
      button.textContent,
      Strings.itinerary.removedItems.keepInItinerary
   );
   assert.equal(button.getAttribute('aria-pressed'), 'false');
   assert.equal(button.classList.contains('is-selected'), false);

   RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState(button, RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState(true));

   assert.equal(button.textContent, Strings.itinerary.dayPlanner.remove);
   assert.equal(button.getAttribute('aria-pressed'), 'true');
   assert.equal(button.classList.contains('is-selected'), true);
   assert.equal(
      button.title,
      Strings.itinerary.removedItems.removeFromItineraryHint
   );
});
