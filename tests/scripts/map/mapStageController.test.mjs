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


function _withReferenceFrame(mapInner, run, { properties = {}, probe = null } = {}) {
   const originalGetComputedStyle = globalThis.getComputedStyle;
   const originalCreateElement = document.createElement.bind(document);

   document.documentElement = originalCreateElement('html');
   window.innerWidth = 1920;
   globalThis.getComputedStyle = () => ({
      getPropertyValue(property) {
         return properties[property] ?? '';
      },
   });

   if (probe) {
      document.createElement = (tagName) => {
         const node = originalCreateElement(tagName);

         node.getBoundingClientRect = () => probe;
         return node;
      };
   }

   try {
      return run();
   } finally {
      globalThis.getComputedStyle = originalGetComputedStyle;
      document.createElement = originalCreateElement;
      delete window.innerWidth;
      delete document.documentElement;
   }
}

installDomTestHooks();


test('Test_Fit_TestMissingInner_ExpectNull', () => {
   const fit = MapStageController.fit(null);

   assert.equal(fit, null);
});


test('Test_Fit_TestWideContainer_ExpectSlackOnHeight', () => {
   const fit = MapStageController.fit({
      clientWidth: WIDE_CONTAINER_WIDTH,
      clientHeight: WIDE_CONTAINER_HEIGHT,
   });
   const height = WIDE_CONTAINER_WIDTH / _contentAspect();

   assert.equal(fit.left, Position.FIRST);
   assert.equal(fit.width, WIDE_CONTAINER_WIDTH);
   assert.equal(fit.top, (WIDE_CONTAINER_HEIGHT - height) / 2);
   assert.equal(fit.height, height + MapStageController.COVER_SLACK_PX);
});


test('Test_Fit_TestFractionalFrame_ExpectBorderBox', () => {
   const mapInner = {
      clientWidth: 1420,
      clientHeight: 924,
      getBoundingClientRect: () => ({
         width: 1419.84375,
         height: 923.8046875,
      }),
   };
   const fit = MapStageController.fit(mapInner);

   assert.equal(fit.left, Position.FIRST);
   assert.equal(fit.top, Position.FIRST);
   assert.equal(fit.width, 1419.84375);
   assert.equal(fit.height, 923.8046875);
});


test('Test_ReferenceContainerSize_TestMissingInner_ExpectZero', () => {
   const size = MapStageController.referenceContainerSize(null);

   assert.equal(size.width, Position.FIRST);
   assert.equal(size.height, Position.FIRST);
});


test('Test_ReferenceContainerSize_TestMissingFrame_ExpectClientSize', () => {
   const mapInner = { clientWidth: 640, clientHeight: 480 };
   const size = _withReferenceFrame(mapInner, () => (
      MapStageController.referenceContainerSize(mapInner)
   ));

   assert.equal(size.width, mapInner.clientWidth);
   assert.equal(size.height, mapInner.clientHeight);
});


test('Test_ReferenceContainerSize_TestMeasuredFrame_ExpectViewportRemainder', () => {
   const mapInner = { clientWidth: 100, clientHeight: 80 };
   const size = _withReferenceFrame(mapInner, () => (
      MapStageController.referenceContainerSize(mapInner)
   ), {
      properties: {
         '--map-marker-panel-width': '405px',
         '--map-frame-height': '924px',
      },
      probe: {
         width: 405,
         height: 924,
         top: 0,
         left: 0,
         right: 405,
         bottom: 924,
      },
   });

   assert.equal(size.width, 1515);
   assert.equal(size.height, 924);
});


test('Test_ReferenceContainerSize_TestEmptyProbe_ExpectClientSize', () => {
   const mapInner = { clientWidth: 640, clientHeight: 480 };
   const size = _withReferenceFrame(mapInner, () => (
      MapStageController.referenceContainerSize(mapInner)
   ), {
      properties: {
         '--map-marker-panel-width': '405px',
         '--map-frame-height': '924px',
      },
   });

   assert.equal(size.width, mapInner.clientWidth);
   assert.equal(size.height, mapInner.clientHeight);
});


