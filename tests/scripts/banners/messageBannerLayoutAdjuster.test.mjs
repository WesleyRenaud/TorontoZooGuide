import assert from 'node:assert/strict';
import test from 'node:test';

import { MessageBannerLayoutAdjuster } from '../../../scripts/banners/messageBannerLayoutAdjuster.js';
import { Position } from '../../../scripts/shared/enums/position.js';
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
   assert.equal(icon.children.length, Position.FOURTH);
});


test('Test_CreateSnowflakeIcon_TestDefaults_ExpectSvg', () => {
   const icon = MessageBannerLayoutAdjuster.createSnowflakeIcon();

   assert.equal(icon.namespaceURI, MessageBannerLayoutAdjuster.SVG_NS);
   assert.equal(icon.getAttribute('class'), 'off-display-snowflake-icon');
   assert.equal(icon.children[0].getAttribute('d'), MessageBannerLayoutAdjuster.SNOWFLAKE_PATH);
});


test('Test_GetDesktopWidthRange_TestViewport_ExpectClamped', () => {
   const viewportWidth = 800;
   window.innerWidth = viewportWidth;

   const range = MessageBannerLayoutAdjuster.getDesktopWidthRange();

   assert.equal(range.min <= range.max, true);
   assert.ok(range.max <= viewportWidth - MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER);
});


test('Test_GetDesktopWidthRange_TestMissingViewport_ExpectMaxFallback', () => {
   delete window.innerWidth;

   const range = MessageBannerLayoutAdjuster.getDesktopWidthRange();

   assert.equal(range.max, MessageBannerLayoutAdjuster.ALERT_MAX_WIDTH);
});


test('Test_SetBannerWidth_TestElement_ExpectCssVar', () => {
   const el = document.createElement('div');
   const width = 640.4;

   MessageBannerLayoutAdjuster.setBannerWidth(el, width);

   assert.equal(el.style['--alert-banner-width'], `${Math.round(width)}px`);
});


test('Test_IsMobileAlertLayout_TestMatchMediaTrue_ExpectTrue', () => {
   window.matchMedia = () => ({ matches: true });

   const isMobile = MessageBannerLayoutAdjuster.isMobileAlertLayout();

   assert.equal(isMobile, true);
});


test('Test_IsMobileAlertLayout_TestMatchMediaFalse_ExpectFalse', () => {
   window.matchMedia = () => ({ matches: false });

   const isMobile = MessageBannerLayoutAdjuster.isMobileAlertLayout();

   assert.equal(isMobile, false);
});


test('Test_IsMobileAlertLayout_TestMissingMatchMedia_ExpectFalse', () => {
   delete window.matchMedia;

   const isMobile = MessageBannerLayoutAdjuster.isMobileAlertLayout();

   assert.equal(isMobile, false);
});


test('Test_GetMeasuredHeight_TestRect_ExpectHeight', () => {
   const height = 120;
   const el = _createBannerElement({ height });

   const measured = MessageBannerLayoutAdjuster.getMeasuredHeight(el);

   assert.equal(measured, height);
});


test('Test_GetMeasuredHeight_TestOffset_ExpectOffsetHeight', () => {
   const offsetHeight = 88;
   const el = _createBannerElement({ height: 0, offsetHeight });

   const measured = MessageBannerLayoutAdjuster.getMeasuredHeight(el);

   assert.equal(measured, offsetHeight);
});


test('Test_GetMeasuredHeight_TestEmpty_ExpectZero', () => {
   const el = _createBannerElement({ height: 0, offsetHeight: 0 });

   const measured = MessageBannerLayoutAdjuster.getMeasuredHeight(el);

   assert.equal(measured, 0);
});


test('Test_GetWidthToHeightRatio_TestHeightPresent_ExpectRatio', () => {
   const height = 100;
   const width = 200;
   const el = _createBannerElement({ height });

   const ratio = MessageBannerLayoutAdjuster.getWidthToHeightRatio(el, width);

   assert.equal(ratio, width / height);
});


test('Test_GetWidthToHeightRatio_TestMissingHeight_ExpectNull', () => {
   const width = 200;
   const el = _createBannerElement({ height: 0, offsetHeight: 0 });

   const ratio = MessageBannerLayoutAdjuster.getWidthToHeightRatio(el, width);

   assert.equal(ratio, null);
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
   const viewportWidth = 1200;
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = viewportWidth;
   const el = _createBannerElement({ height: 900 });

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);

   assert.equal(
      el.style['--alert-banner-width'],
      `${viewportWidth - MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER}px`
   );
});


test('Test_AdjustBannerWidth_TestNullMaxRatio_ExpectSetsMax', () => {
   const viewportWidth = 1200;
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = viewportWidth;
   const el = document.createElement('div');
   el.style.removeProperty = (name) => {
      delete el.style[name];
   };
   let callCount = 0;
   el.getBoundingClientRect = () => {
      callCount += 1;
      if (callCount === Position.SECOND) {
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
      `${viewportWidth - MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER}px`
   );
});


test('Test_AdjustBannerWidth_TestSearchSteps_ExpectBinarySearchWidth', () => {
   const viewportWidth = 1200;
   const height = 400;
   window.matchMedia = () => ({ matches: false });
   window.innerWidth = viewportWidth;
   const el = _createBannerElement({ height });

   MessageBannerLayoutAdjuster.adjustBannerWidth(el);
   const width = Number.parseFloat(el.style['--alert-banner-width']);

   assert.ok(width > MessageBannerLayoutAdjuster.ALERT_MIN_WIDTH);
   assert.ok(width <= viewportWidth - MessageBannerLayoutAdjuster.ALERT_VIEWPORT_GUTTER);
   assert.ok(Math.abs(width / height - MessageBannerLayoutAdjuster.ALERT_WIDTH_TO_HEIGHT_RATIO) < 0.05);
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

   assert.ok(callCount >= Position.FOURTH);
});
