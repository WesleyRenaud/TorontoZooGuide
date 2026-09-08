import assert from 'node:assert/strict';
import test from 'node:test';

import { MapRuntimeFactory } from '../../../scripts/map/mapRuntimeFactory.js';
import { OffDisplayFragment } from '../../../scripts/banners/offDisplayFragment.js';
import { RestaurantClosedFragment } from '../../../scripts/banners/restaurantClosedFragment.js';
import { RestroomMessageFragment } from '../../../scripts/banners/restroomMessageFragment.js';
import { GiftShopClosedFragment } from '../../../scripts/banners/giftShopClosedFragment.js';
import { AttractionClosedFragment } from '../../../scripts/banners/attractionClosedFragment.js';
import { DrinkingFountainClosedFragment } from '../../../scripts/banners/drinkingFountainClosedFragment.js';
import { GuardiansTalkLinkedAnimalOpener } from '../../../scripts/guardians/guardiansTalkLinkedAnimalOpener.js';
import { LabelPresenter } from '../../../scripts/map/labelPresenter.js';
import { TooltipController } from '../../../scripts/tooltips/tooltipController.js';
import { FocusController } from '../../../scripts/focus/focusController.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_HasRequiredRuntimeElements_TestPresence_ExpectBoolean', () => {
   assert.equal(
      MapRuntimeFactory.hasRequiredRuntimeElements({
         mapInner: {},
         tooltipEl: {},
         viewportEl: {},
      }),
      true
   );
   assert.equal(
      MapRuntimeFactory.hasRequiredRuntimeElements({
         mapInner: null,
         tooltipEl: {},
         viewportEl: {},
      }),
      false
   );
});

test('Test_CreateMapBannerSet_TestFragments_ExpectBannerKeys', () => {
   const originalOff = OffDisplayFragment.createOffDisplayBanner;
   const originalRestaurant = RestaurantClosedFragment.createRestaurantClosedBanner;
   const originalRestroom = RestroomMessageFragment.createRestroomMessageBanner;
   const originalGift = GiftShopClosedFragment.createGiftShopClosedBanner;
   const originalAttraction = AttractionClosedFragment.createAttractionClosedBanner;
   const originalFountain = DrinkingFountainClosedFragment.createDrinkingFountainClosedBanner;

   OffDisplayFragment.createOffDisplayBanner = () => 'off';
   RestaurantClosedFragment.createRestaurantClosedBanner = () => 'restaurant';
   RestroomMessageFragment.createRestroomMessageBanner = () => 'restroom';
   GiftShopClosedFragment.createGiftShopClosedBanner = () => 'gift';
   AttractionClosedFragment.createAttractionClosedBanner = () => 'attraction';
   DrinkingFountainClosedFragment.createDrinkingFountainClosedBanner = () => 'fountain';

   try {
      assert.deepEqual(MapRuntimeFactory.createMapBannerSet(), {
         offDisplayBanner: 'off',
         restaurantClosedBanner: 'restaurant',
         restroomMessageBanner: 'restroom',
         giftShopClosedBanner: 'gift',
         attractionClosedBanner: 'attraction',
         drinkingFountainClosedBanner: 'fountain',
      });
   } finally {
      OffDisplayFragment.createOffDisplayBanner = originalOff;
      RestaurantClosedFragment.createRestaurantClosedBanner = originalRestaurant;
      RestroomMessageFragment.createRestroomMessageBanner = originalRestroom;
      GiftShopClosedFragment.createGiftShopClosedBanner = originalGift;
      AttractionClosedFragment.createAttractionClosedBanner = originalAttraction;
      DrinkingFountainClosedFragment.createDrinkingFountainClosedBanner = originalFountain;
   }
});

test('Test_CreateAnimalCardClickHandler_TestAnimalAndTalk_ExpectHandlers', async () => {
   const openedAnimals = [];
   const openedTalks = [];
   const originalOpen = GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal;
   GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal = async (item) => {
      openedTalks.push(item);
   };

   try {
      const handler = MapRuntimeFactory.createAnimalCardClickHandler({
         openFromAnimal: (item) => { openedAnimals.push(item); },
      });

      handler({ type: 'animal', species: 'Lion' });
      handler({ type: 'guardiansTalk', name: 'Talk' });
      handler({ type: 'restaurant' });

      assert.deepEqual(openedAnimals, [{ type: 'animal', species: 'Lion' }]);
      await Promise.resolve();
      assert.deepEqual(openedTalks, [{ type: 'guardiansTalk', name: 'Talk' }]);
   } finally {
      GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal = originalOpen;
   }
});

test('Test_CreateMapTooltipAndFocus_TestWiring_ExpectControllers', () => {
   const originalBannerSet = MapRuntimeFactory.createMapBannerSet;
   const originalClickHandler = MapRuntimeFactory.createAnimalCardClickHandler;
   const originalTooltip = TooltipController.createTooltipController;
   const originalFocus = FocusController.createFocusController;
   const originalLabels = LabelPresenter.initLabelVisibilityToggle;

   MapRuntimeFactory.createMapBannerSet = () => ({ banner: true });
   MapRuntimeFactory.createAnimalCardClickHandler = () => 'click-handler';
   TooltipController.createTooltipController = (options) => ({ tooltip: true, options });
   FocusController.createFocusController = (options) => ({ focus: true, options });
   LabelPresenter.initLabelVisibilityToggle = () => {};

   try {
      const tooltip = MapRuntimeFactory.createMapTooltip({
         tooltipEl: { id: 'tip' },
         speciesOverlay: {},
      });
      assert.equal(tooltip.tooltip, true);
      assert.equal(tooltip.options.onAnimalCardClick, 'click-handler');
      assert.equal(tooltip.options.banner, true);

      const markers = {
         getMarkerByCoord: (key) => `marker:${key}`,
         getAllMarkers: () => ['a'],
      };
      const focus = MapRuntimeFactory.createMapFocus({
         panzoom: {},
         markers,
         tooltip,
         viewportEl: { id: 'vp' },
      });
      assert.equal(focus.focus, true);
      assert.equal(focus.options.getMarkerByCoord('1|2'), 'marker:1|2');
      assert.deepEqual(focus.options.getAllMarkers(), ['a']);
      assert.equal(focus.options.getViewportEl().id, 'vp');

      MapRuntimeFactory.initMapLabels({ id: 'labels' });
   } finally {
      MapRuntimeFactory.createMapBannerSet = originalBannerSet;
      MapRuntimeFactory.createAnimalCardClickHandler = originalClickHandler;
      TooltipController.createTooltipController = originalTooltip;
      FocusController.createFocusController = originalFocus;
      LabelPresenter.initLabelVisibilityToggle = originalLabels;
   }
});

test('Test_CreateTooltipRepositioner_TestCalls_ExpectImmediateAndRaf', async () => {
   const calls = [];
   const originalRaf = globalThis.requestAnimationFrame;
   globalThis.requestAnimationFrame = (cb) => {
      cb();
      return 1;
   };

   try {
      const reposition = MapRuntimeFactory.createTooltipRepositioner({
         tooltip: { reposition: () => { calls.push('tooltip'); } },
         hover: { reposition: () => { calls.push('hover'); } },
      });

      reposition();
      assert.deepEqual(calls, ['tooltip', 'hover', 'tooltip', 'hover']);
   } finally {
      globalThis.requestAnimationFrame = originalRaf;
   }
});