test('Test_MarkerLayerFrame_TestEmptyContainer_ExpectNull', () => {
   const frame = MapStageController.markerLayerFrame(Position.FIRST, Position.FIRST);

   assert.equal(frame, null);
});


test('Test_PlaceMarkerLayer_TestEmptyFrame_ExpectUnstyled', () => {
   const stage = document.createElement('div');
   const layer = document.createElement('div');

   layer.id = MapStageController.MARKER_LAYER_ID;
   stage.appendChild(layer);
   MapStageController.placeMarkerLayer(stage, {
      clientWidth: Position.FIRST,
      clientHeight: Position.FIRST,
   });

   assert.equal(layer.style.left, undefined);
});


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
      assert.equal(stage.style.height, `${height + MapStageController.COVER_SLACK_PX}px`);
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
      assert.equal(secondStage.style.width, `${width + MapStageController.COVER_SLACK_PX}px`);
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


test('Test_Mount_TestMarkerLayer_ExpectAnchoredToFirstFrame', () => {
   const originalObserver = globalThis.ResizeObserver;
   delete globalThis.ResizeObserver;
   const mapInner = _stageBox(document.createElement('div'));

   try {
      const stage = MapStageController.mount(mapInner);
      const layer = stage.querySelector(`#${MapStageController.MARKER_LAYER_ID}`);
      const rect = MapStageController.frameFor(mapInner);
      const stageWidth = rect.width + MapStageController.COVER_SLACK_PX;
      const stageHeight = rect.height + MapStageController.COVER_SLACK_PX;

      assert.equal(layer.style.left, `${(-rect.left / stageWidth) * 100}%`);
      assert.equal(layer.style.top, `${(-rect.top / stageHeight) * 100}%`);
      assert.equal(layer.style.width, `${(mapInner.clientWidth / stageWidth) * 100}%`);
      assert.equal(layer.style.height, `${(mapInner.clientHeight / stageHeight) * 100}%`);
   } finally {
      globalThis.ResizeObserver = originalObserver;
   }
});


test('Test_Apply_TestResize_ExpectMarkerLayerStays', () => {
   const stage = document.createElement('div');
   const layer = document.createElement('div');
   const mapInner = _stageBox({ clientWidth: 0, clientHeight: 0 });

   layer.id = MapStageController.MARKER_LAYER_ID;
   stage.appendChild(layer);
   MapStageController.apply(stage, mapInner);

   const anchored = {
      left: layer.style.left,
      top: layer.style.top,
      width: layer.style.width,
      height: layer.style.height,
   };
   const resized = MapStageController.coverRect(
      NARROW_CONTAINER_WIDTH,
      NARROW_CONTAINER_HEIGHT,
      ZooMapConstants.ZOO_MAP_WIDTH_PX,
      ZooMapConstants.ZOO_MAP_HEIGHT_PX
   );

   mapInner.clientWidth = NARROW_CONTAINER_WIDTH;
   mapInner.clientHeight = NARROW_CONTAINER_HEIGHT;
   MapStageController.apply(stage, mapInner);

   assert.equal(layer.style.left, anchored.left);
   assert.equal(layer.style.top, anchored.top);
   assert.equal(layer.style.width, anchored.width);
   assert.equal(layer.style.height, anchored.height);
   assert.equal(stage.style.width, `${resized.width + MapStageController.COVER_SLACK_PX}px`);
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
      assert.equal(frames.at(Position.FIRST).height, height + MapStageController.COVER_SLACK_PX);
      assert.equal(frames.at(Position.FIRST).top, (WIDE_CONTAINER_HEIGHT - height) / 2);
   } finally {
      globalThis.ResizeObserver = originalObserver;
   }
});
