import assert from 'node:assert/strict';
import test from 'node:test';

import { AppConfig } from '../../../scripts/config/appConfig.js';
import { PanzoomAdapter } from '../../../scripts/map/panzoomAdapter.js';
import { PanzoomLabelPresenter } from '../../../scripts/map/panzoomLabelPresenter.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


function _installPanzoom() {
   const parent = document.createElement('div');
   const mapInner = document.createElement('div');
   parent.appendChild(mapInner);
   const originalGlobal = globalThis.Panzoom;
   globalThis.Panzoom = () => ({
      zoomWithWheel: () => {},
      getScale: () => 1,
   });

   return {
      mapInner,
      restore() {
         globalThis.Panzoom = originalGlobal;
      },
   };
}


test('Test_CreatePanzoom_TestContain_ExpectWiredPanzoom', () => {
   const parent = document.createElement('div');
   const mapInner = document.createElement('div');
   parent.appendChild(mapInner);
   const contain = AppConfig.DEFAULT_MAP_CONTAIN;
   const panzoom = {
      zoomWithWheel: () => {},
   };
   const originalGlobal = globalThis.Panzoom;
   const originalHandler = PanzoomLabelPresenter.createSvgLabelVisibilityHandler;
   const visibilityCalls = [];

   globalThis.Panzoom = (el, options) => {
      assert.equal(el, mapInner);
      assert.equal(options.minScale, 1);
      assert.equal(options.maxScale, 10);
      assert.equal(options.contain, contain);
      assert.equal(options.startX, Position.FIRST);
      assert.equal(options.startY, Position.FIRST);
      return panzoom;
   };
   PanzoomLabelPresenter.createSvgLabelVisibilityHandler = () => {
      const handler = () => { visibilityCalls.push(true); };
      return handler;
   };

   const result = PanzoomAdapter.createPanzoom(mapInner, { contain });

   assert.equal(result, panzoom);
   assert.equal(typeof parent.listeners.wheel, 'function');
   assert.equal(typeof mapInner.listeners.panzoomchange, 'function');
   assert.equal(visibilityCalls.length, Position.SECOND);
   globalThis.Panzoom = originalGlobal;
   PanzoomLabelPresenter.createSvgLabelVisibilityHandler = originalHandler;
});


test('Test_CreatePanzoom_TestRightPointerDown_ExpectStopped', () => {
   const { mapInner, restore } = _installPanzoom();

   PanzoomAdapter.createPanzoom(mapInner, { contain: AppConfig.DEFAULT_MAP_CONTAIN });
   let stopped = false;
   mapInner.listeners.pointerdown({
      button: 2,
      stopImmediatePropagation() {
         stopped = true;
      },
   });

   assert.equal(stopped, true);
   restore();
});


test('Test_CreatePanzoom_TestPrimaryPointerDown_ExpectContinues', () => {
   const { mapInner, restore } = _installPanzoom();

   PanzoomAdapter.createPanzoom(mapInner, { contain: AppConfig.DEFAULT_MAP_CONTAIN });
   let stopped = false;
   mapInner.listeners.pointerdown({
      button: 0,
      stopImmediatePropagation() {
         stopped = true;
      },
   });

   assert.equal(stopped, false);
   restore();
});


test('Test_CreatePanzoom_TestDragStart_ExpectPrevented', () => {
   const { mapInner, restore } = _installPanzoom();

   PanzoomAdapter.createPanzoom(mapInner, { contain: AppConfig.DEFAULT_MAP_CONTAIN });
   let prevented = false;
   mapInner.listeners.dragstart({
      preventDefault() {
         prevented = true;
      },
   });

   assert.equal(prevented, true);
   restore();
});
