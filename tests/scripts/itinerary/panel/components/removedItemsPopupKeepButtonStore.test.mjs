import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupKeepButtonStore } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupKeepButtonStore.js';
import { Strings } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';


test('Test_GetKeepOverrideButtonState_TestUnselected_ExpectKeepLabels', () => {
   const isSelected = false;

   const state = RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState(isSelected);

   assert.equal(state.selected, isSelected);
   assert.equal(state.textContent, Strings.itinerary.removedItems.keepInItinerary);
   assert.equal(state.title, '');
   assert.equal(state.ariaPressed, String(isSelected));
});


test('Test_GetKeepOverrideButtonState_TestSelected_ExpectRemoveLabels', () => {
   const isSelected = true;

   const state = RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState(isSelected);

   assert.equal(state.selected, isSelected);
   assert.equal(state.textContent, Strings.itinerary.dayPlanner.remove);
   assert.equal(state.title, Strings.itinerary.removedItems.removeFromItineraryHint);
   assert.equal(state.ariaPressed, String(isSelected));
});


test('Test_ApplyKeepOverrideButtonState_TestUnselected_ExpectKeepPresentation', () => {
   const button = createDomNode('button', 'itin-removed-keep-btn');
   const state = RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState(false);

   RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState(button, state);

   assert.equal(button.textContent, state.textContent);
   assert.equal(button.getAttribute('aria-pressed'), state.ariaPressed);
   assert.equal(button.classList.contains('is-selected'), state.selected);
});


test('Test_ApplyKeepOverrideButtonState_TestSelected_ExpectRemovePresentation', () => {
   const button = createDomNode('button', 'itin-removed-keep-btn');
   const state = RemovedItemsPopupKeepButtonStore.getKeepOverrideButtonState(true);

   RemovedItemsPopupKeepButtonStore.applyKeepOverrideButtonState(button, state);

   assert.equal(button.textContent, state.textContent);
   assert.equal(button.getAttribute('aria-pressed'), state.ariaPressed);
   assert.equal(button.classList.contains('is-selected'), state.selected);
   assert.equal(button.title, state.title);
});
