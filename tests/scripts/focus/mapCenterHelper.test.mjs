import assert from 'node:assert/strict';
import test from 'node:test';

import { MapCenterHelper } from '../../../scripts/focus/mapCenterHelper.js';

test('Test_CenterMarkerWithContain_TestPanzoom_ExpectPannedAndRestored', () => {
   const pans = [];
   const contains = [];
   const panzoom = {
      options: { contain: 'outside' },
      getScale: () => 2,
      getPan: () => ({ x: 0, y: 0 }),
      setOptions({ contain }) { contains.push(contain); this.options.contain = contain; },
      pan(x, y, options) { pans.push({ x, y, options }); },
   };
   const markerEl = {
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 10, height: 10 }),
   };
   const viewportEl = {
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 100, height: 100 }),
   };

   MapCenterHelper.centerMarkerWithContain(panzoom, markerEl, viewportEl);

   assert.ok(pans.length >= 2);
   assert.equal(panzoom.options.contain, 'outside');
   assert.ok(contains.includes('none'));
});

test('Test_CenterMarkerWithContain_TestMissingArgs_ExpectNoThrow', () => {
   assert.doesNotThrow(() => MapCenterHelper.centerMarkerWithContain(null, null, null));
});
