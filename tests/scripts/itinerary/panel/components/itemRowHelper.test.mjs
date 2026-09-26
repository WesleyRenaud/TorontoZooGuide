import assert from 'node:assert/strict';
import test from 'node:test';

import { ItemRowHelper } from '../../../../../scripts/itinerary/panel/components/itemRowHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateItemNameElement_TestSpecies_ExpectPanelName', () => {
   const species = 'African Lion';
   const enclosureName = 'African Savanna';

   const animalTitle = ItemRowHelper.createItemNameElement({
      species,
      enclosureName,
   });

   assert.equal(animalTitle.className, 'itin-panel-name');
   assert.match(animalTitle.textContent, new RegExp(species));
});


test('Test_CreateItemNameElement_TestPlainName_ExpectPanelName', () => {
   const name = 'Conservation Carousel';
   const nameSuffix = ' • Open';

   const plainTitle = ItemRowHelper.createItemNameElement({
      name,
      nameSuffix,
   });

   assert.equal(plainTitle.className, 'itin-panel-name');
   assert.match(plainTitle.textContent, new RegExp(name));
});
