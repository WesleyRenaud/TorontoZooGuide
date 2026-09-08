import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionRenderer } from '../../../../../scripts/itinerary/selectors/regionSelector/regionRenderer.js';
import { RegionStore } from '../../../../../scripts/itinerary/selectors/regionSelector/regionStore.js';
import { RegionRendererBuilder } from '../../../../../scripts/itinerary/selectors/regionSelector/regionRendererBuilder.js';

test('Test_BuildRegionRows_TestExhibits_ExpectRegionAndExhibitRows', () => {
   const originalExhibits = RegionStore.getRegionExhibits;
   const originalName = RegionStore.getRegionName;
   const originalSelected = RegionStore.isRegionFullySelected;
   const originalHide = RegionStore.shouldHideDuplicateSingleExhibit;
   const originalCreate = RegionRendererBuilder.createChoiceRow;

   RegionStore.getRegionExhibits = () => ['Savanna', 'Rainforest'];
   RegionStore.getRegionName = () => 'Africa';
   RegionStore.isRegionFullySelected = () => false;
   RegionStore.shouldHideDuplicateSingleExhibit = () => false;
   RegionRendererBuilder.createChoiceRow = (args) => args;

   try {
      const rows = RegionRenderer.buildRegionRows({}, new Set(['Savanna']));
      assert.equal(rows.length, 3);
      assert.equal(rows[0].action, 'toggle-region');
      assert.equal(rows[1].exhibitName, 'Savanna');
      assert.equal(rows[1].isSelected, true);
      assert.equal(rows[2].isSelected, false);
   } finally {
      RegionStore.getRegionExhibits = originalExhibits;
      RegionStore.getRegionName = originalName;
      RegionStore.isRegionFullySelected = originalSelected;
      RegionStore.shouldHideDuplicateSingleExhibit = originalHide;
      RegionRendererBuilder.createChoiceRow = originalCreate;
   }
});

test('Test_BuildRegionRows_TestHideDuplicate_ExpectRegionOnly', () => {
   const originalExhibits = RegionStore.getRegionExhibits;
   const originalName = RegionStore.getRegionName;
   const originalSelected = RegionStore.isRegionFullySelected;
   const originalHide = RegionStore.shouldHideDuplicateSingleExhibit;
   const originalCreate = RegionRendererBuilder.createChoiceRow;

   RegionStore.getRegionExhibits = () => ['Africa'];
   RegionStore.getRegionName = () => 'Africa';
   RegionStore.isRegionFullySelected = () => true;
   RegionStore.shouldHideDuplicateSingleExhibit = () => true;
   RegionRendererBuilder.createChoiceRow = (args) => args;

   try {
      const rows = RegionRenderer.buildRegionRows({}, new Set());
      assert.equal(rows.length, 1);
      assert.equal(rows[0].isSelected, true);
   } finally {
      RegionStore.getRegionExhibits = originalExhibits;
      RegionStore.getRegionName = originalName;
      RegionStore.isRegionFullySelected = originalSelected;
      RegionStore.shouldHideDuplicateSingleExhibit = originalHide;
      RegionRendererBuilder.createChoiceRow = originalCreate;
   }
});
