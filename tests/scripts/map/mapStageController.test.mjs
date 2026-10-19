import assert from 'node:assert/strict';
import test from 'node:test';

import { MapStageController } from '../../../scripts/map/mapStageController.js';
import { ZooMapConstants } from '../../../scripts/shared/zooMapConstants.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

const WIDE_CONTAINER_WIDTH = 2000;
const WIDE_CONTAINER_HEIGHT = 800;
const NARROW_CONTAINER_WIDTH = 800;
const NARROW_CONTAINER_HEIGHT = 1200;


function _contentAspect() {
   return ZooMapConstants.ZOO_MAP_WIDTH_PX / ZooMapConstants.ZOO_MAP_HEIGHT_PX;
}


function _stageBox(mapInner) {
   mapInner.clientWidth = WIDE_CONTAINER_WIDTH;
   mapInner.clientHeight = WIDE_CONTAINER_HEIGHT;
   return mapInner;
}

installDomTestHooks();


test('Test_CoverRect_TestWiderContainer_ExpectVerticalOverflow', () => {
   const rect = MapStageController.coverRect(
      WIDE_CONTAINER_WIDTH,
      WIDE_CONTAINER_HEIGHT,
      ZooMapConstants.ZOO_MAP_WIDTH_PX,
      ZooMapConstants.ZOO_MAP_HEIGHT_PX
   );
   const height = WIDE_CONTAINER_WIDTH / _contentAspect();

   assert.equal(rect.left, Position.FIRST);
   assert.equal(rect.width, WIDE_CONTAINER_WIDTH);
   assert.equal(rect.height, height);
   assert.equal(rect.top, (WIDE_CONTAINER_HEIGHT - height) / 2);
});


test('Test_CoverRect_TestNarrowerContainer_ExpectHorizontalOverflow', () => {
   const rect = MapStageController.coverRect(
      NARROW_CONTAINER_WIDTH,
      NARROW_CONTAINER_HEIGHT,
      ZooMapConstants.ZOO_MAP_WIDTH_PX,
      ZooMapConstants.ZOO_MAP_HEIGHT_PX
   );
   const width = NARROW_CONTAINER_HEIGHT * _contentAspect();

   assert.equal(rect.top, Position.FIRST);
   assert.equal(rect.height, NARROW_CONTAINER_HEIGHT);
   assert.equal(rect.width, width);
   assert.equal(rect.left, (NARROW_CONTAINER_WIDTH - width) / 2);
});


test('Test_CoverRect_TestNonPositive_ExpectNull', () => {
   const rect = MapStageController.coverRect(
      Position.FIRST,
      WIDE_CONTAINER_HEIGHT,
      ZooMapConstants.ZOO_MAP_WIDTH_PX,
      ZooMapConstants.ZOO_MAP_HEIGHT_PX
   );

   assert.equal(rect, null);
});


test('Test_Apply_TestMissingStage_ExpectNoThrow', () => {
   const applied = MapStageController.apply(null, {
      clientWidth: WIDE_CONTAINER_WIDTH,
      clientHeight: WIDE_CONTAINER_HEIGHT,
   });

   assert.equal(applied, null);
});


test('Test_Apply_TestEmptyContainer_ExpectUnset', () => {
   const stage = document.createElement('div');

   MapStageController.apply(stage, {
      clientWidth: Position.FIRST,
      clientHeight: WIDE_CONTAINER_HEIGHT,
   });

   assert.equal(stage.style.width, undefined);
});


test('Test_FindStage_TestNoQuery_ExpectNull', () => {
   const stage = MapStageController.findStage({});

   assert.equal(stage, null);
});


test('Test_Mount_TestMissingMap_ExpectNull', () => {
   const stage = MapStageController.mount(null);

   assert.equal(stage, null);
});


test('Test_Mount_TestPrepend_ExpectCoverSizedStage', () => {
   const originalObserver = globalThis.ResizeObserver;
   const observed = [];
   globalThis.ResizeObserver = class ResizeObserver {
      constructor(callback) {
         this.callback = callback;
      }

      observe(target) {
         observed.push(target);
         this.callback();
      }
   };
   const mapInner = _stageBox(document.createElement('div'));
   const zooMapMount = document.createElement('div');
   zooMapMount.id = 'zooMapMount';
   mapInner.appendChild(zooMapMount);
   mapInner.prepend = (stage) => {
      stage.parentElement = mapInner;
      mapInner.children.unshift(stage);
   };

   try {
      const stage = MapStageController.mount(mapInner);
      const height = WIDE_CONTAINER_WIDTH / _contentAspect();

      assert.equal(stage.id, MapStageController.STAGE_ID);
      assert.equal(mapInner.children.at(Position.FIRST), stage);
      assert.equal(zooMapMount.parentElement, stage);
      assert.equal(stage.style.width, `${WIDE_CONTAINER_WIDTH}px`);
      assert.equal(stage.style.height, `${height}px`);
      assert.equal(stage.style.left, `${Position.FIRST}px`);
      assert.equal(stage.style.top, `${Position.FIRST}px`);
      assert.equal(observed.at(Position.FIRST), mapInner);
      assert.equal(observed.length, Position.SECOND);
   } finally {
      globalThis.ResizeObserver = originalObserver;
   }
});


