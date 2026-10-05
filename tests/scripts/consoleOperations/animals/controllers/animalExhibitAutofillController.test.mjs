import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalExhibitAutofillController } from '../../../../../scripts/consoleOperations/animals/controllers/animalExhibitAutofillController.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createSelect(options = []) {
   const selectEl = document.createElement('select');
   options.forEach((name) => {
      const optionEl = document.createElement('option');
      optionEl.value = name;
      optionEl.textContent = name;
      selectEl.appendChild(optionEl);
   });
   return selectEl;
}

function _populateExhibits(targetEl, exhibits) {
   targetEl.replaceChildren();
   exhibits.forEach((name) => {
      const optionEl = document.createElement('option');
      optionEl.value = name;
      optionEl.textContent = name;
      targetEl.appendChild(optionEl);
   });
}


test('Test_CreateAnimalExhibitAutofillController_TestUniqueSpecies_ExpectSetsExhibitWithoutClearingSpecies', async () => {
   const africanLion = 'African Lion';
   const africaSavanna = 'Africa Savanna';
   const eurasiaWilds = 'Eurasia Wilds';
   const uniqueExhibits = [africaSavanna];
   const populated = [];
   const uniqueFills = [];
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect([africaSavanna, eurasiaWilds]);
   speciesEl.value = africanLion;
   exhibitEl.value = '';

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => [africaSavanna, eurasiaWilds],
      loadExhibitsForSpecies: async (species) => {
         assert.equal(species, africanLion);
         return uniqueExhibits;
      },
      populateExhibits: (targetEl, exhibits) => {
         populated.push({ targetEl, exhibits });
         _populateExhibits(targetEl, exhibits);
      },
      onUniqueFill: () => {
         uniqueFills.push(true);
      },
   });

   await speciesEl.listeners.change();

   assert.equal(populated.length, uniqueFills.length);
   assert.deepEqual(populated[Position.FIRST].exhibits, uniqueExhibits);
   assert.equal(exhibitEl.value, africaSavanna);
   assert.equal(speciesEl.value, africanLion);
   assert.deepEqual(uniqueFills, [true]);
});


test('Test_CreateAnimalExhibitAutofillController_TestMultipleExhibits_ExpectNarrowsAndLeavesEmpty', async () => {
   const eurasiaWilds = 'Eurasia Wilds';
   const canadianDomain = 'Canadian Domain';
   const exhibits = [eurasiaWilds, canadianDomain];
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(['Africa Savanna']);
   speciesEl.value = 'Bactrian Camel';
   exhibitEl.value = '';

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => ['Africa Savanna', eurasiaWilds],
      loadExhibitsForSpecies: async () => exhibits,
      populateExhibits: _populateExhibits,
   });

   await speciesEl.listeners.change();

   assert.equal(exhibitEl.value, '');
   assert.equal(exhibitEl.children.length, exhibits.length);
   assert.equal(exhibitEl.children[Position.FIRST].value, eurasiaWilds);
   assert.equal(exhibitEl.children[Position.SECOND].value, canadianDomain);
});


test('Test_CreateAnimalExhibitAutofillController_TestSelectedExhibitMultipleExhibits_ExpectNarrowsAndKeepsSelection', async () => {
   const africaSavanna = 'Africa Savanna';
   const speciesExhibits = [africaSavanna, 'African Rainforest Pavilion', 'Kids Zoo'];
   const uniqueFills = [];
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect([africaSavanna, 'Eurasia Wilds']);
   speciesEl.value = 'Marabou Stork';
   exhibitEl.value = africaSavanna;

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => [africaSavanna, 'Eurasia Wilds'],
      loadExhibitsForSpecies: async () => speciesExhibits,
      populateExhibits: _populateExhibits,
      onUniqueFill: () => {
         uniqueFills.push(true);
      },
   });

   await speciesEl.listeners.change();

   assert.equal(exhibitEl.value, africaSavanna);
   assert.deepEqual(
      exhibitEl.children.map((optionEl) => optionEl.value),
      speciesExhibits
   );
   assert.deepEqual(uniqueFills, []);
});


test('Test_CreateAnimalExhibitAutofillController_TestEmptySpecies_ExpectRestoresExhibitListAndKeepsSelection', async () => {
   const africaSavanna = 'Africa Savanna';
   const eurasiaWilds = 'Eurasia Wilds';
   const exhibits = [africaSavanna, eurasiaWilds];
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect([eurasiaWilds]);
   speciesEl.value = '';
   exhibitEl.value = eurasiaWilds;

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => exhibits,
      loadExhibitsForSpecies: async () => {
         assert.fail('should not load exhibits for species');
      },
      populateExhibits: _populateExhibits,
   });

   await speciesEl.listeners.change();

   assert.equal(exhibitEl.value, eurasiaWilds);
   assert.equal(exhibitEl.children.length, exhibits.length);
   assert.equal(exhibitEl.children[Position.FIRST].value, africaSavanna);
   assert.equal(exhibitEl.children[Position.SECOND].value, eurasiaWilds);
});


