import assert from 'node:assert/strict';
import test from 'node:test';

import { ClosedExhibitFragment } from '../../../scripts/map/closedExhibitFragment.js';
import { ClosedExhibitOverlayHelper } from '../../../scripts/map/closedExhibitOverlayHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';

const africanRainforest = 'african-rainforest';
const malayanWoods = 'malayan-woods';


test('Test_SetClosedExhibitOverlaysVisible_TestKeys_ExpectHideAndShow', () => {
   const calls = [];
   const overlays = ['overlay'];
   const originalGet = ClosedExhibitOverlayHelper.getClosedExhibitOverlays;
   const originalNormalize = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys;
   const originalHide = ClosedExhibitOverlayHelper.hideClosedExhibitOverlays;
   const originalShow = ClosedExhibitOverlayHelper.showClosedExhibitOverlay;

   ClosedExhibitOverlayHelper.getClosedExhibitOverlays = () => overlays;
   ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = (values) => values;
   ClosedExhibitOverlayHelper.hideClosedExhibitOverlays = (hiddenOverlays) => {
      calls.push(['hide', hiddenOverlays]);
   };
   ClosedExhibitOverlayHelper.showClosedExhibitOverlay = (key) => {
      calls.push(['show', key]);
   };

   try {
      ClosedExhibitFragment.setClosedExhibitOverlaysVisible([africanRainforest, malayanWoods]);

      assert.deepEqual(calls, [
         ['hide', overlays],
         ['show', africanRainforest],
         ['show', malayanWoods],
      ]);
   } finally {
      ClosedExhibitOverlayHelper.getClosedExhibitOverlays = originalGet;
      ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = originalNormalize;
      ClosedExhibitOverlayHelper.hideClosedExhibitOverlays = originalHide;
      ClosedExhibitOverlayHelper.showClosedExhibitOverlay = originalShow;
   }
});


test('Test_SyncClosedExhibitOverlays_TestMissingFetch_ExpectEmpty', async () => {
   const visible = [];
   const originalSet = ClosedExhibitFragment.setClosedExhibitOverlaysVisible;
   const originalNormalize = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys;
   ClosedExhibitFragment.setClosedExhibitOverlaysVisible = (keys) => {
      visible.push(keys);
   };
   ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = (rows) => rows;

   try {
      const keys = await ClosedExhibitFragment.syncClosedExhibitOverlays({}, {});

      assert.deepEqual(keys, []);
      assert.deepEqual(visible.at(Position.LAST), []);
   } finally {
      ClosedExhibitFragment.setClosedExhibitOverlaysVisible = originalSet;
      ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = originalNormalize;
   }
});


test('Test_SyncClosedExhibitOverlays_TestFetchKeys_ExpectReturned', async () => {
   const visible = [];
   const closedKeys = [africanRainforest];
   const originalSet = ClosedExhibitFragment.setClosedExhibitOverlaysVisible;
   const originalNormalize = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys;
   ClosedExhibitFragment.setClosedExhibitOverlaysVisible = (keys) => {
      visible.push(keys);
   };
   ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = (rows) => rows;

   try {
      const keys = await ClosedExhibitFragment.syncClosedExhibitOverlays({
         closedExhibit: {
            fetch: async () => closedKeys,
         },
      }, { day: 1 });

      assert.deepEqual(keys, closedKeys);
   } finally {
      ClosedExhibitFragment.setClosedExhibitOverlaysVisible = originalSet;
      ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = originalNormalize;
   }
});


test('Test_SyncClosedExhibitOverlays_TestFetchFailure_ExpectEmpty', async () => {
   const originalSet = ClosedExhibitFragment.setClosedExhibitOverlaysVisible;
   const originalNormalize = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys;
   ClosedExhibitFragment.setClosedExhibitOverlaysVisible = () => {};
   ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = (rows) => rows;

   try {
      const keys = await ClosedExhibitFragment.syncClosedExhibitOverlays({
         closedExhibit: {
            fetch: async () => {
               throw new Error('fail');
            },
         },
      }, {});

      assert.deepEqual(keys, []);
   } finally {
      ClosedExhibitFragment.setClosedExhibitOverlaysVisible = originalSet;
      ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys = originalNormalize;
   }
});
