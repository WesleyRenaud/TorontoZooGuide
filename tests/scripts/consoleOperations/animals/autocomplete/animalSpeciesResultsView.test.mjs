import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSpeciesResultsView } from '../../../../../scripts/consoleOperations/animals/autocomplete/animalSpeciesResultsView.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
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

   const emptyEl = resultsEl.children[Position.FIRST];
   assert.equal(resultsEl.classList.contains('active'), true);
   assert.equal(emptyEl.className, 'console-operations-autocomplete-empty');
   assert.equal(emptyEl.textContent, Strings.common.noMatches);
});


test('Test_CreateAnimalSpeciesResultsView_TestClear_ExpectInactive', () => {
   const { inputEl, resultsEl } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });
   view.render([]);

   view.clear();

   assert.equal(resultsEl.classList.contains('active'), false);
   assert.equal(resultsEl.children.length, 0);
});


test('Test_CreateAnimalSpeciesResultsView_TestRenderAndSelect_ExpectInputChange', () => {
   const lion = 'Lion';
   const tiger = 'Tiger';
   const matches = [lion, tiger];
   const { inputEl, resultsEl, changes } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });

   view.render(matches);
   const firstMatchEl = resultsEl.children[Position.FIRST];

   firstMatchEl.listeners.mousedown({ preventDefault() {} });
   firstMatchEl.click();

   assert.equal(firstMatchEl.textContent, lion);
   assert.equal(inputEl.value, lion);
   assert.deepEqual(changes, ['change']);
   assert.equal(resultsEl.classList.contains('active'), false);
});


test('Test_CreateAnimalSpeciesResultsView_TestArrowDown_ExpectFirstHighlighted', () => {
   const lion = 'Lion';
   const matches = [lion, 'Tiger', 'Bear'];
   const { inputEl, resultsEl } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });
   view.render(matches);
   for (const child of resultsEl.children) {
      child.scrollIntoView = () => {};
   }

   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });

   assert.equal(resultsEl.children[Position.FIRST].classList.contains('is-highlighted'), true);
});


test('Test_CreateAnimalSpeciesResultsView_TestArrowDownTwice_ExpectSecondHighlighted', () => {
   const matches = ['Lion', 'Tiger', 'Bear'];
   const { inputEl, resultsEl } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });
   view.render(matches);
   for (const child of resultsEl.children) {
      child.scrollIntoView = () => {};
   }

   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });
   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });

   assert.equal(resultsEl.children[Position.SECOND].classList.contains('is-highlighted'), true);
});


test('Test_CreateAnimalSpeciesResultsView_TestArrowUp_ExpectFirstHighlighted', () => {
   const matches = ['Lion', 'Tiger', 'Bear'];
   const { inputEl, resultsEl } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });
   view.render(matches);
   for (const child of resultsEl.children) {
      child.scrollIntoView = () => {};
   }

   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });
   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });
   view.handleKeydown({ key: 'ArrowUp', preventDefault() {} });

   assert.equal(resultsEl.children[Position.FIRST].classList.contains('is-highlighted'), true);
});


test('Test_CreateAnimalSpeciesResultsView_TestEnter_ExpectSelectsHighlighted', () => {
   const lion = 'Lion';
   const matches = [lion, 'Tiger', 'Bear'];
   const { inputEl, resultsEl, changes } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });
   view.render(matches);
   for (const child of resultsEl.children) {
      child.scrollIntoView = () => {};
   }
   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });

   view.handleKeydown({ key: 'Enter', preventDefault() {} });

   assert.equal(inputEl.value, lion);
   assert.deepEqual(changes, ['change']);
});


test('Test_CreateAnimalSpeciesResultsView_TestEscape_ExpectCleared', () => {
   const matches = ['Lion', 'Tiger'];
   const { inputEl, resultsEl } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });
   view.render(matches);
   for (const child of resultsEl.children) {
      child.scrollIntoView = () => {};
   }

   view.handleKeydown({ key: 'Escape' });

   assert.equal(resultsEl.classList.contains('active'), false);
});


test('Test_CreateAnimalSpeciesResultsView_TestArrowDownAfterEscape_ExpectNoHighlight', () => {
   const matches = ['Lion', 'Tiger'];
   const { inputEl, resultsEl } = _createEls();
   const view = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({ inputEl, resultsEl });
   view.render(matches);
   for (const child of resultsEl.children) {
      child.scrollIntoView = () => {};
   }
   view.handleKeydown({ key: 'Escape' });

   view.handleKeydown({ key: 'ArrowDown', preventDefault() {} });

   assert.equal(resultsEl.classList.contains('active'), false);
});
