import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSpeciesResultsView } from '../../../../../scripts/consoleOperations/animals/autocomplete/animalSpeciesResultsView.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createEls() {
   const inputEl = document.createElement('input');
   const resultsEl = document.createElement('div');
   const changes = [];

   inputEl.dispatchEvent = (event) => {
      changes.push(event.type);
      inputEl.listeners?.[event.type]?.(event);
   };

   return { inputEl, resultsEl, changes };
}

test('Test_CreateAnimalSpeciesResultsView_TestEmptyMatches_ExpectEmptyState', () => {
   const { inputEl, resultsEl } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });

   view.render([]);
   assert.equal(resultsEl.classList.contains('active'), true);
   assert.equal(resultsEl.children[0].className, 'console-operations-autocomplete-empty');
   assert.equal(resultsEl.children[0].textContent, Strings.common.noMatches);

   view.clear();
   assert.equal(resultsEl.classList.contains('active'), false);
   assert.equal(resultsEl.children.length, 0);
});

test('Test_CreateAnimalSpeciesResultsView_TestRenderAndSelect_ExpectInputChange', () => {
   const { inputEl, resultsEl, changes } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });

   view.render(['Lion', 'Tiger']);
   assert.equal(resultsEl.classList.contains('active'), true);
   assert.equal(resultsEl.children.length, 2);
   assert.equal(resultsEl.children[0].textContent, 'Lion');

   resultsEl.children[0].listeners.mousedown({ preventDefault() {} });
   resultsEl.children[0].click();

   assert.equal(inputEl.value, 'Lion');
   assert.deepEqual(changes, ['change']);
   assert.equal(resultsEl.classList.contains('active'), false);
});

test('Test_CreateAnimalSpeciesResultsView_TestKeydown_ExpectHighlightAndSelect', () => {
   const { inputEl, resultsEl, changes } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });

   view.render(['Lion', 'Tiger', 'Bear']);
   for (const child of resultsEl.children) {
      child.scrollIntoView = () => {};
   }

   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });
   assert.equal(resultsEl.children[0].classList.contains('is-highlighted'), true);

   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });
   assert.equal(resultsEl.children[1].classList.contains('is-highlighted'), true);

   view.handleKeydown({ key: 'ArrowUp', preventDefault() {} });
   assert.equal(resultsEl.children[0].classList.contains('is-highlighted'), true);

   view.handleKeydown({ key: 'Enter', preventDefault() {} });
   assert.equal(inputEl.value, 'Lion');
   assert.deepEqual(changes, ['change']);

   view.render(['Lion', 'Tiger']);
   for (const child of resultsEl.children) {
      child.scrollIntoView = () => {};
   }
   view.handleKeydown({ key: 'Escape' });
   assert.equal(resultsEl.classList.contains('active'), false);

   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });
});
