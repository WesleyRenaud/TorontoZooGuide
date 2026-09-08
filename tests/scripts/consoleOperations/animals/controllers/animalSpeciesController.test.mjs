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

test('Test_CreateAnimalSpeciesAutocompleteController_TestStaleErrorAndEmptyFocus_ExpectIgnored', async () => {
   const originalSource = SpeciesProvider.createAnimalSpeciesSource;
   const originalResultsView = AnimalSpeciesResultsView.createAnimalSpeciesResultsView;
   const originalFilter = SpeciesMatcher.filterSpeciesMatches;
   const originalDebounce = AnimalSpeciesAutocompleteHelper.debounce;
   const originalGetField = ControllerHelper.getFieldValue;
   const originalTrim = ValueNormalizer.asTrimmedString;
   const renders = [];
   const clears = [];
   let resolveSlow;
   let resolveThrowing;
   let loadCalls = 0;
   let mode = 'stale-success';

   SpeciesProvider.createAnimalSpeciesSource = () => ({
      loadForExhibit: async () => {
         loadCalls += 1;
         if (mode === 'stale-success') {
            if (loadCalls === 1) {
               await new Promise((resolve) => {
                  resolveSlow = resolve;
               });
               return [{ species: 'Stale' }];
            }
            return [{ species: 'Fresh' }];
         }

         if (mode === 'error') {
            throw new Error('lookup failed');
         }

         if (mode === 'stale-error' && loadCalls === 1) {
            await new Promise((resolve) => {
               resolveThrowing = resolve;
            });
            throw new Error('stale failure');
         }

         return [{ species: 'Ok' }];
      },
   });
   AnimalSpeciesResultsView.createAnimalSpeciesResultsView = () => ({
      clear: () => { clears.push(true); },
      render: (matches) => { renders.push(matches); },
      handleKeydown: () => {},
   });
   SpeciesMatcher.filterSpeciesMatches = (list) => list;
   AnimalSpeciesAutocompleteHelper.debounce = (fn) => fn;
   ControllerHelper.getFieldValue = () => 'Savanna';
   ValueNormalizer.asTrimmedString = (value) => String(value || '').trim();

   try {
      const inputEl = document.createElement('input');
      const resultsEl = document.createElement('div');
      const exhibitEl = document.createElement('select');

      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl,
         exhibitEl,
      });

      inputEl.value = '';
      inputEl.listeners.focus();
      assert.equal(loadCalls, 0);

      inputEl.value = 'Li';
      const staleSearch = inputEl.listeners.input();
      await inputEl.listeners.input();
      assert.deepEqual(renders.at(-1), [{ species: 'Fresh' }]);

      const renderCountAfterFresh = renders.length;
      resolveSlow();
      await staleSearch;
      assert.equal(renders.length, renderCountAfterFresh);

      mode = 'error';
      loadCalls = 0;
      clears.length = 0;
      inputEl.value = 'Er';
      await inputEl.listeners.input();
      assert.ok(clears.length >= 1);

      mode = 'stale-error';
      loadCalls = 0;
      const staleErrorSearch = inputEl.listeners.input();
      mode = 'ok-after-stale-error';
      await inputEl.listeners.input();
      const clearCountAfterOk = clears.length;
      resolveThrowing();
      await staleErrorSearch;
      assert.equal(clears.length, clearCountAfterOk);
   } finally {
      SpeciesProvider.createAnimalSpeciesSource = originalSource;
      AnimalSpeciesResultsView.createAnimalSpeciesResultsView = originalResultsView;
      SpeciesMatcher.filterSpeciesMatches = originalFilter;
      AnimalSpeciesAutocompleteHelper.debounce = originalDebounce;
      ControllerHelper.getFieldValue = originalGetField;
      ValueNormalizer.asTrimmedString = originalTrim;
   }
});
