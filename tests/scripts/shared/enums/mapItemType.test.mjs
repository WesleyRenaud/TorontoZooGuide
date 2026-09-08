import assert from 'node:assert/strict';
import test from 'node:test';

import { MapItemType } from '../../../../scripts/shared/enums/mapItemType.js';

test('Test_MapItemType_TestConstants_ExpectValues', () => {
   assert.equal(MapItemType.TRANSPORTATION_STATION, 'transportationStation');
});
