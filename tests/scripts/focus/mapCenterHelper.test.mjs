import assert from 'node:assert/strict';
import test from 'node:test';

import { MapCenterHelper } from '../../../scripts/focus/mapCenterHelper.js';
import { AppConfig } from '../../../scripts/config/appConfig.js';


test('Test_CenterMarkerWithContain_TestPanzoom_ExpectPannedAndRestored', () => {
   const pans = [];
   const contains = [];
   const contain = AppConfig.DEFAULT_MAP_CONTAIN;
   const panzoom = {
      options: { contain },
      getScale: () => 2,
      getPan: () => ({ x: 0, y: 0 }),
      setOptions({ contain: next }) { contains.push(next); this.options.contain = next; },
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
   assert.equal(panzoom.options.contain, contain);
   assert.ok(contains.includes('none'));
});


test('Test_CenterMarkerWithContain_TestMissingArgs_ExpectNoThrow', () => {
   const panzoom = null;
   const markerEl = null;
   const viewportEl = null;

   const center = () => MapCenterHelper.centerMarkerWithContain(panzoom, markerEl, viewportEl);

   assert.doesNotThrow(center);
});