test('Test_Mount_TestExistingStage_ExpectReuse', () => {
   const originalObserver = globalThis.ResizeObserver;
   globalThis.ResizeObserver = class ResizeObserver {
      observe() {}
   };
   const mapInner = _stageBox(document.createElement('div'));
   mapInner.prepend = (stage) => {
      stage.parentElement = mapInner;
      mapInner.children.unshift(stage);
   };

   try {
      const firstStage = MapStageController.mount(mapInner);
      mapInner.clientWidth = NARROW_CONTAINER_WIDTH;
      mapInner.clientHeight = NARROW_CONTAINER_HEIGHT;
      const secondStage = MapStageController.mount(mapInner);
      const width = NARROW_CONTAINER_HEIGHT * _contentAspect();

      assert.equal(secondStage, firstStage);
      assert.equal(secondStage.style.height, `${NARROW_CONTAINER_HEIGHT}px`);
      assert.equal(secondStage.style.top, `${Position.FIRST}px`);
      assert.equal(secondStage.style.left, `${Position.FIRST}px`);
      assert.equal(secondStage.style.width, `${width}px`);
   } finally {
      globalThis.ResizeObserver = originalObserver;
   }
});


test('Test_Mount_TestWithoutPrepend_ExpectAppended', () => {
   const originalObserver = globalThis.ResizeObserver;
   delete globalThis.ResizeObserver;
   const mapInner = _stageBox(document.createElement('div'));

   try {
      const stage = MapStageController.mount(mapInner);

      assert.equal(mapInner.children.at(Position.LAST), stage);
      assert.equal(stage.style.width, `${WIDE_CONTAINER_WIDTH}px`);
   } finally {
      globalThis.ResizeObserver = originalObserver;
   }
});


test('Test_Apply_TestNoMarkerLayer_ExpectStageSize', () => {
   const stage = document.createElement('div');
   const mapInner = {
      clientWidth: WIDE_CONTAINER_WIDTH,
      clientHeight: WIDE_CONTAINER_HEIGHT,
   };

   const rect = MapStageController.apply(stage, mapInner);

   assert.equal(rect.width, WIDE_CONTAINER_WIDTH);
   assert.equal(stage.querySelector(`#${MapStageController.MARKER_LAYER_ID}`), null);
});


test('Test_Apply_TestMissingContainer_ExpectUnset', () => {
   const stage = document.createElement('div');

   MapStageController.apply(stage, null);

   assert.equal(stage.style.width, undefined);
});


test('Test_SyncPan_TestScaleOne_ExpectCentered', () => {
   const pans = [];
   const rect = { left: -40, top: 0 };

   MapStageController.syncPan({
      getScale: () => 1,
      pan: (x, y, options) => {
         pans.push({ x, y, options });
      },
   }, rect);

   assert.equal(pans.at(Position.FIRST).x, rect.left);
   assert.equal(pans.at(Position.FIRST).y, rect.top);
   assert.equal(pans.at(Position.FIRST).options.animate, false);
});


test('Test_SyncPan_TestZoomed_ExpectCurrentPan', () => {
   const pans = [];
   const currentPan = { x: 5, y: -8 };

   MapStageController.syncPan({
      getScale: () => 2,
      getPan: () => currentPan,
      pan: (x, y) => {
         pans.push({ x, y });
      },
   }, { left: -40, top: 0 });

   assert.equal(pans.at(Position.FIRST).x, currentPan.x);
   assert.equal(pans.at(Position.FIRST).y, currentPan.y);
});


test('Test_Mount_TestMarkerLayer_ExpectVisiblePanel', () => {
   const originalObserver = globalThis.ResizeObserver;
   delete globalThis.ResizeObserver;
   const mapInner = _stageBox(document.createElement('div'));

   try {
      const stage = MapStageController.mount(mapInner);
      const layer = stage.querySelector(`#${MapStageController.MARKER_LAYER_ID}`);
      const rect = MapStageController.frameFor(mapInner);

      assert.equal(layer.style.left, `${-rect.left}px`);
      assert.equal(layer.style.top, `${-rect.top}px`);
      assert.equal(layer.style.width, `${WIDE_CONTAINER_WIDTH}px`);
      assert.equal(layer.style.height, `${WIDE_CONTAINER_HEIGHT}px`);
   } finally {
      globalThis.ResizeObserver = originalObserver;
   }
});


test('Test_Mount_TestOnFrame_ExpectRect', () => {
   const originalObserver = globalThis.ResizeObserver;
   const frames = [];
   globalThis.ResizeObserver = class ResizeObserver {
      constructor(callback) {
         this.callback = callback;
      }

      observe() {
         this.callback();
      }
   };
   const mapInner = _stageBox(document.createElement('div'));
   mapInner.prepend = (stage) => {
      stage.parentElement = mapInner;
      mapInner.children.unshift(stage);
   };

   try {
      MapStageController.mount(mapInner, (rect) => {
         frames.push(rect);
      });
      const height = WIDE_CONTAINER_WIDTH / _contentAspect();

      assert.equal(frames.at(Position.FIRST).width, WIDE_CONTAINER_WIDTH);
      assert.equal(frames.at(Position.FIRST).height, height);
      assert.equal(frames.at(Position.FIRST).top, (WIDE_CONTAINER_HEIGHT - height) / 2);
   } finally {
      globalThis.ResizeObserver = originalObserver;
   }
});
