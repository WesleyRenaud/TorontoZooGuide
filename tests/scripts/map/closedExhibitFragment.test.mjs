import assert from 'node:assert/strict';
import test from 'node:test';

import { ClosedExhibitFragment } from '../../../scripts/map/closedExhibitFragment.js';
import { ClosedExhibitOverlayHelper } from '../../../scripts/map/closedExhibitOverlayHelper.js';

test('Test_SetClosedExhibitOverlaysVisible_TestKeys_ExpectHideAndShow', () => {
   const calls = [];
   const originalGet = ClosedExhibitOverlayHelper.getClosedExhibitOverlays;
   const originalNormalize = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys;
   const originalHide = ClosedExhibitOverlayHelper.hideClosedExhibitOverlays;
   const originalShow = ClosedExhibitOverlayHelper.showClosedExhibitOverlay;

   ClosedExhibitOverlayHelper.getClosedExhibitOverlays = () => ['overlay'];
   ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = (values) => values;
   ClosedExhibitOverlayHelper.hideClosedExhibitOverlays = (overlays) => {
      calls.push(['hide', overlays]);
   };
   ClosedExhibitOverlayHelper.showClosedExhibitOverlay = (key) => {
      calls.push(['show', key]);
   };

   try {
      ClosedExhibitFragment.setClosedExhibitOverlaysVisible(['african-rainforest', 'malayan-woods']);
      assert.deepEqual(calls, [
         ['hide', ['overlay']],
         ['show', 'african-rainforest'],
         ['show', 'malayan-woods'],
      ]);
   } finally {
      ClosedExhibitOverlayHelper.getClosedExhibitOverlays = originalGet;
      ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = originalNormalize;
      ClosedExhibitOverlayHelper.hideClosedExhibitOverlays = originalHide;
      ClosedExhibitOverlayHelper.showClosedExhibitOverlay = originalShow;
   }
});

test('Test_SyncClosedExhibitOverlays_TestFetchPaths_ExpectKeysOrEmpty', async () => {
   const visible = [];
   const originalSet = ClosedExhibitFragment.setClosedExhibitOverlaysVisible;
   const originalNormalize = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys;
   ClosedExhibitFragment.setClosedExhibitOverlaysVisible = (keys) => { visible.push(keys); };
   ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = (rows) => rows;

   try {
      assert.deepEqual(await ClosedExhibitFragment.syncClosedExhibitOverlays({}, {}), []);
      assert.deepEqual(visible.at(-1), []);

      assert.deepEqual(
         await ClosedExhibitFragment.syncClosedExhibitOverlays({
            closedExhibit: {
               fetch: async () => ['african-rainforest'],
            },
         }, { day: 1 }),
         ['african-rainforest']
      );

      assert.deepEqual(
         await ClosedExhibitFragment.syncClosedExhibitOverlays({
            closedExhibit: {
               fetch: async () => { throw new Error('fail'); },
            },
         }, {}),
         []
      );
   } finally {
      ClosedExhibitFragment.setClosedExhibitOverlaysVisible = originalSet;
      ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = originalNormalize;
   }
});
