import assert from 'node:assert/strict';
import test from 'node:test';

import { IconUrlProvider } from '../../../scripts/assets/iconUrlProvider.js';
import { MarkerTypeRendererFactory } from '../../../scripts/markers/markerTypeRendererFactory.js';
import { MarkerVisualHelper } from '../../../scripts/markers/markerVisualHelper.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

function _markerEl() {
   return document.createElement('div');
}

test('Test_ShouldShowLimitedViewingIndicator_TestCases_ExpectBoolean', () => {
   assert.equal(MarkerTypeRendererFactory.shouldShowLimitedViewingIndicator(null), false);
   assert.equal(MarkerTypeRendererFactory.shouldShowLimitedViewingIndicator({
      off_display_message: 'Off',
      has_limited_viewing_schedule: true,
      limited_viewing_message: 'Limited',
   }), false);
   assert.equal(MarkerTypeRendererFactory.shouldShowLimitedViewingIndicator({
      has_limited_viewing_schedule: true,
      limited_viewing_message: 'Limited',
   }), true);
   assert.equal(MarkerTypeRendererFactory.shouldShowLimitedViewingIndicator({
      viewing_alert_messages: ['Alert'],
   }), true);
});

test('Test_ShouldShowRestroomAlertIndicator_TestCases_ExpectBoolean', () => {
   assert.equal(MarkerTypeRendererFactory.shouldShowRestroomAlertIndicator({
      is_closed: true,
      has_alert: true,
      alert_message: 'Alert',
   }), false);
   assert.equal(MarkerTypeRendererFactory.shouldShowRestroomAlertIndicator({
      is_closed: false,
      has_alert: true,
      alert_message: 'Alert',
   }), true);
   assert.equal(MarkerTypeRendererFactory.shouldShowRestroomAlertIndicator({
      is_closed: false,
      has_alert: true,
   }), false);
});

test('Test_ApplyAttractionMarkerSize_TestOverrides_ExpectSized', () => {
   const markerEl = _markerEl();

   MarkerTypeRendererFactory.applyAttractionMarkerSize(markerEl, 'Unknown');
   assert.equal(markerEl.style.width, undefined);

   MarkerTypeRendererFactory.applyAttractionMarkerSize(markerEl, 'Splash Island');
   assert.equal(markerEl.style.width, '80px');
   assert.equal(markerEl.style.height, '80px');
});

test('Test_ApplyOptionalSize_TestCallable_ExpectInvoked', () => {
   const calls = [];
   MarkerTypeRendererFactory.applyOptionalSize({ id: 1 }, { name: 'A' }, (el, item) => {
      calls.push([el, item]);
   });
   MarkerTypeRendererFactory.applyOptionalSize({}, {}, null);
   assert.equal(calls.length, 1);
});

test('Test_CreateGenericIconMarkerRenderer_TestCount_ExpectVisualHelpers', () => {
   const calls = [];
   const originalClass = MarkerVisualHelper.applyMarkerClass;
   const originalGeneric = MarkerVisualHelper.applyGenericIcon;

   MarkerVisualHelper.applyMarkerClass = (...args) => calls.push(['class', ...args]);
   MarkerVisualHelper.applyGenericIcon = (...args) => calls.push(['icon', ...args]);

   try {
      const render = MarkerTypeRendererFactory.createGenericIconMarkerRenderer(ItemType.PAVILION);
      const markerEl = _markerEl();
      render(markerEl, [{ type: ItemType.PAVILION }, { type: ItemType.PAVILION }]);
      assert.deepEqual(calls[0], [
         'class',
         markerEl,
         MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE[ItemType.PAVILION],
      ]);
      assert.deepEqual(calls[1], [
         'icon',
         markerEl,
         MarkerTypeRendererFactory.GENERIC_ICON_PATHS[ItemType.PAVILION],
         2,
      ]);
   } finally {
      MarkerVisualHelper.applyMarkerClass = originalClass;
      MarkerVisualHelper.applyGenericIcon = originalGeneric;
   }
});

