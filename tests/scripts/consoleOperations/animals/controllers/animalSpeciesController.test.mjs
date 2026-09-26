import assert from 'node:assert/strict';
import test from 'node:test';

import { ValueNormalizer } from '../../../../../scripts/api/valueNormalizer.js';
import { AnimalSpeciesResultsView } from '../../../../../scripts/consoleOperations/animals/autocomplete/animalSpeciesResultsView.js';
import { SpeciesMatcher } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesMatcher.js';
import { SpeciesProvider } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesProvider.js';
import { AnimalSpeciesAutocompleteHelper } from '../../../../../scripts/consoleOperations/animals/controllers/animalSpeciesAutocompleteHelper.js';
import { AnimalSpeciesController } from '../../../../../scripts/consoleOperations/animals/controllers/animalSpeciesController.js';
import { ControllerHelper } from '../../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _restore(originals) {
   SpeciesProvider.createAnimalSpeciesSource = originals.source;
   AnimalSpeciesResultsView.createAnimalSpeciesResultsView = originals.resultsView;
   SpeciesMatcher.filterSpeciesMatches = originals.filter;
   AnimalSpeciesAutocompleteHelper.debounce = originals.debounce;
   ControllerHelper.getFieldValue = originals.getField;
   ValueNormalizer.asTrimmedString = originals.trim;
}

function _installAutocompleteStubs({
   renders = [],
   clears = [],
   keydowns = [],
   loadForExhibit = async () => [{ species: 'Lion' }],
} = {}) {
   const originals = {
      source: SpeciesProvider.createAnimalSpeciesSource,
      resultsView: AnimalSpeciesResultsView.createAnimalSpeciesResultsView,
      filter: SpeciesMatcher.filterSpeciesMatches,
      debounce: AnimalSpeciesAutocompleteHelper.debounce,
      getField: ControllerHelper.getFieldValue,
      trim: ValueNormalizer.asTrimmedString,
   };

   SpeciesProvider.createAnimalSpeciesSource = () => ({
      loadForExhibit,
   });
   AnimalSpeciesResultsView.createAnimalSpeciesResultsView = () => ({
      clear: () => {
         clears.push(true);
      },
      render: (matches) => {
         renders.push(matches);
      },
      handleKeydown: (event) => {
         keydowns.push(event);
      },
   });
   SpeciesMatcher.filterSpeciesMatches = (list, query) => (
      list.filter((row) => row.species.includes(query))
   );
   AnimalSpeciesAutocompleteHelper.debounce = (fn) => fn;
   ControllerHelper.getFieldValue = () => 'Savanna';
   ValueNormalizer.asTrimmedString = (value) => String(value || '').trim();

   return originals;
}


