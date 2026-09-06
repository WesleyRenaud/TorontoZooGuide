import assert from 'node:assert/strict';
import { test } from 'node:test';

import { SelectorControllerElements } from '../../../../scripts/itinerary/selectors/selectorControllerElements.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

test.describe('createSelectorElements', () => {
   installDomTestHooks();

   test('Test_Builds_TestBuildsTheSelectorShellAndMapsElementReferences_ExpectOk', () => {
      const elements = SelectorControllerElements.createSelectorElements({
         topTitle: 'Top title',
         h1: 'Heading',
         subtitle: 'Subtitle',
      });

      assert.equal(elements.rootEl.className, 'itin-overlay');
      assert.equal(
         elements.rootEl.querySelector('.itin-top-title')?.textContent,
         'Top title'
      );
      assert.equal(
         elements.bodyEl.querySelector('.itin-h1')?.textContent,
         'Heading'
      );
      assert.equal(
         elements.bodyEl.querySelector('.itin-subtitle')?.textContent,
         'Subtitle'
      );
      assert.equal(elements.inputEl.className, 'itin-search-input');
      assert.equal(elements.resultsEl.className, 'itin-results');
      assert.equal(
         elements.nextButtonEl.textContent,
         Strings.itinerary.actions.next
      );
      assert.equal(
         elements.finishButtonEl.textContent,
         Strings.itinerary.actions.finish
      );
      assert.equal(
         elements.closeButtonEl.getAttribute('aria-label'),
         Strings.itinerary.aria.closeBuilder
      );
   });

   test('Test_Omits_TestOmitsTheNextButtonWhenHideNextButtonIsTrue_ExpectOk', () => {
      const elements = SelectorControllerElements.createSelectorElements({
         topTitle: 'Top title',
         h1: 'Heading',
         subtitle: 'Subtitle',
         hideNextButton: true,
      });

      assert.equal(elements.nextButtonEl, null);
      assert.ok(elements.finishButtonEl);
   });
});
