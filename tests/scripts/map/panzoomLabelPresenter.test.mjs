import assert from 'node:assert/strict';
import test from 'node:test';

import { PanzoomLabelPresenter } from '../../../scripts/map/panzoomLabelPresenter.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_SetLabelVisibility_TestHide_ExpectDisplayNone', () => {
   const label = document.createElement('div');
   PanzoomLabelPresenter.setLabelVisibility([label], true);
   assert.equal(label.style.display, 'none');
   PanzoomLabelPresenter.setLabelVisibility([label], false);
   assert.equal(label.style.display, '');
});

test('Test_SyncSvgLabelVisibility_TestScale_ExpectHiddenAboveThreshold', () => {
   const mapInner = document.createElement('div');
   const primary = document.createElement('div');
   primary.className = 'map-label-primary-svg';
   mapInner.appendChild(primary);

   PanzoomLabelPresenter.syncSvgLabelVisibility(mapInner, 3);
   assert.equal(primary.style.display, 'none');

   PanzoomLabelPresenter.syncSvgLabelVisibility(mapInner, 1.5);
   assert.equal(primary.style.display, '');
});

test('Test_CreateSvgLabelVisibilityHandler_TestPanzoom_ExpectSynced', () => {
   const mapInner = document.createElement('div');
   const label = document.createElement('div');
   label.className = 'map-label-secondary-svg';
   mapInner.appendChild(label);
   const handler = PanzoomLabelPresenter.createSvgLabelVisibilityHandler(mapInner, {
      getScale: () => 3,
   });
   handler();
   assert.equal(label.style.display, 'none');
});
