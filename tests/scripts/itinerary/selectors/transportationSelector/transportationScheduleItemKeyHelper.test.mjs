import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationScheduleItemKeyHelper } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKeyHelper.js';


test('Test_AddedAsAttractionFromWire_TestOne_ExpectTrue', () => {
   const value = '1';

   const flag = TransportationScheduleItemKeyHelper.addedAsAttractionFromWire(value);

   assert.equal(flag, Boolean(Number(value)));
});


test('Test_AddedAsAttractionFromWire_TestZero_ExpectFalse', () => {
   const value = '0';

   const flag = TransportationScheduleItemKeyHelper.addedAsAttractionFromWire(value);

   assert.equal(flag, Boolean(Number(value)));
});


test('Test_AddedAsAttractionFromWire_TestBlank_ExpectNull', () => {
   const value = '  ';

   const flag = TransportationScheduleItemKeyHelper.addedAsAttractionFromWire(value);

   assert.equal(flag, null);
});


test('Test_AddedAsAttractionFromWire_TestYes_ExpectNull', () => {
   const value = 'yes';

   const flag = TransportationScheduleItemKeyHelper.addedAsAttractionFromWire(value);

   assert.equal(flag, null);
});
