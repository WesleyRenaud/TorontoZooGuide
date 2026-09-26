import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelectorRendererHelper } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorRendererHelper.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}

installDomTestHooks({
   before() {
      document.createElementNS = (ns, tagName) => {
         const node = document.createElement(tagName);
         node.namespaceURI = ns;
         return node;
      };
   },
});


test('Test_CreateLikelihoodWarning_TestEmpty_ExpectNull', () => {
   const level = '';

   const warning = AnimalSelectorRendererHelper.createLikelihoodWarning(level);

   assert.equal(warning, null);
});


test('Test_CreateLikelihoodWarning_TestLow_ExpectLowHint', () => {
   const level = 'low';

   const warning = AnimalSelectorRendererHelper.createLikelihoodWarning(level);

   assert.equal(warning.className, `itin-likelihood-warning ${level}`);
   assert.equal(warning.title, Strings.itinerary.selectors.lowVisibilityHint);
});


test('Test_CreateLikelihoodWarning_TestMedium_ExpectOffDisplayTitle', () => {
   const level = 'medium';

   const warning = AnimalSelectorRendererHelper.createLikelihoodWarning(level);

   assert.equal(warning.title, Strings.itinerary.confirmation.animalMayBeOffDisplay);
});
