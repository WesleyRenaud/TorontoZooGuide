import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupLayoutView } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupLayoutView.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateRemovedItemsPopupLayout_TestDefault_ExpectChangedCopy', () => {
   const layout = RemovedItemsPopupLayoutView.createRemovedItemsPopupLayout();

   assert.equal(layout.root.className, 'tzg-popup');
   assert.equal(layout.overlay.className, 'itin-overlay');
   assert.equal(layout.closeBtn.type, 'button');
   assert.equal(layout.okBtn.type, 'button');
   assert.equal(layout.okBtn.textContent, Strings.itinerary.actions.accept);
   assert.equal(
      layout.content.className,
      'itin-removed-popup-content'
   );
   assert.ok(
      layout.content.textContent.includes(Strings.itinerary.removedItems.someDetailsChanged)
   );
   assert.ok(
      layout.content.textContent.includes(Strings.itinerary.removedItems.changedSubtitle)
   );
   assert.ok(
      layout.root.textContent.includes(Strings.itinerary.removedItems.itineraryUpdated)
   );
});

test('Test_CreateRemovedItemsPopupLayout_TestEmptyItinerary_ExpectEmptyCopy', () => {
   const layout = RemovedItemsPopupLayoutView.createRemovedItemsPopupLayout({
      isEmptyItinerary: true,
   });

   assert.equal(
      layout.content.className,
      'itin-removed-popup-content itin-removed-popup-content-empty'
   );
   assert.ok(
      layout.content.textContent.includes(Strings.itinerary.removedItems.emptyItineraryTitle)
   );
   assert.ok(
      layout.content.textContent.includes(Strings.itinerary.removedItems.emptyItinerarySubtitle)
   );
});
