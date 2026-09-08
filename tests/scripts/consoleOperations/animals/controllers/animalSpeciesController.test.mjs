import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSpeciesController } from '../../../../../scripts/consoleOperations/animals/controllers/animalSpeciesController.js';
import { AnimalSpeciesAutocompleteHelper } from '../../../../../scripts/consoleOperations/animals/controllers/animalSpeciesAutocompleteHelper.js';
import { AnimalSpeciesResultsView } from '../../../../../scripts/consoleOperations/animals/autocomplete/animalSpeciesResultsView.js';
import { SpeciesMatcher } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesMatcher.js';
import { SpeciesProvider } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesProvider.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { ValueNormalizer } from '../../../../../scripts/api/valueNormalizer.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateAnimalSpeciesAutocompleteController_TestMissingEls_ExpectNoopClear', () => {
   const controller = AnimalSpeciesController.createAnimalSpeciesAutocompleteController({});
   assert.equal(typeof controller.clear, 'function');
   controller.clear();
});

test('Test_CreateAnimalSpeciesAutocompleteController_TestSearchAndEvents_ExpectResults', async () => {
   const originalSource = SpeciesProvider.createAnimalSpeciesSource;
   const originalResultsView = AnimalSpeciesResultsView.createAnimalSpeciesResultsView;
   const originalFilter = SpeciesMatcher.filterSpeciesMatches;
   const originalDebounce = AnimalSpeciesAutocompleteHelper.debounce;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalTrim = ValueNormalizer.asTrimmedString;
   const renders = [];
   const clears = [];
   const keydowns = [];
   let loadCalls = 0;

   SpeciesProvider.createAnimalSpeciesSource = () => ({
      loadForExhibit: async () => {
         loadCalls += 1;
         return [{ species: 'Lion' }];
      },
   });
   AnimalSpeciesResultsView.createAnimalSpeciesResultsView = () => ({
      clear: () => { clears.push(true); },
      render: (matches) => { renders.push(matches); },
      handleKeydown: (event) => { keydowns.push(event); },
   });
   SpeciesMatcher.filterSpeciesMatches = (list, query) => list.filter((row) => row.species.includes(query));
   AnimalSpeciesAutocompleteHelper.debounce = (fn) => fn;
   ControllerHelper.getFieldValue = () => 'Savanna';
   ValueNormalizer.asTrimmedString = (value) => String(value || '').trim();

   try {
      const inputEl = document.createElement('input');
      const resultsEl = document.createElement('div');
      const exhibitEl = document.createElement('select');

      const controller = AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl,
         exhibitEl,
      });

      inputEl.value = '';
      inputEl.listeners.input();
      assert.ok(clears.length >= 1);

      inputEl.value = 'Li';
      await inputEl.listeners.input();
      assert.equal(loadCalls, 1);
      assert.deepEqual(renders.at(-1), [{ species: 'Lion' }]);

      inputEl.listeners.focus();
      assert.equal(loadCalls, 2);

      inputEl.listeners.keydown({ key: 'ArrowDown' });
      assert.equal(keydowns.length, 1);

      clears.length = 0;
      inputEl.listeners.blur();
      await new Promise((resolve) => setTimeout(resolve, 160));
      assert.ok(clears.length >= 1);

      inputEl.value = 'keep';
      clears.length = 0;
      exhibitEl.listeners.change();
      assert.equal(inputEl.value, '');
      assert.ok(clears.length >= 1);

      controller.clear();
   } finally {
      SpeciesProvider.createAnimalSpeciesSource = originalSource;
      AnimalSpeciesResultsView.createAnimalSpeciesResultsView = originalResultsView;
      SpeciesMatcher.filterSpeciesMatches = originalFilter;
      AnimalSpeciesAutocompleteHelper.debounce = originalDebounce;
      ControllerHelper.getFieldValue = originalGetField;
      ValueNormalizer.asTrimmedString = originalTrim;
   }
});
