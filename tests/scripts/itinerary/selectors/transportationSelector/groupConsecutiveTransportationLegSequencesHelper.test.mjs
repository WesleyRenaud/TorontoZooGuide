import assert from 'node:assert/strict';
import test from 'node:test';

import { GroupConsecutiveTransportationLegSequencesHelper } from '../../../../../scripts/itinerary/selectors/transportationSelector/groupConsecutiveTransportationLegSequencesHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_NormalizeLegs_TestNull_ExpectEmpty', () => {
   const value = null;

   const legs = GroupConsecutiveTransportationLegSequencesHelper.normalizeLegs(value);

   assert.deepEqual(legs, []);
});


test('Test_NormalizeLegs_TestMixedValues_ExpectObjectLegs', () => {
   const from = 'a';
   const to = 'b';
   const values = [
      { from, to },
      null,
   ];

   const legs = GroupConsecutiveTransportationLegSequencesHelper.normalizeLegs(values);

   assert.equal(legs.at(Position.FIRST).from, from);
   assert.equal(legs.at(Position.FIRST).to, to);
   assert.deepEqual(legs.at(Position.SECOND), {});
});
