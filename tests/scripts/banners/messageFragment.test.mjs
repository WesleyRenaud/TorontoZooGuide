import assert from 'node:assert/strict';
import test from 'node:test';

import { MessageFragment } from '../../../scripts/banners/messageFragment.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_CreateSingleMessageBanner_TestSyncAndHide_ExpectVisibility', () => {
   const banner = MessageFragment.createSingleMessageBanner((item) => item?.closed_message);
   const beforeCount = document.body.children.length;

   banner.sync({});
   assert.equal(document.body.children.length, beforeCount);

   banner.sync({ closed_message: 'Closed today' });
   const el = document.body.children.at(-1);
   assert.equal(el.className, 'off-display-closed-banner');
   assert.equal(el.style.display, 'flex');
   assert.match(el.textContent, /Closed today/);

   banner.hide();
   assert.equal(el.style.display, 'none');
});
