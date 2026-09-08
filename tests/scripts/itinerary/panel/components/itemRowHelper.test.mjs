import assert from 'node:assert/strict';
import test from 'node:test';

import { ItemRowHelper } from '../../../../../scripts/itinerary/panel/components/itemRowHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateItemNameElement_TestSpeciesAndPlain_ExpectPanelName', () => {
   const animalTitle = ItemRowHelper.createItemNameElement({
      species: 'African Lion',
      enclosureName: 'African Savanna',
   });
   assert.equal(animalTitle.className, 'itin-panel-name');
   assert.match(animalTitle.textContent, /African Lion/);

   const plainTitle = ItemRowHelper.createItemNameElement({
      name: 'Carousel',
      nameSuffix: ' • Open',
   });
   assert.equal(plainTitle.className, 'itin-panel-name');
   assert.match(plainTitle.textContent, /Carousel/);
});
