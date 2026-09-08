import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerHelper } from '../../../scripts/markers/markerHelper.js';
import { BannerSynchronizer } from '../../../scripts/tooltips/bannerSynchronizer.js';
import { CarouselView } from '../../../scripts/tooltips/carouselView.js';
import { GlobalListener } from '../../../scripts/tooltips/globalListener.js';
import { PositionFragment } from '../../../scripts/tooltips/positionFragment.js';
import { TooltipController } from '../../../scripts/tooltips/tooltipController.js';
import { TooltipRenderer } from '../../../scripts/tooltips/tooltipRenderer.js';
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

test('Test_CreateTooltipController_TestOpenCloseToggle_ExpectState', () => {
   const stubs = _stubTooltipDeps({ renderResult: true });
   const tooltipEl = document.createElement('div');
   tooltipEl.style.display = 'none';

   try {
      const api = TooltipController.createTooltipController({
         tooltipEl,
         onAnimalCardClick: () => {},
         offDisplayBanner: {},
         restaurantClosedBanner: {},
         restroomMessageBanner: {},
         giftShopClosedBanner: {},
         attractionClosedBanner: {},
         drinkingFountainClosedBanner: {},
      });

      const markerEl = document.createElement('div');
      const items = [{ type: 'animal', species: 'Lion' }, { type: 'restaurant', name: 'Peaks' }];

      api.open(markerEl, items);
      assert.equal(tooltipEl.style.display, 'flex');
      assert.equal(tooltipEl.style.pointerEvents, 'auto');
      assert.deepEqual(api.getOpenItems(), items);
      assert.ok(stubs.carouselCalls.some(([kind]) => kind === 'showFirst'));
      assert.ok(stubs.listenerCalls.includes('install'));
      assert.deepEqual(stubs.positions.at(-1), [tooltipEl, markerEl]);

      stubs.getOnIndexChange()(0);
      assert.deepEqual(stubs.animalIconCalls.at(-1)?.[0], markerEl);
      assert.deepEqual(stubs.bannerSyncs.at(-1), items[0]);

      stubs.getOnIndexChange()(1);
      assert.deepEqual(stubs.bannerSyncs.at(-1), items[1]);

      api.toggle(markerEl, items);
      assert.equal(tooltipEl.style.display, 'none');
      assert.ok(stubs.listenerCalls.includes('uninstall'));
      assert.ok(stubs.bannerHides.length >= 1);
      assert.deepEqual(api.getOpenItems(), []);

      api.open(null, items);
      assert.deepEqual(api.getOpenItems(), []);

      api.close();
   } finally {
      stubs.restore();
   }
});

test('Test_CreateTooltipController_TestRenderFails_ExpectStillInstalled', () => {
   const stubs = _stubTooltipDeps({ renderResult: false });
   const tooltipEl = document.createElement('div');

   try {
      const api = TooltipController.createTooltipController({
         tooltipEl,
         onAnimalCardClick: () => {},
         offDisplayBanner: {},
         restaurantClosedBanner: {},
         restroomMessageBanner: {},
         giftShopClosedBanner: {},
         attractionClosedBanner: {},
         drinkingFountainClosedBanner: {},
      });

      const markerEl = document.createElement('div');
      api.open(markerEl, [{ type: 'animal', species: 'Lion' }]);
      assert.ok(stubs.listenerCalls.includes('install'));
      assert.ok(stubs.bannerSyncs.length >= 1);
      assert.equal(stubs.positions.length, 0);
      assert.ok(stubs.getIsOpenFn()());
   } finally {
      stubs.restore();
   }
});

test('Test_CreateTooltipController_TestAttachAndHover_ExpectHandlers', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const hover = {
      shows: [],
      moves: [],
      hides: 0,
      show(text, event) { this.shows.push([text, event]); },
      move(event) { this.moves.push(event); },
      hide() { this.hides += 1; },
   };

   try {
      const api = TooltipController.createTooltipController({
         tooltipEl,
         onAnimalCardClick: () => {},
         offDisplayBanner: {},
         restaurantClosedBanner: {},
         restroomMessageBanner: {},
         giftShopClosedBanner: {},
         attractionClosedBanner: {},
         drinkingFountainClosedBanner: {},
      });

      const markerEl = document.createElement('div');
      markerEl.dataset.hover = 'Lion';
      const items = [{ type: 'animal', species: 'Lion' }];

      api.attachToMarker(markerEl, items, hover);
      markerEl.listeners.mouseenter({ stopPropagation() {} });
      markerEl.listeners.mousemove({});
      markerEl.listeners.mouseleave();
      assert.equal(hover.shows[0][0], 'Lion');
      assert.equal(hover.moves.length, 1);
      assert.equal(hover.hides, 1);

      markerEl.click();
      assert.deepEqual(api.getOpenItems(), items);

      const nonClickable = document.createElement('div');
      api.attachToMarker(nonClickable, items, hover, { clickable: false });
      nonClickable.click();
      assert.equal(api.getOpenItems().length, 1);

      api.jumpTo((item) => item.species === 'Lion');
      assert.equal(stubs.carouselCalls.at(-1)[0], 'jumpTo');

      stubs.getStepFn()(1);
      assert.deepEqual(stubs.carouselCalls.at(-1), ['step', 1]);
      stubs.getCloseFn()();
   } finally {
      stubs.restore();
   }
});

test('Test_CreateTooltipController_TestRepositionAndMissingTooltip_ExpectGuards', () => {
   const stubs = _stubTooltipDeps();

   try {
      const withoutTooltip = TooltipController.createTooltipController({
         tooltipEl: null,
         onAnimalCardClick: () => {},
         offDisplayBanner: {},
         restaurantClosedBanner: {},
         restroomMessageBanner: {},
         giftShopClosedBanner: {},
         attractionClosedBanner: {},
         drinkingFountainClosedBanner: {},
      });

      withoutTooltip.open(document.createElement('div'), [{ type: 'animal' }]);
      withoutTooltip.close();
      withoutTooltip.reposition();

      const tooltipEl = document.createElement('div');
      const api = TooltipController.createTooltipController({
         tooltipEl,
         onAnimalCardClick: () => {},
         offDisplayBanner: {},
         restaurantClosedBanner: {},
         restroomMessageBanner: {},
         giftShopClosedBanner: {},
         attractionClosedBanner: {},
         drinkingFountainClosedBanner: {},
      });

      api.reposition();
      const markerEl = document.createElement('div');
      api.open(markerEl, [{ type: 'restaurant', name: 'Peaks' }]);
      stubs.positions.length = 0;
      api.reposition();
      assert.deepEqual(stubs.positions.at(-1), [tooltipEl, markerEl]);

      stubs.getOnIndexChange()(0);
      assert.equal(stubs.animalIconCalls.length, 0);
   } finally {
      stubs.restore();
   }
});
