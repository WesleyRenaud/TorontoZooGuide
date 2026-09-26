import assert from 'node:assert/strict';
import test from 'node:test';

import { AppConfig } from '../../../scripts/config/appConfig.js';
import { PanzoomAdapter } from '../../../scripts/map/panzoomAdapter.js';
import { PanzoomLabelPresenter } from '../../../scripts/map/panzoomLabelPresenter.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


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
      return panzoom;
   };
   PanzoomLabelPresenter.createSvgLabelVisibilityHandler = () => {
      const handler = () => { visibilityCalls.push(true); };
      return handler;
   };

   try {
      const result = PanzoomAdapter.createPanzoom(mapInner, { contain });

      assert.equal(result, panzoom);
      assert.equal(typeof parent.listeners.wheel, 'function');
      assert.equal(typeof mapInner.listeners.panzoomchange, 'function');
      assert.equal(visibilityCalls.length, Position.SECOND);
   } finally {
      globalThis.Panzoom = originalGlobal;
      PanzoomLabelPresenter.createSvgLabelVisibilityHandler = originalHandler;
   }
});
