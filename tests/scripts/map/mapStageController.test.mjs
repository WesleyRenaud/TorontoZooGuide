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

   assert.equal(applied, undefined);
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


test('Test_Apply_TestMissingContainer_ExpectUnset', () => {
   const stage = document.createElement('div');

   MapStageController.apply(stage, null);

   assert.equal(stage.style.width, undefined);
});
