import assert from 'node:assert/strict';
import test from 'node:test';

import { ZooMapConstants } from '../../../scripts/shared/zooMapConstants.js';


test('Test_ZooMapConstants_TestViewBox_ExpectWidthAndHeight', () => {
   const viewBox = ZooMapConstants.ZOO_MAP_VIEW_BOX;

   assert.equal(
      viewBox,
      `0 0 ${ZooMapConstants.ZOO_MAP_WIDTH_PX} ${ZooMapConstants.ZOO_MAP_HEIGHT_PX}`
   );
});