test('Test_CreateAnimalSpeciesAutocompleteController_TestMissingEls_ExpectNoopClear', () => {
   const controller = AnimalSpeciesController.createAnimalSpeciesAutocompleteController({});

   controller.clear();

   assert.equal(typeof controller.clear, 'function');
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestEmptyInput_ExpectCleared', () => {
   const clears = [];
   const originals = _installAutocompleteStubs({ clears });

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
      });
      inputEl.value = '';

      inputEl.listeners.input();

      assert.ok(clears.length >= 1);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestSearch_ExpectResults', async () => {
   const lion = 'Lion';
   const query = 'Li';
   const matches = [{ species: lion }];
   const renders = [];
   let loadCalls = 0;
   const originals = _installAutocompleteStubs({
      renders,
      loadForExhibit: async () => {
         loadCalls += 1;
         return matches;
      },
   });

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
      });
      inputEl.value = query;

      await inputEl.listeners.input();

      assert.equal(loadCalls, 1);
      assert.deepEqual(renders.at(Position.LAST), matches);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestFocus_ExpectReload', async () => {
   const matches = [{ species: 'Lion' }];
   const renders = [];
   let loadCalls = 0;
   const originals = _installAutocompleteStubs({
      renders,
      loadForExhibit: async () => {
         loadCalls += 1;
         return matches;
      },
   });

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
      });
      inputEl.value = 'Li';
      await inputEl.listeners.input();

      inputEl.listeners.focus();

      assert.equal(loadCalls, 2);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestKeydown_ExpectForwarded', () => {
   const keydowns = [];
   const originals = _installAutocompleteStubs({ keydowns });
   const event = { key: 'ArrowDown' };

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
      });

      inputEl.listeners.keydown(event);

      assert.equal(keydowns.length, 1);
      assert.equal(keydowns[Position.FIRST], event);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestBlur_ExpectCleared', async () => {
   const clears = [];
   const originals = _installAutocompleteStubs({ clears });

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
      });

      inputEl.listeners.blur();
      await new Promise((resolve) => setTimeout(resolve, 160));

      assert.ok(clears.length >= 1);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestExhibitChange_ExpectKeepsValueAndClears', () => {
   const keptValue = 'keep';
   const clears = [];
   const originals = _installAutocompleteStubs({ clears });

   try {
      const inputEl = document.createElement('input');
      const exhibitEl = document.createElement('select');
      const controller = AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl,
      });
      inputEl.value = keptValue;

      exhibitEl.listeners.change();
      controller.clear();

      assert.equal(inputEl.value, keptValue);
      assert.ok(clears.length >= 1);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestInjectedSpeciesSource_ExpectUsed', async () => {
   const lion = 'Lion';
   const query = 'Li';
   const originals = {
      source: SpeciesProvider.createAnimalSpeciesSource,
      resultsView: AnimalSpeciesResultsView.createAnimalSpeciesResultsView,
      filter: SpeciesMatcher.filterSpeciesMatches,
      debounce: AnimalSpeciesAutocompleteHelper.debounce,
      getField: ControllerHelper.getFieldValue,
      trim: ValueNormalizer.asTrimmedString,
   };
   const renders = [];
   let defaultSourceCalls = 0;
   let injectedLoads = 0;

   SpeciesProvider.createAnimalSpeciesSource = () => {
      defaultSourceCalls += 1;
      return { loadForExhibit: async () => [] };
   };
   AnimalSpeciesResultsView.createAnimalSpeciesResultsView = () => ({
      clear: () => {},
      render: (matches) => {
         renders.push(matches);
      },
      handleKeydown: () => {},
   });
   SpeciesMatcher.filterSpeciesMatches = (list) => list;
   AnimalSpeciesAutocompleteHelper.debounce = (fn) => fn;
   ControllerHelper.getFieldValue = () => 'Savanna';
   ValueNormalizer.asTrimmedString = (value) => String(value || '').trim();

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
         speciesSource: {
            loadForExhibit: async () => {
               injectedLoads += 1;
               return [lion];
            },
         },
      });
      inputEl.value = query;

      await inputEl.listeners.input();

      assert.equal(defaultSourceCalls, 0);
      assert.equal(injectedLoads, 1);
      assert.deepEqual(renders.at(Position.LAST), [lion]);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestEmptyFocus_ExpectIgnored', () => {
   let loadCalls = 0;
   const originals = _installAutocompleteStubs({
      loadForExhibit: async () => {
         loadCalls += 1;
         return [];
      },
   });

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
      });
      inputEl.value = '';

      inputEl.listeners.focus();

      assert.equal(loadCalls, 0);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestStaleSuccess_ExpectIgnored', async () => {
   const fresh = { species: 'Fresh' };
   const renders = [];
   let resolveSlow;
   let loadCalls = 0;
   const originals = _installAutocompleteStubs({
      renders,
      loadForExhibit: async () => {
         loadCalls += 1;
         if (loadCalls === 1) {
            await new Promise((resolve) => {
               resolveSlow = resolve;
            });
            return [{ species: 'Stale' }];
         }

         return [fresh];
      },
   });
   SpeciesMatcher.filterSpeciesMatches = (list) => list;

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
      });
      inputEl.value = 'Li';
      const staleSearch = inputEl.listeners.input();
      await inputEl.listeners.input();
      const renderCountAfterFresh = renders.length;
      resolveSlow();
      await staleSearch;

      assert.deepEqual(renders.at(Position.LAST), [fresh]);
      assert.equal(renders.length, renderCountAfterFresh);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestLookupError_ExpectCleared', async () => {
   const clears = [];
   const originals = _installAutocompleteStubs({
      clears,
      loadForExhibit: async () => {
         throw new Error('lookup failed');
      },
   });

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
      });
      inputEl.value = 'Er';

      await inputEl.listeners.input();

      assert.ok(clears.length >= 1);
   } finally {
      _restore(originals);
   }
});


test('Test_CreateAnimalSpeciesAutocompleteController_TestStaleError_ExpectIgnored', async () => {
   const ok = { species: 'Ok' };
   const renders = [];
   const clears = [];
   let resolveThrowing;
   let loadCalls = 0;
   const originals = _installAutocompleteStubs({
      renders,
      clears,
      loadForExhibit: async () => {
         loadCalls += 1;
         if (loadCalls === 1) {
            await new Promise((resolve) => {
               resolveThrowing = resolve;
            });
            throw new Error('stale failure');
         }

         return [ok];
      },
   });
   SpeciesMatcher.filterSpeciesMatches = (list) => list;

   try {
      const inputEl = document.createElement('input');
      AnimalSpeciesController.createAnimalSpeciesAutocompleteController({
         inputEl,
         resultsEl: document.createElement('div'),
         exhibitEl: document.createElement('select'),
      });
      inputEl.value = 'Er';
      const staleErrorSearch = inputEl.listeners.input();
      await inputEl.listeners.input();
      const clearCountAfterOk = clears.length;
      resolveThrowing();
      await staleErrorSearch;

      assert.deepEqual(renders.at(Position.LAST), [ok]);
      assert.equal(clears.length, clearCountAfterOk);
   } finally {
      _restore(originals);
   }
});
