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
