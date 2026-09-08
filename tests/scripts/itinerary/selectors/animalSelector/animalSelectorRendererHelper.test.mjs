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

test('Test_CreateLikelihoodWarning_TestLevels_ExpectWarningOrNull', () => {
   assert.equal(AnimalSelectorRendererHelper.createLikelihoodWarning(''), null);

   const low = AnimalSelectorRendererHelper.createLikelihoodWarning('low');
   assert.equal(low.className, 'itin-likelihood-warning low');
   assert.equal(low.title, Strings.itinerary.selectors.lowVisibilityHint);

   const medium = AnimalSelectorRendererHelper.createLikelihoodWarning('medium');
   assert.equal(medium.title, Strings.itinerary.confirmation.animalMayBeOffDisplay);
});
