import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerHelper } from '../../../scripts/markers/markerHelper.js';
import { BannerSynchronizer } from '../../../scripts/tooltips/bannerSynchronizer.js';
import { CarouselView } from '../../../scripts/tooltips/carouselView.js';
import { GlobalListener } from '../../../scripts/tooltips/globalListener.js';
import { PositionFragment } from '../../../scripts/tooltips/positionFragment.js';
import { TooltipController } from '../../../scripts/tooltips/tooltipController.js';
import { TooltipRenderer } from '../../../scripts/tooltips/tooltipRenderer.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


function _stubTooltipDeps({ renderResult = true } = {}) {
   const bannerSyncs = [];
   const bannerHides = [];
   const carouselCalls = [];
   const listenerCalls = [];
   const positions = [];
   const visualCalls = [];
   const animalIconCalls = [];
   let onIndexChange = null;
   let stepFn = null;
   let closeFn = null;
   let isOpenFn = null;
   let getItemAtIndex = null;

   const originals = {
      banners: BannerSynchronizer.createTooltipBannerSync,
      carousel: CarouselView.createTooltipCarouselView,
      listeners: GlobalListener.createTooltipGlobalListeners,
      position: PositionFragment.positionTooltip,
      applyVisual: MarkerHelper.applyMarkerVisual,
      setAnimal: MarkerHelper.setMarkerToAnimalIcon,
      getRenderer: TooltipRenderer.getRendererForItem,
   };

   BannerSynchronizer.createTooltipBannerSync = () => ({
      sync: (item) => bannerSyncs.push(item),
      hideAll: () => bannerHides.push(true),
   });

   CarouselView.createTooltipCarouselView = (options) => {
      onIndexChange = options.onIndexChange;
      return {
         render: (items) => {
            carouselCalls.push(['render', items]);
            return renderResult;
         },
         showFirst: () => carouselCalls.push(['showFirst']),
         clear: () => carouselCalls.push(['clear']),
         step: (delta) => carouselCalls.push(['step', delta]),
         jumpTo: (fn) => carouselCalls.push(['jumpTo', fn]),
      };
   };

   GlobalListener.createTooltipGlobalListeners = (options) => {
      stepFn = options.step;
      closeFn = options.close;
      isOpenFn = options.isOpen;
      getItemAtIndex = options.getItemAtIndex;
      return {
         install: () => listenerCalls.push('install'),
         uninstall: () => listenerCalls.push('uninstall'),
      };
   };

   PositionFragment.positionTooltip = (tooltipEl, markerEl) => {
      positions.push([tooltipEl, markerEl]);
   };
   MarkerHelper.applyMarkerVisual = (...args) => visualCalls.push(args);
   MarkerHelper.setMarkerToAnimalIcon = (...args) => animalIconCalls.push(args);

   return {
      bannerSyncs,
      bannerHides,
      carouselCalls,
      listenerCalls,
      positions,
      visualCalls,
      animalIconCalls,
      getOnIndexChange: () => onIndexChange,
      getStepFn: () => stepFn,
      getCloseFn: () => closeFn,
      getIsOpenFn: () => isOpenFn,
      getItemAtIndex: () => getItemAtIndex,
      restore() {
         BannerSynchronizer.createTooltipBannerSync = originals.banners;
         CarouselView.createTooltipCarouselView = originals.carousel;
         GlobalListener.createTooltipGlobalListeners = originals.listeners;
         PositionFragment.positionTooltip = originals.position;
         MarkerHelper.applyMarkerVisual = originals.applyVisual;
         MarkerHelper.setMarkerToAnimalIcon = originals.setAnimal;
         TooltipRenderer.getRendererForItem = originals.getRenderer;
      },
   };
}


function _createApi(tooltipEl) {
   return TooltipController.createTooltipController({
      tooltipEl,
      onAnimalCardClick: () => {},
      offDisplayBanner: {},
      restaurantClosedBanner: {},
      restroomMessageBanner: {},
      giftShopClosedBanner: {},
      attractionClosedBanner: {},
      drinkingFountainClosedBanner: {},
   });
}