test('Test_CreateLikelihoodIconMarkerRenderer_TestSingleAndCount_ExpectIcons', () => {
   const calls = [];
   const originalClass = MarkerVisualHelper.applyMarkerClass;
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalBg = MarkerVisualHelper.applyBackgroundImage;
   const originalLikelihood = MarkerVisualHelper.getLikelihoodVisual;

   MarkerVisualHelper.applyMarkerClass = (...args) => calls.push(['class', ...args]);
   MarkerVisualHelper.applyCountMarker = (...args) => calls.push(['count', ...args]);
   MarkerVisualHelper.applyBackgroundImage = (...args) => calls.push(['bg', ...args]);
   MarkerVisualHelper.getLikelihoodVisual = () => ({ colour: '#abc', iconToken: 'open' });

   try {
      const render = MarkerTypeRendererFactory.createLikelihoodIconMarkerRenderer({
         type: ItemType.RESTAURANT,
         getIconUrl: (_item, token) => `url-${token}`,
         applySize: (el) => calls.push(['size', el]),
      });
      const markerEl = _markerEl();

      render(markerEl, [{ likelihood: 100 }, { likelihood: 50 }]);
      assert.ok(calls.some(([kind]) => kind === 'count'));

      calls.length = 0;
      render(markerEl, [{ likelihood: 100 }]);
      assert.ok(calls.some((entry) => entry[0] === 'bg' && entry[2] === 'url-open'));
      assert.ok(calls.some(([kind]) => kind === 'size'));
   } finally {
      MarkerVisualHelper.applyMarkerClass = originalClass;
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerVisualHelper.applyBackgroundImage = originalBg;
      MarkerVisualHelper.getLikelihoodVisual = originalLikelihood;
   }
});

test('Test_RenderAnimalMarker_TestCountAndLimited_ExpectVisuals', () => {
   const calls = [];
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalBg = MarkerVisualHelper.applyBackgroundImage;
   const originalClass = MarkerVisualHelper.applyMarkerClass;
   const originalLikelihood = MarkerVisualHelper.getLikelihoodVisual;
   const originalAnimalUrl = IconUrlProvider.getAnimalIconUrl;

   MarkerVisualHelper.applyCountMarker = (...args) => calls.push(['count', ...args]);
   MarkerVisualHelper.applyBackgroundImage = (...args) => calls.push(['bg', ...args]);
   MarkerVisualHelper.applyMarkerClass = (...args) => calls.push(['class', ...args]);
   MarkerVisualHelper.getLikelihoodVisual = () => ({ colour: '#ff0000' });
   IconUrlProvider.getAnimalIconUrl = (...args) => {
      calls.push(['url', ...args]);
      return 'animal-url';
   };

   try {
      const markerEl = _markerEl();
      MarkerTypeRendererFactory.renderAnimalMarker(markerEl, [
         { species: 'Lion', exhibit: 'Africa', likelihood: 80 },
         { species: 'Tiger' },
      ]);
      assert.ok(calls.some(([kind]) => kind === 'count'));

      calls.length = 0;
      MarkerTypeRendererFactory.renderAnimalMarker(markerEl, [{
         species: 'Lion',
         exhibit: 'Africa',
         likelihood: 80,
         viewing_alert_messages: ['Alert'],
      }]);
      assert.ok(calls.some((entry) => entry[0] === 'bg' && entry[2] === 'animal-url'));
      assert.ok(calls.some((entry) => (
         entry[0] === 'class'
         && entry[2] === MarkerTypeRendererFactory.LIMITED_VIEWING_MARKER_CLASS
      )));
   } finally {
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerVisualHelper.applyBackgroundImage = originalBg;
      MarkerVisualHelper.applyMarkerClass = originalClass;
      MarkerVisualHelper.getLikelihoodVisual = originalLikelihood;
      IconUrlProvider.getAnimalIconUrl = originalAnimalUrl;
   }
});

