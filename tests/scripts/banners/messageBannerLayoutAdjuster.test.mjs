import assert from 'node:assert/strict';
import test from 'node:test';

import { MessageBannerLayoutAdjuster } from '../../../scripts/banners/messageBannerLayoutAdjuster.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}

function _createBannerElement({ height = 200, offsetHeight } = {}) {
   const el = document.createElement('div');
   el.getBoundingClientRect = () => ({ height });
   Object.defineProperty(el, 'offsetHeight', {
      configurable: true,
      get: () => (offsetHeight != null ? offsetHeight : height),
   });
   el.style.removeProperty = (name) => {
      delete el.style[name];
   };
   return el;
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_CreateWarningIcon_TestDefaults_ExpectSvg', () => {
   const icon = MessageBannerLayoutAdjuster.createWarningIcon();
   assert.equal(icon.namespaceURI, MessageBannerLayoutAdjuster.SVG_NS);
   assert.equal(icon.getAttribute('class'), 'off-display-warning-icon');
   assert.equal(icon.children.length, 3);
});

test('Test_GetDesktopWidthRange_TestViewport_ExpectClamped', () => {
   window.innerWidth = 800;
   const range = MessageBannerLayoutAdjuster.getDesktopWidthRange();
   assert.equal(range.min <= range.max, true);
   assert.ok(range.max <= 800 - MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER);
});

test('Test_GetDesktopWidthRange_TestMissingViewport_ExpectMaxFallback', () => {
   delete window.innerWidth;
   const range = MessageBannerLayoutAdjuster.getDesktopWidthRange();
   assert.equal(range.max, MessageBannerLayoutAdjuster.ALERT_MAX_WIDTH);
});

test('Test_SetBannerWidth_TestElement_ExpectCssVar', () => {
   const el = document.createElement('div');
   MessageBannerLayoutAdjuster.setBannerWidth(el, 640.4);
   assert.equal(el.style['--alert-banner-width'], '640px');
});

test('Test_IsMobileAlertLayout_TestMatchMedia_ExpectMatches', () => {
   window.matchMedia = () => ({ matches: true });
   assert.equal(MessageBannerLayoutAdjuster.isMobileAlertLayout(), true);

   window.matchMedia = () => ({ matches: false });
   assert.equal(MessageBannerLayoutAdjuster.isMobileAlertLayout(), false);

   delete window.matchMedia;
   assert.equal(MessageBannerLayoutAdjuster.isMobileAlertLayout(), false);
});

test('Test_GetMeasuredHeight_TestRectAndOffset_ExpectHeight', () => {
   const withRect = _createBannerElement({ height: 120 });
   assert.equal(MessageBannerLayoutAdjuster.getMeasuredHeight(withRect), 120);

   const withOffset = _createBannerElement({ height: 0, offsetHeight: 88 });
   assert.equal(MessageBannerLayoutAdjuster.getMeasuredHeight(withOffset), 88);

   const empty = _createBannerElement({ height: 0, offsetHeight: 0 });
   assert.equal(MessageBannerLayoutAdjuster.getMeasuredHeight(empty), 0);
});

test('Test_GetWidthToHeightRatio_TestHeightPresentAndMissing_ExpectRatioOrNull', () => {
   const el = _createBannerElement({ height: 100 });
   assert.equal(MessageBannerLayoutAdjuster.getWidthToHeightRatio(el, 200), 2);

   const empty = _createBannerElement({ height: 0, offsetHeight: 0 });
   assert.equal(MessageBannerLayoutAdjuster.getWidthToHeightRatio(empty, 200), null);
});

test('Test_AdjustBannerWidth_TestMobile_ExpectClearsWidth', () => {
   window.matchMedia = () => ({ matches: true });
   const el = _createBannerElement();
   el.style['--alert-banner-width'] = '700px';

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   assert.equal(el.style['--alert-banner-width'], undefined);
});

test('Test_AdjustBannerWidth_TestZeroMax_ExpectClearsWidth', () => {
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER;
   const el = _createBannerElement();
   el.style['--alert-banner-width'] = '700px';

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   assert.equal(el.style['--alert-banner-width'], undefined);
});

test('Test_AdjustBannerWidth_TestMinEqualsMax_ExpectSetsMax', () => {
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = MessageBannerLayoutAdjuster.ALERT_MIN_WIDTH
      + MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER;
   const el = _createBannerElement({ height: 100 });

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   assert.equal(
      el.style['--alert-banner-width'],
      `${MessageBannerLayoutAdjuster.ALERT_MIN_WIDTH}px`
   );
});

test('Test_AdjustBannerWidth_TestNullMinRatio_ExpectEarlyReturn', () => {
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = 1200;
   const el = _createBannerElement({ height: 0, offsetHeight: 0 });

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   assert.equal(
      el.style['--alert-banner-width'],
      `${MessageBannerLayoutAdjuster.ALERT_MIN_WIDTH}px`
   );
});

test('Test_AdjustBannerWidth_TestMinRatioAlreadyWide_ExpectSetsMin', () => {
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = 1200;
   const el = _createBannerElement({ height: 200 });

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   assert.equal(
      el.style['--alert-banner-width'],
      `${MessageBannerLayoutAdjuster.ALERT_MIN_WIDTH}px`
   );
});

test('Test_AdjustBannerWidth_TestMaxRatioStillNarrow_ExpectSetsMax', () => {
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = 1200;
   const el = _createBannerElement({ height: 900 });
   const expectedMax = 1200 - MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER;

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   assert.equal(el.style['--alert-banner-width'], `${expectedMax}px`);
});

test('Test_AdjustBannerWidth_TestNullMaxRatio_ExpectSetsMax', () => {
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = 1200;
   const el = document.createElement('div');
   el.style.removeProperty = (name) => {
      delete el.style[name];
   };
   let callCount = 0;
   el.getBoundingClientRect = () => {
      callCount += 1;
      if (callCount === 1) {
         return { height: 400 };
      }
      return { height: 0 };
   };
   Object.defineProperty(el, 'offsetHeight', {
      configurable: true,
      get: () => 0,
   });

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   assert.equal(
      el.style['--alert-banner-width'],
      `${1200 - MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER}px`
   );
});

test('Test_AdjustBannerWidth_TestSearchSteps_ExpectBinarySearchWidth', () => {
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = 1200;
   const el = _createBannerElement({ height: 400 });

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   const width = Number.parseFloat(el.style['--alert-banner-width']);
   assert.ok(width > MessageBannerLayoutAdjuster.ALERT_MIN_WIDTH);
   assert.ok(width <= 1200 - MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER);
   assert.ok(Math.abs(width / 400 - MessageBannerLayoutAdjuster.ALERT_WIDTH_TO_HEIGHT_RATIO) < 0.05);
});

test('Test_AdjustBannerWidth_TestNullMidRatio_ExpectEarlyReturn', () => {
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = 1200;
   const el = document.createElement('div');
   el.style.removeProperty = (name) => {
      delete el.style[name];
   };
   let callCount = 0;
   el.getBoundingClientRect = () => {
      callCount += 1;
      if (callCount <= 2) {
         return { height: 400 };
      }
      return { height: 0 };
   };
   Object.defineProperty(el, 'offsetHeight', {
      configurable: true,
      get: () => 0,
   });

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   assert.ok(callCount >= 3);
});