test('Test_CreateTooltipController_TestOpen_ExpectVisible', () => {
   const stubs = _stubTooltipDeps({ renderResult: true });
   const tooltipEl = document.createElement('div');
   tooltipEl.style.display = 'none';
   const lion = { type: ItemType.ANIMAL, species: 'African Lion' };
   const cafe = { type: ItemType.RESTAURANT, name: 'Peaks Cafe' };
   const items = [lion, cafe];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.open(markerEl, items);

      assert.equal(tooltipEl.style.display, 'flex');
      assert.equal(tooltipEl.style.pointerEvents, 'auto');
      assert.deepEqual(api.getOpenItems(), items);
      assert.ok(stubs.carouselCalls.some(([kind]) => kind === 'showFirst'));
      assert.ok(stubs.listenerCalls.includes('install'));
      assert.deepEqual(stubs.positions.at(Position.LAST), [tooltipEl, markerEl]);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestIndexChange_ExpectBannerSync', () => {
   const stubs = _stubTooltipDeps({ renderResult: true });
   const tooltipEl = document.createElement('div');
   const lion = { type: ItemType.ANIMAL, species: 'African Lion' };
   const cafe = { type: ItemType.RESTAURANT, name: 'Peaks Cafe' };
   const items = [lion, cafe];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.open(markerEl, items);
      stubs.getOnIndexChange()(Position.FIRST);
      stubs.getOnIndexChange()(Position.SECOND);

      assert.deepEqual(stubs.animalIconCalls.at(Position.LAST)?.at(Position.FIRST), markerEl);
      assert.deepEqual(stubs.bannerSyncs.at(Position.LAST), cafe);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestToggle_ExpectClosed', () => {
   const stubs = _stubTooltipDeps({ renderResult: true });
   const tooltipEl = document.createElement('div');
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.open(markerEl, items);
      api.toggle(markerEl, items);

      assert.equal(tooltipEl.style.display, 'none');
      assert.ok(stubs.listenerCalls.includes('uninstall'));
      assert.ok(stubs.bannerHides.length >= Position.SECOND);
      assert.deepEqual(api.getOpenItems(), []);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestOpenWithoutMarker_ExpectEmpty', () => {
   const stubs = _stubTooltipDeps({ renderResult: true });
   const tooltipEl = document.createElement('div');
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      api.open(null, items);

      assert.deepEqual(api.getOpenItems(), []);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestRenderFails_ExpectStillInstalled', () => {
   const stubs = _stubTooltipDeps({ renderResult: false });
   const tooltipEl = document.createElement('div');

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.open(markerEl, [{ type: ItemType.ANIMAL, species: 'African Lion' }]);

      assert.ok(stubs.listenerCalls.includes('install'));
      assert.ok(stubs.bannerSyncs.length >= Position.SECOND);
      assert.equal(stubs.positions.length, Position.FIRST);
      assert.ok(stubs.getIsOpenFn()());
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestAttachAndHover_ExpectHandlers', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const hoverText = 'African Lion';
   const hover = {
      shows: [],
      moves: [],
      hides: 0,
      show(text, event) { this.shows.push([text, event]); },
      move(event) { this.moves.push(event); },
      hide() { this.hides += 1; },
   };
   const items = [{ type: ItemType.ANIMAL, species: hoverText }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      markerEl.dataset.hover = hoverText;
      api.attachToMarker(markerEl, items, hover);
      markerEl.listeners.mouseenter({ stopPropagation() {} });
      markerEl.listeners.mousemove({});
      markerEl.listeners.mouseleave();
      markerEl.click();

      assert.equal(hover.shows.at(Position.FIRST).at(Position.FIRST), hoverText);
      assert.equal(hover.moves.length, Position.SECOND);
      assert.equal(hover.hides, 2);
      assert.deepEqual(api.getOpenItems(), items);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestNonClickable_ExpectNoOpen', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const hover = {
      shows: [],
      moves: [],
      hides: 0,
      show() {},
      move() {},
      hide() { this.hides += 1; },
   };
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.attachToMarker(markerEl, items, hover);
      markerEl.click();
      const nonClickable = document.createElement('div');
      api.attachToMarker(nonClickable, items, hover, { clickable: false });
      nonClickable.click();

      assert.equal(api.getOpenItems().length, Position.SECOND);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestJumpAndStep_ExpectCarousel', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const species = 'African Lion';

   try {
      const api = _createApi(tooltipEl);
      api.jumpTo((item) => item.species === species);
      stubs.getStepFn()(1);
      const stepped = stubs.carouselCalls.some((call) => call.at(Position.FIRST) === 'step');
      stubs.getCloseFn()();

      assert.equal(stepped, true);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestMissingTooltip_ExpectGuards', () => {
   const stubs = _stubTooltipDeps();

   try {
      const withoutTooltip = _createApi(null);
      withoutTooltip.open(document.createElement('div'), [{ type: ItemType.ANIMAL }]);
      withoutTooltip.close();
      withoutTooltip.reposition();

      assert.deepEqual(withoutTooltip.getOpenItems(), []);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestReposition_ExpectPositioned', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.open(markerEl, [{ type: ItemType.RESTAURANT, name: 'Peaks Cafe' }]);
      stubs.positions.length = 0;
      api.reposition();
      stubs.getOnIndexChange()(Position.FIRST);

      assert.deepEqual(stubs.positions.at(Position.LAST), [tooltipEl, markerEl]);
      assert.equal(stubs.animalIconCalls.length, Position.FIRST);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestSyncMarkerGuards_ExpectNoop', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');

   try {
      const api = _createApi(tooltipEl);
      const onIndexChange = stubs.getOnIndexChange();
      onIndexChange(99);
      const markerEl = document.createElement('div');
      api.open(markerEl, [{ type: ItemType.ANIMAL, species: 'African Lion' }]);
      onIndexChange(99);
      api.close();
      onIndexChange(Position.FIRST);

      assert.equal(stubs.animalIconCalls.length, Position.FIRST);
   } finally {
      stubs.restore();
   }
});
