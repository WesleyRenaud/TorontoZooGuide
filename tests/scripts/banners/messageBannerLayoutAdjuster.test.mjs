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

test('Test_SetBannerWidth_TestElement_ExpectCssVar', () => {
   const el = document.createElement('div');
   MessageBannerLayoutAdjuster.setBannerWidth(el, 640.4);
   assert.equal(el.style['--alert-banner-width'], '640px');
});
