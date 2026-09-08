import assert from 'node:assert/strict';
import test from 'node:test';

import { LayerRequestBuilder } from '../../../scripts/map/layerRequestBuilder.js';
import { TransportationSelectorModel } from '../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';

test('Test_UniqStrings_TestValues_ExpectUniqueTrimmed', () => {
   assert.deepEqual(LayerRequestBuilder.uniqStrings([' Lion ', 'Tiger', 'Lion', '', null]), [
      'Lion',
      'Tiger',
   ]);
});

test('Test_BuildFocusIncludes_TestFocusTypes_ExpectIncludes', () => {
   assert.deepEqual(LayerRequestBuilder.buildFocusIncludes('animal', { species: 'African Lion' }), {
      speciesToInclude: ['African Lion'],
      restaurantsToInclude: [],
      giftShopsToInclude: [],
      attractionsToInclude: [],
      transportationStationsToInclude: [],
   });
   assert.deepEqual(
      LayerRequestBuilder.buildFocusIncludes('restaurant', { name: 'Peaks Cafe' }).restaurantsToInclude,
      ['Peaks Cafe']
   );
   assert.deepEqual(
      LayerRequestBuilder.buildFocusIncludes('giftShop', { name: 'Zootique' }).giftShopsToInclude,
      ['Zootique']
   );
   assert.deepEqual(
      LayerRequestBuilder.buildFocusIncludes('attraction', { name: 'Carousel' }).attractionsToInclude,
      ['Carousel']
   );
   assert.deepEqual(
      LayerRequestBuilder.buildFocusIncludes('transportationStation', { name: 'Main Station' })
         .transportationStationsToInclude,
      ['Main Station']
   );
   assert.deepEqual(LayerRequestBuilder.buildFocusIncludes('animal', null).speciesToInclude, []);
});

test('Test_BuildFullyUnscheduledTransportationRows_TestMix_ExpectUnscheduledOnly', () => {
   const originalScheduled = TransportationSelectorModel.isTransportationScheduled;
   const originalName = TransportationSelectorModel.getTransportationName;
   TransportationSelectorModel.getTransportationName = (row) => row.name;
   TransportationSelectorModel.isTransportationScheduled = (row) => row.scheduled === true;

   try {
      const rows = LayerRequestBuilder.buildFullyUnscheduledTransportationRows(
         [
            { name: 'Zoomobile', scheduled: false },
            { name: 'Zoomobile', scheduled: false },
            { name: 'Shuttle', scheduled: true },
            { name: 'Boat', scheduled: false },
         ],
         [{ transportation: 'Boat' }]
      );

      assert.deepEqual(rows, [{ name: 'Zoomobile', scheduled: false, type: 'transportation' }]);
   } finally {
      TransportationSelectorModel.isTransportationScheduled = originalScheduled;
      TransportationSelectorModel.getTransportationName = originalName;
   }
});
