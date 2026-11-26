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
import { Strings } from '../../../scripts/strings.js';
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
   let listenerOptions = null;

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
      listenerOptions = options;
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
      getListenerOptions: () => listenerOptions,
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


function _createHoverRecorder() {
   return {
      shows: [],
      hides: 0,
      show(text, markerEl) { this.shows.push([text, markerEl]); },
      move() {},
      hide() { this.hides += 1; },
   };
}


function _trackFocus(element) {
   element.focusCalls = [];
   element.focus = (options) => {
      element.focusCalls.push(options);
      document.activeElement = element;
   };
   return element;
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


test('Test_CreateTooltipController_TestClickableMarker_ExpectButtonSemantics', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const hoverText = 'Australasia Pavilion';
   const items = [{ type: ItemType.PAVILION, name: hoverText }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      markerEl.dataset.hover = hoverText;
      api.attachToMarker(markerEl, items, _createHoverRecorder());

      assert.equal(markerEl.getAttribute('role'), 'button');
      assert.equal(markerEl.getAttribute('tabindex'), '0');
      assert.equal(markerEl.getAttribute('aria-label'), hoverText);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestAnimalCluster_ExpectAccessibleNameStartsWithCount', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const firstSpecies = 'Black Tree Monitor';
   const items = [
      { type: ItemType.ANIMAL, species: firstSpecies },
      ...Array.from({ length: 36 }, (_, index) => ({
         type: ItemType.ANIMAL,
         species: `Other ${index}`,
      })),
   ];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      markerEl.dataset.hover = `${firstSpecies} ${Strings.format.moreCount(36)}`;
      api.attachToMarker(markerEl, items, _createHoverRecorder());

      assert.equal(markerEl.getAttribute('aria-label'), '37 species: Black Tree Monitor and 36 more');
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestMarkerWithoutHoverText_ExpectFallbackLabel', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const items = [{ type: ItemType.TRANSPORTATION_ROUTE_MARKER }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.attachToMarker(markerEl, items, _createHoverRecorder());

      assert.equal(markerEl.getAttribute('aria-label'), Strings.map.markerAria);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestNonClickableMarker_ExpectNotFocusable', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.attachToMarker(markerEl, items, _createHoverRecorder(), { clickable: false });

      assert.equal(markerEl.getAttribute('role'), null);
      assert.equal(markerEl.getAttribute('tabindex'), null);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestMarkerEnterKey_ExpectOpen', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const hover = _createHoverRecorder();
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.attachToMarker(markerEl, items, hover);
      const notPrevented = markerEl.dispatchEvent({ type: 'keydown', key: 'Enter' });

      assert.equal(notPrevented, false);
      assert.equal(hover.hides, 1);
      assert.deepEqual(api.getOpenItems(), items);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestMarkerSpaceKeyTwice_ExpectClosed', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.dispatchEvent({ type: 'keydown', key: ' ' });
      markerEl.dispatchEvent({ type: 'keydown', key: ' ' });

      assert.deepEqual(api.getOpenItems(), []);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestMarkerOtherKey_ExpectIgnored', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      const notPrevented = markerEl.dispatchEvent({ type: 'keydown', key: 'Tab' });

      assert.equal(notPrevented, true);
      assert.deepEqual(api.getOpenItems(), []);
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


test('Test_CreateTooltipController_TestClickableMarker_ExpectCollapsedDisclosureState', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   tooltipEl.id = 'tooltip';
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      api.attachToMarker(markerEl, items, _createHoverRecorder());

      assert.equal(markerEl.getAttribute('aria-expanded'), 'false');
      assert.equal(markerEl.getAttribute('aria-controls'), 'tooltip');
      assert.equal(tooltipEl.getAttribute('role'), 'dialog');
      assert.equal(tooltipEl.getAttribute('aria-modal'), null);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestMarkerEnterKey_ExpectFocusMovedAndNamed', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = _trackFocus(document.createElement('div'));
      markerEl.dataset.hover = 'African Lion';
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.focus();
      markerEl.dispatchEvent({ type: 'keydown', key: 'Enter' });

      assert.equal(document.activeElement, tooltipEl);
      assert.equal(markerEl.getAttribute('aria-expanded'), 'true');
      assert.equal(tooltipEl.getAttribute('aria-label'), Strings.tooltips.detailsAria('African Lion'));
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestMarkerClick_ExpectFocusMoved', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = _trackFocus(document.createElement('div'));
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.click();

      assert.equal(document.activeElement, tooltipEl);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestProgrammaticOpen_ExpectFocusUnchanged', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   const searchBox = _trackFocus(document.createElement('input'));
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = document.createElement('div');
      searchBox.focus();
      api.open(markerEl, items);

      assert.equal(document.activeElement, searchBox);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestCloseWithFocusInside_ExpectFocusReturnedToMarker', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = _trackFocus(document.createElement('div'));
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.dispatchEvent({ type: 'keydown', key: 'Enter' });
      stubs.getCloseFn()();

      assert.equal(document.activeElement, markerEl);
      assert.equal(markerEl.getAttribute('aria-expanded'), 'false');
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestCloseWithFocusOutside_ExpectFocusUnchanged', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   const otherEl = _trackFocus(document.createElement('div'));
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = _trackFocus(document.createElement('div'));
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.dispatchEvent({ type: 'keydown', key: 'Enter' });
      otherEl.focus();
      stubs.getCloseFn()();

      assert.equal(document.activeElement, otherEl);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestTabFromOpenMarker_ExpectFocusIntoTooltip', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   tooltipEl.style.display = 'none';
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = _trackFocus(document.createElement('div'));
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      api.open(markerEl, items);
      markerEl.focus();
      const notPrevented = markerEl.dispatchEvent({ type: 'keydown', key: 'Tab' });

      assert.equal(notPrevented, false);
      assert.equal(document.activeElement, tooltipEl);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestTabFromClosedMarker_ExpectNativeTab', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   tooltipEl.style.display = 'none';
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = _trackFocus(document.createElement('div'));
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.focus();
      const notPrevented = markerEl.dispatchEvent({ type: 'keydown', key: 'Tab' });

      assert.equal(notPrevented, true);
      assert.equal(document.activeElement, markerEl);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestKeyboardSuspendedOption_ExpectPassedToGlobalListeners', () => {
   const stubs = _stubTooltipDeps();
   const isKeyboardSuspended = () => true;

   try {
      TooltipController.createTooltipController({
         tooltipEl: document.createElement('div'),
         isKeyboardSuspended,
      });

      assert.equal(stubs.getListenerOptions().isKeyboardSuspended, isKeyboardSuspended);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestMouseClickMarker_ExpectFocusWithoutRing', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = _trackFocus(document.createElement('div'));
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.dispatchEvent({ type: 'click', detail: 1 });

      assert.equal(document.activeElement, tooltipEl);
      assert.deepEqual(tooltipEl.focusCalls, [{ preventScroll: true, focusVisible: false }]);
      assert.equal(tooltipEl.hasAttribute('data-pointer-opened'), true);

      markerEl.dispatchEvent({ type: 'click', detail: 1 });
      assert.equal(tooltipEl.hasAttribute('data-pointer-opened'), false);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestKeyboardOpenMarker_ExpectFocusRingKept', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];

   try {
      const api = _createApi(tooltipEl);
      const markerEl = _trackFocus(document.createElement('div'));
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.dispatchEvent({ type: 'keydown', key: 'Enter' });
      markerEl.dispatchEvent({ type: 'keydown', key: 'Enter' });
      markerEl.dispatchEvent({ type: 'click', detail: 0 });

      assert.deepEqual(tooltipEl.focusCalls, [{ preventScroll: true }, { preventScroll: true }]);
      assert.equal(tooltipEl.hasAttribute('data-pointer-opened'), false);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestSpeciesLinkActivation_ExpectPinPassedAsFocusFallback', () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = document.createElement('div');
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];
   const clicks = [];

   try {
      const api = TooltipController.createTooltipController({
         tooltipEl,
         onAnimalCardClick: (item, context) => clicks.push([item, context]),
      });
      const markerEl = document.createElement('div');
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.dispatchEvent({ type: 'keydown', key: 'Enter' });
      stubs.getListenerOptions().onAnimalCardClick(items[0]);

      assert.deepEqual(clicks, [[items[0], { returnFocusFallback: markerEl }]]);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateTooltipController_TestKeyboardSuspended_ExpectFocusLeaveSuspended', async () => {
   const stubs = _stubTooltipDeps();
   const tooltipEl = _trackFocus(document.createElement('div'));
   const outside = _trackFocus(document.createElement('div'));
   const items = [{ type: ItemType.ANIMAL, species: 'African Lion' }];
   let suspended = true;

   try {
      const api = TooltipController.createTooltipController({
         tooltipEl,
         isKeyboardSuspended: () => suspended,
      });
      const markerEl = _trackFocus(document.createElement('div'));
      api.attachToMarker(markerEl, items, _createHoverRecorder());
      markerEl.dispatchEvent({ type: 'keydown', key: 'Enter' });
      outside.focus();
      tooltipEl.dispatchEvent({ type: 'focusout' });
      await new Promise((resolve) => setTimeout(resolve, 5));

      assert.deepEqual(api.getOpenItems(), items);

      suspended = false;
      tooltipEl.dispatchEvent({ type: 'focusout' });
      await new Promise((resolve) => setTimeout(resolve, 5));

      assert.deepEqual(api.getOpenItems(), []);
   } finally {
      stubs.restore();
   }
});
