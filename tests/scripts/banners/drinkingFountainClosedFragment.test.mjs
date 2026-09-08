import assert from 'node:assert/strict';
import test from 'node:test';

import { DrinkingFountainClosedFragment } from '../../../scripts/banners/drinkingFountainClosedFragment.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_CreateDrinkingFountainClosedBanner_TestMessage_ExpectShown', () => {
   const banner = DrinkingFountainClosedFragment.createDrinkingFountainClosedBanner();
   banner.sync({ closed_message: 'Fountain closed' });
   assert.match(document.body.children.at(-1).textContent, /Fountain closed/);
});
