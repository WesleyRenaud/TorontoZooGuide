import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionRenderer } from '../../../../../scripts/itinerary/selectors/regionSelector/regionRenderer.js';
import { RegionStore } from '../../../../../scripts/itinerary/selectors/regionSelector/regionStore.js';
import { RegionRendererBuilder } from '../../../../../scripts/itinerary/selectors/regionSelector/regionRendererBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_BuildRegionRows_TestExhibits_ExpectRegionAndExhibitRows', () => {
   const originalExhibits = RegionStore.getRegionExhibits;
   const originalName = RegionStore.getRegionName;
   const originalSelected = RegionStore.isRegionFullySelected;
   const originalHide = RegionStore.shouldHideDuplicateSingleExhibit;
   const originalCreate = RegionRendererBuilder.createChoiceRow;
   const savanna = 'Savanna';
   const rainforest = 'Rainforest';
   const exhibits = [savanna, rainforest];
   const regionName = 'Africa';
   const selectedExhibits = new Set([savanna]);
   RegionStore.getRegionExhibits = () => exhibits;
   RegionStore.getRegionName = () => regionName;
   RegionStore.isRegionFullySelected = () => false;
   RegionStore.shouldHideDuplicateSingleExhibit = () => false;
   RegionRendererBuilder.createChoiceRow = (args) => args;

   try {
      const rows = RegionRenderer.buildRegionRows({}, selectedExhibits);

      assert.equal(rows.length, exhibits.length + 1);
      assert.equal(rows.at(Position.FIRST).action, 'toggle-region');
      assert.equal(rows.at(Position.SECOND).exhibitName, savanna);
      assert.equal(rows.at(Position.SECOND).isSelected, selectedExhibits.has(savanna));
      assert.equal(rows.at(Position.THIRD).isSelected, selectedExhibits.has(rainforest));
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
   const regionName = 'Africa';
   RegionStore.getRegionExhibits = () => [regionName];
   RegionStore.getRegionName = () => regionName;
   RegionStore.isRegionFullySelected = () => true;
   RegionStore.shouldHideDuplicateSingleExhibit = () => true;
   RegionRendererBuilder.createChoiceRow = (args) => args;

   try {
      const rows = RegionRenderer.buildRegionRows({}, new Set());

      assert.equal(rows.length, 1);
      assert.equal(rows.at(Position.FIRST).isSelected, true);
   } finally {
      RegionStore.getRegionExhibits = originalExhibits;
      RegionStore.getRegionName = originalName;
      RegionStore.isRegionFullySelected = originalSelected;
      RegionStore.shouldHideDuplicateSingleExhibit = originalHide;
      RegionRendererBuilder.createChoiceRow = originalCreate;
   }
});
