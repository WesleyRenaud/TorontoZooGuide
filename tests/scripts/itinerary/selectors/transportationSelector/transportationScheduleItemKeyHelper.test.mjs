import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationScheduleItemKeyHelper } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKeyHelper.js';

test('Test_AddedAsAttractionFromWire_TestTokens_ExpectBooleanOrNull', () => {
   assert.equal(TransportationScheduleItemKeyHelper.addedAsAttractionFromWire('1'), true);
   assert.equal(TransportationScheduleItemKeyHelper.addedAsAttractionFromWire('0'), false);
   assert.equal(TransportationScheduleItemKeyHelper.addedAsAttractionFromWire('  '), null);
   assert.equal(TransportationScheduleItemKeyHelper.addedAsAttractionFromWire('yes'), null);
});
