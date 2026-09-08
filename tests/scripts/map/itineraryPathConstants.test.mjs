import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPathConstants } from '../../../scripts/map/itineraryPathConstants.js';

test('Test_ItineraryPathConstants_TestArrowMetrics_ExpectPositive', () => {
   assert.equal(ItineraryPathConstants.ITINERARY_PATH_ARROW_INTERVAL_PX, 60);
   assert.equal(ItineraryPathConstants.ITINERARY_PATH_ARROW_SKIP_END_PX, 20);
   assert.equal(ItineraryPathConstants.ITINERARY_PATH_ARROW_MIN_PATH_LENGTH_PX, 36);
   assert.equal(ItineraryPathConstants.ITINERARY_PATH_ARROW_CURVE_SAMPLE_STEP_PX, 8);
   assert.equal(ItineraryPathConstants.ITINERARY_PATH_ARROW_SIDE_OFFSET_PX, 3);
});
