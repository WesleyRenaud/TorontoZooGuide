import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RemovedItemsFragment } from '../../../../../scripts/itinerary/panel/components/removedItemsFragment.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

const _removedAnimal = {
   species: 'African Lion',
   exhibit: 'Africa Savanna',
};

const _removedAttraction = {
   name: 'Conservation Carousel',
};

function _clickOverlay(overlay) {
   overlay.listeners.click?.({
      target: overlay,
      preventDefault() {},
      stopPropagation() {},
   });
}

installDomTestHooks();


test('Test_ShowRemovedItemsPopup_TestMissingMount_ExpectNoOp', () => {
   const mount = createDomNode('div');

   RemovedItemsFragment.showRemovedItemsPopup({
      mountEl: null,
      removed: { animals: [_removedAnimal] },
   });

   assert.equal(mount.children.length, 0);
});


test('Test_ShowRemovedItemsPopup_TestEmptyRemoved_ExpectNoOp', () => {
   const mount = createDomNode('div');

   RemovedItemsFragment.showRemovedItemsPopup({
      mountEl: mount,
      removed: { animals: [] },
   });

   assert.equal(mount.children.length, 0);
});


test('Test_ShowRemovedItemsPopup_TestAccept_ExpectKeptItems', () => {
   const mount = createDomNode('div');
   const accepted = [];

   RemovedItemsFragment.showRemovedItemsPopup({
      mountEl: mount,
      removed: {
         animals: [_removedAnimal],
         attractions: [_removedAttraction],
      },
      onAccept: (payload) => {
         accepted.push(payload);
      },
   });
   const keepButtons = mount.querySelectorAll('.itin-removed-keep-btn');
   keepButtons[Position.FIRST]?.click();
   keepButtons[Position.SECOND]?.click();
   mount.querySelector('.itin-finish')?.click();

   assert.equal(mount.children.length, 0);
   assert.deepEqual(accepted, [{
      animalsToKeep: [_removedAnimal],
      attractionsToKeep: [_removedAttraction.name],
   }]);
});


test('Test_ShowRemovedItemsPopup_TestCloseButton_ExpectDismiss', () => {
   const mount = createDomNode('div');
   const dismissCalls = [];

   RemovedItemsFragment.showRemovedItemsPopup({
      mountEl: mount,
      removed: { animals: [_removedAnimal] },
      onDismiss: () => {
         dismissCalls.push('dismissed');
      },
   });
   mount.querySelector('.itin-close')?.click();

   assert.deepEqual(dismissCalls, ['dismissed']);
   assert.equal(mount.children.length, 0);
});


test('Test_ShowRemovedItemsPopup_TestOverlayClick_ExpectDismiss', () => {
   const mount = createDomNode('div');
   const dismissCalls = [];

   RemovedItemsFragment.showRemovedItemsPopup({
      mountEl: mount,
      removed: { animals: [_removedAnimal] },
      onDismiss: () => {
         dismissCalls.push('overlay');
      },
   });
   const overlay = mount.querySelector('.itin-overlay');
   _clickOverlay(overlay);

   assert.deepEqual(dismissCalls, ['overlay']);
   assert.equal(mount.children.length, 0);
});


test('Test_ShowRemovedItemsPopup_TestToggleKeepOff_ExpectEmptyAccept', () => {
   const mount = createDomNode('div');
   const accepted = [];

   RemovedItemsFragment.showRemovedItemsPopup({
      mountEl: mount,
      removed: { animals: [_removedAnimal] },
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
});


test('Test_ShowRemovedItemsPopup_TestViewAlternatives_ExpectNavigates', () => {
   const mount = createDomNode('div');
   const viewedSteps = [];
   const talkName = 'African Lion';
   const location = 'Africa Savanna';

   RemovedItemsFragment.showRemovedItemsPopup({
      mountEl: mount,
      removed: {
         guardiansTalks: [{
            name: talkName,
            location,
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