test('Test_RenderRestroomMarker_TestClosedAndAlert_ExpectVisuals', () => {
   const calls = [];
   const originalClass = MarkerVisualHelper.applyMarkerClass;
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalBg = MarkerVisualHelper.applyBackgroundImage;
   const originalLikelihood = MarkerVisualHelper.getLikelihoodVisual;
   const originalUrl = IconUrlProvider.getRestroomIconUrl;

   MarkerVisualHelper.applyMarkerClass = (...args) => calls.push(['class', ...args]);
   MarkerVisualHelper.applyCountMarker = (...args) => calls.push(['count', ...args]);
   MarkerVisualHelper.applyBackgroundImage = (...args) => calls.push(['bg', ...args]);
   MarkerVisualHelper.getLikelihoodVisual = (likelihood) => ({
      colour: likelihood === 0 ? '#000' : '#fff',
      iconToken: likelihood === 0 ? 'closed-token' : 'open',
   });
   IconUrlProvider.getRestroomIconUrl = (token) => `restroom-${token}`;

   try {
      const markerEl = _markerEl();
      MarkerTypeRendererFactory.renderRestroomMarker(markerEl, [
         { is_closed: false },
         { is_closed: false },
      ]);
      assert.ok(calls.some(([kind]) => kind === 'count'));

      calls.length = 0;
      MarkerTypeRendererFactory.renderRestroomMarker(markerEl, [{
         is_closed: true,
      }]);
      assert.ok(calls.some((entry) => (
         entry[0] === 'bg' && entry[2] === `restroom-${MarkerTypeRendererFactory.CLOSED_RESTROOM_ICON_TOKEN}`
      )));

      calls.length = 0;
      MarkerTypeRendererFactory.renderRestroomMarker(markerEl, [{
         is_closed: false,
         has_alert: true,
         alert_message: 'Alert',
      }]);
      assert.ok(calls.some((entry) => (
         entry[0] === 'class'
         && entry[2] === MarkerTypeRendererFactory.LIMITED_VIEWING_MARKER_CLASS
      )));
   } finally {
      MarkerVisualHelper.applyMarkerClass = originalClass;
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerVisualHelper.applyBackgroundImage = originalBg;
      MarkerVisualHelper.getLikelihoodVisual = originalLikelihood;
      IconUrlProvider.getRestroomIconUrl = originalUrl;
   }
});

test('Test_RenderTransportationRouteMarker_TestRouteColors_ExpectBackground', () => {
   const originalClass = MarkerVisualHelper.applyMarkerClass;
   const classes = [];
   MarkerVisualHelper.applyMarkerClass = (...args) => classes.push(args);

   try {
      const winter = _markerEl();
      MarkerTypeRendererFactory.renderTransportationRouteMarker(winter, [{ route_type: 'winter' }]);
      assert.equal(winter.style.backgroundColor, MarkerTypeRendererFactory.ZOOMOBILE_ROUTE_COLORS.winter);

      const other = _markerEl();
      MarkerTypeRendererFactory.renderTransportationRouteMarker(other, [{ route_type: 'summer' }]);
      assert.equal(other.style.backgroundColor, MarkerTypeRendererFactory.ZOOMOBILE_ROUTE_COLORS.default);
      assert.ok(classes.length >= 2);
   } finally {
      MarkerVisualHelper.applyMarkerClass = originalClass;
   }
});

test('Test_RenderDrinkingFountainMarker_TestLikelihoodPaths_ExpectVisuals', () => {
   const calls = [];
   const originalClass = MarkerVisualHelper.applyMarkerClass;
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalBg = MarkerVisualHelper.applyBackgroundImage;
   const originalLikelihood = MarkerVisualHelper.getLikelihoodVisual;
   const originalUrl = IconUrlProvider.getDrinkingFountainIconUrl;

   MarkerVisualHelper.applyMarkerClass = (...args) => calls.push(['class', ...args]);
   MarkerVisualHelper.applyCountMarker = (...args) => calls.push(['count', ...args]);
   MarkerVisualHelper.applyBackgroundImage = (...args) => calls.push(['bg', ...args]);
   MarkerVisualHelper.getLikelihoodVisual = (likelihood) => ({
      colour: '#111',
      iconToken: String(likelihood),
   });
   IconUrlProvider.getDrinkingFountainIconUrl = (token) => `df-${token}`;

   try {
      const markerEl = _markerEl();
      MarkerTypeRendererFactory.renderDrinkingFountainMarker(markerEl, [
         { likelihood: 0.5 },
         { likelihood: 0.2 },
      ]);
      assert.ok(calls.some(([kind]) => kind === 'count'));

      calls.length = 0;
      MarkerTypeRendererFactory.renderDrinkingFountainMarker(markerEl, [{ is_closed: true }]);
      assert.ok(calls.some((entry) => entry[0] === 'bg' && entry[2] === 'df-0'));

      calls.length = 0;
      MarkerTypeRendererFactory.renderDrinkingFountainMarker(markerEl, [{ likelihood: 0.8 }]);
      assert.ok(calls.some((entry) => entry[0] === 'bg' && entry[2] === 'df-80'));
   } finally {
      MarkerVisualHelper.applyMarkerClass = originalClass;
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerVisualHelper.applyBackgroundImage = originalBg;
      MarkerVisualHelper.getLikelihoodVisual = originalLikelihood;
      IconUrlProvider.getDrinkingFountainIconUrl = originalUrl;
   }
});

