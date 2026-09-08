import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionClosedFragment } from '../../../scripts/banners/attractionClosedFragment.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_CreateAttractionClosedBanner_TestMessage_ExpectShown', () => {
   const banner = AttractionClosedFragment.createAttractionClosedBanner();
   banner.sync({ closed_message: 'Carousel closed' });
   assert.match(document.body.children.at(-1).textContent, /Carousel closed/);
});
