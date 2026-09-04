import assert from 'node:assert/strict';
import { test } from 'node:test';

import { showRemovedItemsPopup } from '../../scripts/itinerary/panel/components/removedItemsPopup.js';
import { SpeciesExhibitKey } from '../../scripts/itinerary/speciesExhibitKey.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

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

   test('returns early without a mount element or popup content', () => {
      const mount = createDomNode('div');

      showRemovedItemsPopup({
         mountEl: null,
         removed: { animals: [removedAnimal] },
      });
      showRemovedItemsPopup({
         mountEl: mount,
         removed: { animals: [] },
      });

      assert.equal(mount.children.length, 0);
   });

   test('accept passes kept animals and attractions to onAccept', () => {
      const mount = createDomNode('div');
      const accepted = [];

      showRemovedItemsPopup({
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

   test('dismisses through the close button and overlay click', () => {
      const mount = createDomNode('div');
      const dismissCalls = [];

      showRemovedItemsPopup({
         mountEl: mount,
         removed: { animals: [removedAnimal] },
         onDismiss: () => {
            dismissCalls.push('dismissed');
         },
      });

      mount.querySelector('.itin-close')?.click();

      assert.deepEqual(dismissCalls, ['dismissed']);
      assert.equal(mount.children.length, 0);

      showRemovedItemsPopup({
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

   test('toggle keep off removes items from the accept payload', () => {
      const mount = createDomNode('div');
      const accepted = [];

      showRemovedItemsPopup({
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

   test('view alternatives removes the popup before navigating', () => {
      const mount = createDomNode('div');
      const viewedSteps = [];

      showRemovedItemsPopup({
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
