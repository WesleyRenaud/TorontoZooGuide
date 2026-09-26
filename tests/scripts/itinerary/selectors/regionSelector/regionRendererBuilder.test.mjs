import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionRendererBuilder } from '../../../../../scripts/itinerary/selectors/regionSelector/regionRendererBuilder.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateChoiceIndicator_TestSelected_ExpectMinus', () => {
   const selected = true;

   const indicator = RegionRendererBuilder.createChoiceIndicator(selected);

   assert.equal(indicator.className, 'itin-add-btn is-added');
   assert.equal(indicator.textContent, '−');
});


test('Test_CreateChoiceIndicator_TestUnselected_ExpectPlus', () => {
   const selected = false;

   const indicator = RegionRendererBuilder.createChoiceIndicator(selected);

   assert.equal(indicator.className, 'itin-add-btn');
   assert.equal(indicator.textContent, '+');
});


test('Test_CreateChoiceRow_TestExhibit_ExpectDatasetAndLabel', () => {
   const label = 'African Rainforest';
   const action = 'toggle-exhibit';
   const regionName = 'Africa';
   const exhibitName = label;

   const button = RegionRendererBuilder.createChoiceRow({
      label,
      isSelected: true,
      action,
      regionName,
      exhibitName,
   });

   assert.equal(button.type, 'button');
   assert.equal(button.dataset.action, action);
   assert.equal(button.dataset.region, regionName);
   assert.equal(button.dataset.exhibit, exhibitName);
   assert.match(button.textContent, new RegExp(label));
   assert.match(button.textContent, /−/);
});


test('Test_CreateChoiceRow_TestRegionOnly_ExpectNoExhibitDataset', () => {
   const label = 'Americas';
   const action = 'toggle-region';
   const regionName = label;

   const button = RegionRendererBuilder.createChoiceRow({
      label,
      isSelected: false,
      action,
      regionName,
   });

   assert.equal(button.dataset.exhibit, undefined);
   assert.match(button.textContent, /\+/);
});
