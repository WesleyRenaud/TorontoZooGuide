import assert from 'node:assert/strict';
import test from 'node:test';

import { OffDisplayFragment } from '../../../scripts/banners/offDisplayFragment.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_CreateOffDisplayBanner_TestMessages_ExpectCombined', () => {
   const banner = OffDisplayFragment.createOffDisplayBanner();
   banner.sync({
      off_display_message: 'Off display',
      limited_viewing_message: 'Limited viewing',
      viewing_alert_messages: ['Alert one', 'Alert two'],
   });
   const text = document.body.children.at(-1).textContent;
   assert.match(text, /Off display/);
   assert.match(text, /Limited viewing/);
   assert.match(text, /Alert one/);
});
