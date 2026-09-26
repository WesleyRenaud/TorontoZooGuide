import assert from 'node:assert/strict';
import test from 'node:test';

import { LayerRequestBuilder } from '../../../scripts/map/layerRequestBuilder.js';
import { TransportationSelectorModel } from '../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';

const africanLion = 'African Lion';
const peaksCafe = 'Peaks Cafe';
const zootique = 'Zootique';
const carousel = 'Carousel';
const mainStation = 'Main Station';


test('Test_UniqStrings_TestValues_ExpectUniqueTrimmed', () => {
   const lion = 'Lion';
   const tiger = 'Tiger';

   const unique = LayerRequestBuilder.uniqStrings([` ${lion} `, tiger, lion, '', null]);

   assert.deepEqual(unique, [lion, tiger]);
});


test('Test_BuildFocusIncludes_TestAnimal_ExpectSpecies', () => {
   const includes = LayerRequestBuilder.buildFocusIncludes(ItemType.ANIMAL, { species: africanLion });

   assert.deepEqual(includes, {
      speciesToInclude: [africanLion],
      restaurantsToInclude: [],
      giftShopsToInclude: [],
      attractionsToInclude: [],
      transportationStationsToInclude: [],
   });
});


test('Test_BuildFocusIncludes_TestRestaurant_ExpectName', () => {
   const includes = LayerRequestBuilder.buildFocusIncludes(ItemType.RESTAURANT, { name: peaksCafe });

   assert.deepEqual(includes.restaurantsToInclude, [peaksCafe]);
});


test('Test_BuildFocusIncludes_TestGiftShop_ExpectName', () => {
   const includes = LayerRequestBuilder.buildFocusIncludes(ItemType.GIFT_SHOP, { name: zootique });

   assert.deepEqual(includes.giftShopsToInclude, [zootique]);
});


test('Test_BuildFocusIncludes_TestAttraction_ExpectName', () => {
   const includes = LayerRequestBuilder.buildFocusIncludes(ItemType.ATTRACTION, { name: carousel });

   assert.deepEqual(includes.attractionsToInclude, [carousel]);
});


test('Test_BuildFocusIncludes_TestTransportationStation_ExpectName', () => {
   const includes = LayerRequestBuilder.buildFocusIncludes(
      ItemType.TRANSPORTATION_STATION,
      { name: mainStation }
   );

   assert.deepEqual(includes.transportationStationsToInclude, [mainStation]);
});


test('Test_BuildFocusIncludes_TestMissingRow_ExpectEmptySpecies', () => {
   const includes = LayerRequestBuilder.buildFocusIncludes(ItemType.ANIMAL, null);

   assert.deepEqual(includes.speciesToInclude, []);
});


test('Test_IsFullyUnscheduledTransportationName_TestMissingName_ExpectFalse', () => {
   const originalName = TransportationSelectorModel.getTransportationName;
   TransportationSelectorModel.getTransportationName = (row) => row.name;
   const missingName = 'Missing';

   try {
      const isUnscheduled = LayerRequestBuilder.isFullyUnscheduledTransportationName(
         missingName,
         [{ name: 'Zoomobile' }],
         new Set()
      );

      assert.equal(isUnscheduled, false);
   } finally {
      TransportationSelectorModel.getTransportationName = originalName;
   }
});


test('Test_IsFullyUnscheduledTransportationName_TestEmptyRows_ExpectFalse', () => {
   const originalName = TransportationSelectorModel.getTransportationName;
   TransportationSelectorModel.getTransportationName = (row) => row.name;
   const missingName = 'Missing';

   try {
      const isUnscheduled = LayerRequestBuilder.isFullyUnscheduledTransportationName(
         missingName,
         [],
         new Set()
      );

      assert.equal(isUnscheduled, false);
   } finally {
      TransportationSelectorModel.getTransportationName = originalName;
   }
});


test('Test_BuildFullyUnscheduledTransportationRows_TestMix_ExpectUnscheduledOnly', () => {
   const originalScheduled = TransportationSelectorModel.isTransportationScheduled;
   const originalName = TransportationSelectorModel.getTransportationName;
   TransportationSelectorModel.getTransportationName = (row) => row.name;
   TransportationSelectorModel.isTransportationScheduled = (row) => row.scheduled === true;
   const zoomobile = { name: 'Zoomobile', scheduled: false };
   const shuttle = { name: 'Shuttle', scheduled: true };
   const boat = { name: 'Boat', scheduled: false };

   try {
      const rows = LayerRequestBuilder.buildFullyUnscheduledTransportationRows(
         [zoomobile, zoomobile, shuttle, boat],
         [{ transportation: boat.name }]
      );

      assert.deepEqual(rows, [{ ...zoomobile, type: ItemType.TRANSPORTATION }]);
   } finally {
      TransportationSelectorModel.isTransportationScheduled = originalScheduled;
      TransportationSelectorModel.getTransportationName = originalName;
   }
});
