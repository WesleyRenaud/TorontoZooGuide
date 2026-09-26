import assert from 'node:assert/strict';
import test from 'node:test';

import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';
import { ClosedExhibitOverlayHelper } from '../../../scripts/map/closedExhibitOverlayHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_GetClosedExhibitOverlayId_TestKey_ExpectPrefixedId', () => {
   const exhibitKey = 'african-rainforest';

   const overlayId = ClosedExhibitOverlayHelper.getClosedExhibitOverlayId(exhibitKey);

   assert.equal(
      overlayId,
      `${ClosedExhibitOverlayHelper.CLOSED_EXHIBIT_OVERLAY_ID_PREFIX}${exhibitKey}`
   );
});


test('Test_NormalizeClosedExhibitKeys_TestValues_ExpectNormalized', () => {
   const exhibit = 'African Rainforest';
   const values = [exhibit, '', null];

   const keys = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys(values);

   assert.deepEqual(keys, [AssetKeyNormalizer.normalize(exhibit)]);
});


test('Test_NormalizeClosedExhibitKeys_TestNull_ExpectEmpty', () => {
   const values = null;

   const keys = ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys(values);

   assert.deepEqual(keys, []);
});


test('Test_HideClosedExhibitOverlays_TestDisplay_ExpectHidden', () => {
   const exhibitKey = 'malayan-woods';
   const overlay = document.createElement('div');
   overlay.id = ClosedExhibitOverlayHelper.getClosedExhibitOverlayId(exhibitKey);
   overlay.style.display = '';
   const originalQueryAll = document.querySelectorAll;
   document.querySelectorAll = (selector) => (
      selector === ClosedExhibitOverlayHelper.CLOSED_EXHIBIT_OVERLAY_SELECTOR
         ? [overlay]
         : []
   );

   try {
      const found = ClosedExhibitOverlayHelper.getClosedExhibitOverlays();

      ClosedExhibitOverlayHelper.hideClosedExhibitOverlays(found);

      assert.equal(overlay.style.display, 'none');
   } finally {
      document.querySelectorAll = originalQueryAll;
   }
});


test('Test_ShowClosedExhibitOverlay_TestKnown_ExpectVisible', () => {
   const exhibitKey = 'malayan-woods';
   const overlay = document.createElement('div');
   overlay.id = ClosedExhibitOverlayHelper.getClosedExhibitOverlayId(exhibitKey);
   overlay.style.display = 'none';
   const overlaysById = new Map([[overlay.id, overlay]]);
   const originalGet = document.getElementById;
   document.getElementById = (id) => overlaysById.get(id) ?? null;

   try {
      ClosedExhibitOverlayHelper.showClosedExhibitOverlay(exhibitKey);

      assert.equal(overlay.style.display, '');
   } finally {
      document.getElementById = originalGet;
   }
});


test('Test_ShowClosedExhibitOverlay_TestMissing_ExpectNoThrow', () => {
   const originalGet = document.getElementById;
   document.getElementById = () => null;

   try {
      const show = () => ClosedExhibitOverlayHelper.showClosedExhibitOverlay('missing');

      assert.doesNotThrow(show);
   } finally {
      document.getElementById = originalGet;
   }
});