test('Test_CreateAnimalExhibitAutofillController_TestClearSpeciesInput_ExpectKeepsExhibitUntilBlank', async () => {
   const africanLion = 'African Lion';
   const africaSavanna = 'Africa Savanna';
   const eurasiaWilds = 'Eurasia Wilds';
   const exhibits = [africaSavanna, eurasiaWilds];
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(exhibits);
   speciesEl.value = africanLion;
   exhibitEl.value = africaSavanna;
   const populated = [];

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => exhibits,
      loadExhibitsForSpecies: async () => {
         assert.fail('should not load exhibits for species');
      },
      populateExhibits: (targetEl, nextExhibits) => {
         populated.push(nextExhibits);
         _populateExhibits(targetEl, nextExhibits);
      },
   });

   await speciesEl.listeners.input();

   assert.equal(exhibitEl.value, africaSavanna);
   assert.equal(populated.length, 0);
});


test('Test_CreateAnimalExhibitAutofillController_TestClearSpeciesInput_ExpectRestoresListAndKeepsExhibit', async () => {
   const africanLion = 'African Lion';
   const africaSavanna = 'Africa Savanna';
   const eurasiaWilds = 'Eurasia Wilds';
   const exhibits = [africaSavanna, eurasiaWilds];
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(exhibits);
   speciesEl.value = africanLion;
   exhibitEl.value = africaSavanna;
   const populated = [];

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => exhibits,
      loadExhibitsForSpecies: async () => {
         assert.fail('should not load exhibits for species');
      },
      populateExhibits: (targetEl, nextExhibits) => {
         populated.push(nextExhibits);
         _populateExhibits(targetEl, nextExhibits);
      },
   });

   speciesEl.value = '';
   await speciesEl.listeners.input();

   assert.equal(exhibitEl.value, africaSavanna);
   assert.equal(populated.length, 1);
   assert.deepEqual(populated[Position.FIRST], exhibits);
});


test('Test_CreateAnimalExhibitAutofillController_TestManualExhibitChange_ExpectKeepsSpecies', () => {
   const lesserKudu = 'Lesser Kudu';
   const africaSavanna = 'Africa Savanna';
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect([africaSavanna, 'Eurasia Wilds']);
   speciesEl.value = lesserKudu;
   exhibitEl.value = africaSavanna;

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => [],
      loadExhibitsForSpecies: async () => [],
      populateExhibits: () => {},
   });

   exhibitEl.dispatchEvent(new Event('change'));

   assert.equal(speciesEl.value, lesserKudu);
   assert.equal(exhibitEl.value, africaSavanna);
});


test('Test_CreateAnimalExhibitAutofillController_TestNoMatches_ExpectEmptyExhibit', async () => {
   const africanLion = 'African Lion';
   const africaSavanna = 'Africa Savanna';
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect([africaSavanna]);
   speciesEl.value = africanLion;
   exhibitEl.value = '';

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => [africaSavanna, 'Eurasia Wilds'],
      loadExhibitsForSpecies: async () => [],
      populateExhibits: _populateExhibits,
   });

   await speciesEl.listeners.change();

   assert.equal(exhibitEl.value, '');
   assert.equal(exhibitEl.children.length, 0);
});


test('Test_CreateAnimalExhibitAutofillController_TestMissingFields_ExpectNoop', async () => {
   const control = AnimalExhibitAutofillController.createAnimalExhibitAutofillController({});

   await control.applySpecies();
});


test('Test_CreateAnimalExhibitAutofillController_TestSpeciesLoadThrows_ExpectKeepsExhibit', async () => {
   const africanLion = 'African Lion';
   const africaSavanna = 'Africa Savanna';
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect([africaSavanna]);
   speciesEl.value = africanLion;
   exhibitEl.value = africaSavanna;

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => {
         throw new Error('full list failed');
      },
      loadExhibitsForSpecies: async () => {
         throw new Error('species list failed');
      },
      populateExhibits: () => {
         assert.fail('should not populate');
      },
   });

   await speciesEl.listeners.change();

   assert.equal(exhibitEl.value, africaSavanna);
});


test('Test_CreateAnimalExhibitAutofillController_TestEmptySpeciesLoadThrows_ExpectKeepsExhibit', async () => {
   const africaSavanna = 'Africa Savanna';
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect([africaSavanna]);
   speciesEl.value = '';
   exhibitEl.value = africaSavanna;

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => {
         throw new Error('full list failed');
      },
      loadExhibitsForSpecies: async () => {
         throw new Error('species list failed');
      },
      populateExhibits: () => {
         assert.fail('should not populate');
      },
   });

   await speciesEl.listeners.change();

   assert.equal(exhibitEl.value, africaSavanna);
});
