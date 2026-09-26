import assert from 'node:assert/strict';
import { test } from 'node:test';

import { SelectorControllerView } from '../../../../scripts/itinerary/selectors/selectorControllerView.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateSelectorElements_TestShell_ExpectMappedParts', () => {
   const topTitle = 'Top title';
   const heading = 'Heading';
   const subtitle = 'Subtitle';

   const elements = SelectorControllerView.createSelectorElements({
      topTitle,
      h1: heading,
      subtitle,
   });

   assert.equal(elements.rootEl.className, 'itin-overlay');
   assert.equal(elements.rootEl.querySelector('.itin-top-title')?.textContent, topTitle);
   assert.equal(elements.bodyEl.querySelector('.itin-h1')?.textContent, heading);
   assert.equal(elements.bodyEl.querySelector('.itin-subtitle')?.textContent, subtitle);
   assert.equal(elements.inputEl.className, 'itin-search-input');
   assert.equal(elements.resultsEl.className, 'itin-results');
   assert.equal(elements.nextButtonEl.textContent, Strings.itinerary.actions.next);
   assert.equal(elements.finishButtonEl.textContent, Strings.itinerary.actions.finish);
   assert.equal(
      elements.closeButtonEl.getAttribute('aria-label'),
      Strings.itinerary.aria.closeBuilder
   );
});


test('Test_CreateSelectorElements_TestHideNext_ExpectNullNext', () => {
   const topTitle = 'Top title';
   const heading = 'Heading';
   const subtitle = 'Subtitle';

   const elements = SelectorControllerView.createSelectorElements({
      topTitle,
      h1: heading,
      subtitle,
      hideNextButton: true,
   });

   assert.equal(elements.nextButtonEl, null);
   assert.ok(elements.finishButtonEl);
});
