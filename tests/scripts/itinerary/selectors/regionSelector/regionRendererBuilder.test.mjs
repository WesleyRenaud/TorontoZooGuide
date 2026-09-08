import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionRendererBuilder } from '../../../../../scripts/itinerary/selectors/regionSelector/regionRendererBuilder.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateChoiceIndicator_TestSelected_ExpectMinus', () => {
   const selected = RegionRendererBuilder.createChoiceIndicator(true);
   assert.equal(selected.className, 'itin-add-btn is-added');
   assert.equal(selected.textContent, '−');

   const unselected = RegionRendererBuilder.createChoiceIndicator(false);
   assert.equal(unselected.className, 'itin-add-btn');
   assert.equal(unselected.textContent, '+');
});

test('Test_CreateChoiceRow_TestExhibit_ExpectDatasetAndLabel', () => {
   const button = RegionRendererBuilder.createChoiceRow({
      label: 'African Rainforest',
      isSelected: true,
      action: 'toggle-exhibit',
      regionName: 'Africa',
      exhibitName: 'African Rainforest',
   });

   assert.equal(button.type, 'button');
   assert.equal(button.dataset.action, 'toggle-exhibit');
   assert.equal(button.dataset.region, 'Africa');
   assert.equal(button.dataset.exhibit, 'African Rainforest');
   assert.match(button.textContent, /African Rainforest/);
   assert.match(button.textContent, /−/);
});

test('Test_CreateChoiceRow_TestRegionOnly_ExpectNoExhibitDataset', () => {
   const button = RegionRendererBuilder.createChoiceRow({
      label: 'Americas',
      isSelected: false,
      action: 'toggle-region',
      regionName: 'Americas',
   });

   assert.equal(button.dataset.exhibit, undefined);
   assert.match(button.textContent, /\+/);
});
