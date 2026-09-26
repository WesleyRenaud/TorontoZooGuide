import assert from 'node:assert/strict';
import test from 'node:test';

import { RestroomMessageFragment } from '../../../scripts/banners/restroomMessageFragment.js';
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


test('Test_CreateRestroomMessageBanner_TestAlertFallback_ExpectShown', () => {
   const message = 'Out of order';
   const banner = RestroomMessageFragment.createRestroomMessageBanner();

   banner.sync({ alert_message: message });

   assert.match(document.body.children.at(Position.LAST).textContent, new RegExp(message));
});
