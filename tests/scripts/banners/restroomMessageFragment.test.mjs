import assert from 'node:assert/strict';
import test from 'node:test';

import { RestroomMessageFragment } from '../../../scripts/banners/restroomMessageFragment.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_CreateRestroomMessageBanner_TestAlertFallback_ExpectShown', () => {
   const banner = RestroomMessageFragment.createRestroomMessageBanner();
   banner.sync({ alert_message: 'Out of order' });
   assert.match(document.body.children.at(-1).textContent, /Out of order/);
});