test('Test_RenderGuestServiceMarker_TestFirstAidAndCount_ExpectVisuals', () => {
   const calls = [];
   const originalClass = MarkerVisualHelper.applyMarkerClass;
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalBg = MarkerVisualHelper.applyBackgroundImage;
   const originalUrl = IconUrlProvider.getGuestServiceIconUrl;

   MarkerVisualHelper.applyMarkerClass = (...args) => calls.push(['class', ...args]);
   MarkerVisualHelper.applyCountMarker = (...args) => calls.push(['count', ...args]);
   MarkerVisualHelper.applyBackgroundImage = (...args) => calls.push(['bg', ...args]);
   IconUrlProvider.getGuestServiceIconUrl = (type) => `gs-${type}`;

   try {
      const markerEl = _markerEl();
      MarkerTypeRendererFactory.renderGuestServiceMarker(markerEl, [
         { service_type: MarkerTypeRendererFactory.FIRST_AID_AND_FAMILY_CENTER_TYPE },
         { service_type: 'Info' },
      ]);
      assert.ok(calls.some(([kind]) => kind === 'count'));
      assert.ok(calls.some((entry) => (
         entry[0] === 'class'
         && entry[2] === MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE.firstAidGuestService
      )));

      calls.length = 0;
      MarkerTypeRendererFactory.renderGuestServiceMarker(markerEl, [{ service_type: 'Info Desk' }]);
      assert.ok(calls.some((entry) => entry[0] === 'bg' && entry[2] === 'gs-Info Desk'));
   } finally {
      MarkerVisualHelper.applyMarkerClass = originalClass;
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerVisualHelper.applyBackgroundImage = originalBg;
      IconUrlProvider.getGuestServiceIconUrl = originalUrl;
   }
});

test('Test_RenderEventSiteMarker_TestSingleAndCount_ExpectVisuals', () => {
   const calls = [];
   const originalClass = MarkerVisualHelper.applyMarkerClass;
   const originalCount = MarkerVisualHelper.applyCountMarker;
   const originalBg = MarkerVisualHelper.applyBackgroundImage;
   const originalUrl = IconUrlProvider.getEventSiteIconUrl;

   MarkerVisualHelper.applyMarkerClass = (...args) => calls.push(['class', ...args]);
   MarkerVisualHelper.applyCountMarker = (...args) => calls.push(['count', ...args]);
   MarkerVisualHelper.applyBackgroundImage = (...args) => calls.push(['bg', ...args]);
   IconUrlProvider.getEventSiteIconUrl = (name) => `event-${name}`;

   try {
      const markerEl = _markerEl();
      MarkerTypeRendererFactory.renderEventSiteMarker(markerEl, [
         { name: 'Stage' },
         { name: 'Stage 2' },
      ]);
      assert.ok(calls.some(([kind]) => kind === 'count'));

      calls.length = 0;
      MarkerTypeRendererFactory.renderEventSiteMarker(markerEl, [{ name: 'Stage' }]);
      assert.ok(calls.some((entry) => entry[0] === 'bg' && entry[2] === 'event-Stage'));
   } finally {
      MarkerVisualHelper.applyMarkerClass = originalClass;
      MarkerVisualHelper.applyCountMarker = originalCount;
      MarkerVisualHelper.applyBackgroundImage = originalBg;
      IconUrlProvider.getEventSiteIconUrl = originalUrl;
   }
});
