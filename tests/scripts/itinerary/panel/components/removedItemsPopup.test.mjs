import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RemovedItemsPopup } from '../../../../../scripts/itinerary/panel/components/removedItemsPopup.js';
import { SpeciesExhibitKey } from '../../../../../scripts/itinerary/speciesExhibitKey.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

const removedAnimal = {
   species: 'African Lion',
   exhibit: 'Africa Savanna',
};

const removedAttraction = {
   name: 'Conservation Carousel',
};

function clickOverlay(overlay) {
   overlay.listeners.click?.({
      target: overlay,
      preventDefault() {},
      stopPropagation() {},
   });
}

test.describe('showRemovedItemsPopup', () => {
   installDomTestHooks();

   test('Test_Returns_TestReturnsEarlyWithoutAMountElementOrPopup_ExpectOk', () => {
      const mount = createDomNode('div');

      RemovedItemsPopup.showRemovedItemsPopup({
         mountEl: null,
         removed: { animals: [removedAnimal] },
      });
      RemovedItemsPopup.showRemovedItemsPopup({
         mountEl: mount,
         removed: { animals: [] },
      });

      assert.equal(mount.children.length, 0);
   });

   test('Test_Accept_TestAcceptPassesKeptAnimalsAndAttractionsToOnAccept_ExpectOk', () => {
      const mount = createDomNode('div');
      const accepted = [];

      RemovedItemsPopup.showRemovedItemsPopup({
         mountEl: mount,
         removed: {
            animals: [removedAnimal],
            attractions: [removedAttraction],
         },
         onAccept: (payload) => {
            accepted.push(payload);
         },
      });

      const keepButtons = mount.querySelectorAll('.itin-removed-keep-btn');

      keepButtons[0]?.click();
      keepButtons[1]?.click();
      mount.querySelector('.itin-finish')?.click();

      assert.equal(mount.children.length, 0);
      assert.deepEqual(accepted, [{
         animalsToKeep: [{
            species: 'African Lion',
            exhibit: 'Africa Savanna',
         }],
         attractionsToKeep: ['Conservation Carousel'],
      }]);
   });

   test('Test_Dismisses_TestDismissesThroughTheCloseButtonAndOverlayClick_ExpectOk', () => {
      const mount = createDomNode('div');
      const dismissCalls = [];

      RemovedItemsPopup.showRemovedItemsPopup({
         mountEl: mount,
         removed: { animals: [removedAnimal] },
         onDismiss: () => {
            dismissCalls.push('dismissed');
         },
      });

      mount.querySelector('.itin-close')?.click();

      assert.deepEqual(dismissCalls, ['dismissed']);
      assert.equal(mount.children.length, 0);

      RemovedItemsPopup.showRemovedItemsPopup({
         mountEl: mount,
         removed: { animals: [removedAnimal] },
         onDismiss: () => {
            dismissCalls.push('overlay');
         },
      });

      const overlay = mount.querySelector('.itin-overlay');

      clickOverlay(overlay);

      assert.deepEqual(dismissCalls, ['dismissed', 'overlay']);
      assert.equal(mount.children.length, 0);
   });

   test('Test_Toggle_TestToggleKeepOffRemovesItemsFromTheAccept_ExpectOk', () => {
      const mount = createDomNode('div');
      const accepted = [];

      RemovedItemsPopup.showRemovedItemsPopup({
         mountEl: mount,
         removed: { animals: [removedAnimal] },
         onAccept: (payload) => {
            accepted.push(payload);
         },
      });

      const keepButton = mount.querySelector('.itin-removed-keep-btn');

      keepButton?.click();
      keepButton?.click();
      mount.querySelector('.itin-finish')?.click();

      assert.deepEqual(accepted, [{
         animalsToKeep: [],
         attractionsToKeep: [],
      }]);
      assert.equal(
         SpeciesExhibitKey.buildSpeciesExhibitKey(removedAnimal),
         'african lion|africa savanna'
      );
   });

   test('Test_View_TestViewAlternativesRemovesThePopupBeforeNavigating_ExpectOk', () => {
      const mount = createDomNode('div');
      const viewedSteps = [];

      RemovedItemsPopup.showRemovedItemsPopup({
         mountEl: mount,
         removed: {
            guardiansTalks: [{
               name: 'African Lion',
               location: 'Africa Savanna',
            }],
         },
         removePopupOnly: undefined,
         onViewAlternatives: (stepKey) => {
            viewedSteps.push(stepKey);
         },
      });

      const alternativesButton = mount.querySelector('.itin-removed-alt-btn');

      alternativesButton?.click();

      assert.deepEqual(viewedSteps, ['guardiansTalks']);
      assert.equal(mount.children.length, 0);
   });
});
