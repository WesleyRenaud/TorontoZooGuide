import assert from 'node:assert/strict';
import test from 'node:test';

import { ZooMapConstants } from '../../../scripts/shared/zooMapConstants.js';

test('Test_ZooMapConstants_TestMapMetrics_ExpectValues', () => {
   assert.equal(ZooMapConstants.ZOO_MAP_WIDTH_PX, 4096);
   assert.equal(ZooMapConstants.ZOO_MAP_HEIGHT_PX, 2665);
   assert.equal(ZooMapConstants.ZOO_MAP_VIEW_BOX, '0 0 4096 2665');
   assert.equal(ZooMapConstants.ENTRANCE_WALK_NODE_ID, 'v-0001');
});
