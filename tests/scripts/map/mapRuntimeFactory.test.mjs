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
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_HasRequiredRuntimeElements_TestPresent_ExpectTrue', () => {
   const hasElements = MapRuntimeFactory.hasRequiredRuntimeElements({
      mapInner: {},
      tooltipEl: {},
      viewportEl: {},
   });

   assert.equal(hasElements, true);
});


test('Test_HasRequiredRuntimeElements_TestMissingInner_ExpectFalse', () => {
   const hasElements = MapRuntimeFactory.hasRequiredRuntimeElements({
      mapInner: null,
      tooltipEl: {},
      viewportEl: {},
   });

   assert.equal(hasElements, false);
});


test('Test_CreateMapBannerSet_TestFragments_ExpectBannerKeys', () => {
   const originalOff = OffDisplayFragment.createOffDisplayBanner;
   const originalRestaurant = RestaurantClosedFragment.createRestaurantClosedBanner;
   const originalRestroom = RestroomMessageFragment.createRestroomMessageBanner;
   const originalGift = GiftShopClosedFragment.createGiftShopClosedBanner;
   const originalAttraction = AttractionClosedFragment.createAttractionClosedBanner;
   const originalFountain = DrinkingFountainClosedFragment.createDrinkingFountainClosedBanner;
   const offDisplayBanner = 'off';
   const restaurantClosedBanner = 'restaurant';
   const restroomMessageBanner = 'restroom';
   const giftShopClosedBanner = 'gift';
   const attractionClosedBanner = 'attraction';
   const drinkingFountainClosedBanner = 'fountain';

   OffDisplayFragment.createOffDisplayBanner = () => offDisplayBanner;
   RestaurantClosedFragment.createRestaurantClosedBanner = () => restaurantClosedBanner;
   RestroomMessageFragment.createRestroomMessageBanner = () => restroomMessageBanner;
   GiftShopClosedFragment.createGiftShopClosedBanner = () => giftShopClosedBanner;
   AttractionClosedFragment.createAttractionClosedBanner = () => attractionClosedBanner;
   DrinkingFountainClosedFragment.createDrinkingFountainClosedBanner = () => drinkingFountainClosedBanner;

   try {
      const banners = MapRuntimeFactory.createMapBannerSet();

      assert.deepEqual(banners, {
         offDisplayBanner,
         restaurantClosedBanner,
         restroomMessageBanner,
         giftShopClosedBanner,
         attractionClosedBanner,
         drinkingFountainClosedBanner,
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


test('Test_CreateAnimalCardClickHandler_TestAnimal_ExpectOpened', () => {
   const openedAnimals = [];
   const animal = { type: ItemType.ANIMAL, species: 'African Lion' };
   const handler = MapRuntimeFactory.createAnimalCardClickHandler({
      openFromAnimal: (item) => {
         openedAnimals.push(item);
      },
   });

   handler(animal);

   assert.deepEqual(openedAnimals, [animal]);
});


test('Test_CreateAnimalCardClickHandler_TestTalk_ExpectOpened', async () => {
   const openedTalks = [];
   const originalOpen = GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal;
   const talk = { type: ItemType.GUARDIANS_TALK, name: 'Amur Tiger' };
   GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal = async (item) => {
      openedTalks.push(item);
   };

   try {
      const handler = MapRuntimeFactory.createAnimalCardClickHandler({
         openFromAnimal: () => {},
      });
      handler(talk);
      await Promise.resolve();

      assert.deepEqual(openedTalks, [talk]);
   } finally {
      GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal = originalOpen;
   }
});


test('Test_CreateAnimalCardClickHandler_TestRestaurant_ExpectIgnored', () => {
   const openedAnimals = [];
   const handler = MapRuntimeFactory.createAnimalCardClickHandler({
      openFromAnimal: (item) => {
         openedAnimals.push(item);
      },
   });

   handler({ type: ItemType.RESTAURANT });

   assert.deepEqual(openedAnimals, []);
});


test('Test_CreateMapTooltipAndFocus_TestWiring_ExpectControllers', () => {
   const originalBannerSet = MapRuntimeFactory.createMapBannerSet;
   const originalClickHandler = MapRuntimeFactory.createAnimalCardClickHandler;
   const originalTooltip = TooltipController.createTooltipController;
   const originalFocus = FocusController.createFocusController;
   const originalLabels = LabelPresenter.initLabelVisibilityToggle;
   const clickHandler = 'click-handler';
   const banner = true;
   const coordKey = '1|2';
   const allMarkers = ['a'];
   const viewportId = 'vp';

   MapRuntimeFactory.createMapBannerSet = () => ({ banner });
   MapRuntimeFactory.createAnimalCardClickHandler = () => clickHandler;
   TooltipController.createTooltipController = (options) => ({ tooltip: true, options });
   FocusController.createFocusController = (options) => ({ focus: true, options });
   LabelPresenter.initLabelVisibilityToggle = () => {};

   try {
      const tooltip = MapRuntimeFactory.createMapTooltip({
         tooltipEl: { id: 'tip' },
         speciesOverlay: {},
      });
      const markers = {
         getMarkerByCoord: (key) => `marker:${key}`,
         getAllMarkers: () => allMarkers,
      };
      const focus = MapRuntimeFactory.createMapFocus({
         panzoom: {},
         markers,
         tooltip,
         viewportEl: { id: viewportId },
      });
      MapRuntimeFactory.initMapLabels({ id: 'labels' });

      assert.equal(tooltip.tooltip, true);
      assert.equal(tooltip.options.onAnimalCardClick, clickHandler);
      assert.equal(tooltip.options.banner, banner);
      assert.equal(focus.focus, true);
      assert.equal(focus.options.getMarkerByCoord(coordKey), `marker:${coordKey}`);
      assert.deepEqual(focus.options.getAllMarkers(), allMarkers);
      assert.equal(focus.options.getViewportEl().id, viewportId);
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
         tooltip: {
            reposition: () => {
               calls.push('tooltip');
            },
         },
         hover: {
            reposition: () => {
               calls.push('hover');
            },
         },
      });
      reposition();

      assert.deepEqual(calls, ['tooltip', 'hover', 'tooltip', 'hover']);
   } finally {
      globalThis.requestAnimationFrame = originalRaf;
   }
});
