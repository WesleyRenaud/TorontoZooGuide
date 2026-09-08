import assert from 'node:assert/strict';
import test from 'node:test';

import { ClosedExhibitOverlayHelper } from '../../../scripts/map/closedExhibitOverlayHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_GetClosedExhibitOverlayId_TestKey_ExpectPrefixedId', () => {
   assert.equal(
      ClosedExhibitOverlayHelper.getClosedExhibitOverlayId('african-rainforest'),
      'closed-exhibit-overlay-african-rainforest'
   );
});

test('Test_NormalizeClosedExhibitKeys_TestValues_ExpectNormalized', () => {
   assert.deepEqual(
      ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys(['African Rainforest', '', null]),
      ['african-rainforest']
   );
   assert.deepEqual(ClosedExhibitOverlayHelper.normalizeClosedExhibitKeys(null), []);
});

test('Test_HideAndShowClosedExhibitOverlays_TestDisplay_ExpectToggled', () => {
   const overlay = document.createElement('div');
   overlay.id = ClosedExhibitOverlayHelper.getClosedExhibitOverlayId('malayan-woods');
   overlay.style.display = '';

   const overlaysById = new Map([[overlay.id, overlay]]);
   const originalGet = document.getElementById;
   const originalQueryAll = document.querySelectorAll;

   document.getElementById = (id) => overlaysById.get(id) ?? null;
   document.querySelectorAll = (selector) => (
      selector === ClosedExhibitOverlayHelper.CLOSED_EXHIBIT_OVERLAY_SELECTOR
         ? [overlay]
         : []
   );

   try {
      const found = ClosedExhibitOverlayHelper.getClosedExhibitOverlays();
      ClosedExhibitOverlayHelper.hideClosedExhibitOverlays(found);
      assert.equal(overlay.style.display, 'none');

      ClosedExhibitOverlayHelper.showClosedExhibitOverlay('malayan-woods');
      assert.equal(overlay.style.display, '');

      ClosedExhibitOverlayHelper.showClosedExhibitOverlay('missing');
   } finally {
      document.getElementById = originalGet;
      document.querySelectorAll = originalQueryAll;
   }
});
