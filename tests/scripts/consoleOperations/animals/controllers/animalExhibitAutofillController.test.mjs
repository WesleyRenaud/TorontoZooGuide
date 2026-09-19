import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalExhibitAutofillController } from '../../../../../scripts/consoleOperations/animals/controllers/animalExhibitAutofillController.js';
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

test('Test_CreateAnimalExhibitAutofillController_TestUniqueSpecies_ExpectSetsExhibitWithoutClearingSpecies', async () => {
   const populated = [];
   const uniqueFills = [];
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(['Africa Savanna', 'Eurasia Wilds']);
   speciesEl.value = 'African Lion';
   exhibitEl.value = '';

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => ['Africa Savanna', 'Eurasia Wilds'],
      loadExhibitsForSpecies: async (species) => {
         assert.equal(species, 'African Lion');
         return ['Africa Savanna'];
      },
      populateExhibits: (targetEl, exhibits) => {
         populated.push({ targetEl, exhibits });
         targetEl.replaceChildren();
         exhibits.forEach((name) => {
            const optionEl = document.createElement('option');
            optionEl.value = name;
            optionEl.textContent = name;
            targetEl.appendChild(optionEl);
         });
      },
      onUniqueFill: () => {
         uniqueFills.push(true);
      },
   });

   await speciesEl.listeners.change();

   assert.equal(populated.length, 1);
   assert.deepEqual(populated[0].exhibits, ['Africa Savanna']);
   assert.equal(exhibitEl.value, 'Africa Savanna');
   assert.equal(speciesEl.value, 'African Lion');
   assert.deepEqual(uniqueFills, [true]);
});

test('Test_CreateAnimalExhibitAutofillController_TestMultipleExhibits_ExpectNarrowsAndLeavesEmpty', async () => {
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(['Africa Savanna']);
   speciesEl.value = 'Bactrian Camel';

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => ['Africa Savanna', 'Eurasia Wilds'],
      loadExhibitsForSpecies: async () => ['Eurasia Wilds', 'Canadian Domain'],
      populateExhibits: (targetEl, exhibits) => {
         targetEl.replaceChildren();
         exhibits.forEach((name) => {
            const optionEl = document.createElement('option');
            optionEl.value = name;
            optionEl.textContent = name;
            targetEl.appendChild(optionEl);
         });
      },
   });

   await speciesEl.listeners.change();

   assert.equal(exhibitEl.value, '');
   assert.equal(exhibitEl.children.length, 2);
   assert.equal(exhibitEl.children[0].value, 'Eurasia Wilds');
   assert.equal(exhibitEl.children[1].value, 'Canadian Domain');
});

test('Test_CreateAnimalExhibitAutofillController_TestEmptySpecies_ExpectRestoresExhibitList', async () => {
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(['Eurasia Wilds']);
   speciesEl.value = '';
   exhibitEl.value = 'Eurasia Wilds';

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => ['Africa Savanna', 'Eurasia Wilds'],
      loadExhibitsForSpecies: async () => {
         assert.fail('should not load exhibits for species');
      },
      populateExhibits: (targetEl, exhibits) => {
         targetEl.replaceChildren();
         exhibits.forEach((name) => {
            const optionEl = document.createElement('option');
            optionEl.value = name;
            optionEl.textContent = name;
            targetEl.appendChild(optionEl);
         });
      },
   });

   await speciesEl.listeners.change();

   assert.equal(exhibitEl.value, '');
   assert.equal(exhibitEl.children.length, 2);
   assert.equal(exhibitEl.children[0].value, 'Africa Savanna');
   assert.equal(exhibitEl.children[1].value, 'Eurasia Wilds');
});

test('Test_CreateAnimalExhibitAutofillController_TestClearSpeciesInput_ExpectClearsExhibit', async () => {
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(['Africa Savanna', 'Eurasia Wilds']);
   speciesEl.value = 'African Lion';
   exhibitEl.value = 'Africa Savanna';
   const populated = [];

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => ['Africa Savanna', 'Eurasia Wilds'],
      loadExhibitsForSpecies: async () => {
         assert.fail('should not load exhibits for species');
      },
      populateExhibits: (targetEl, exhibits) => {
         populated.push(exhibits);
         targetEl.replaceChildren();
         exhibits.forEach((name) => {
            const optionEl = document.createElement('option');
            optionEl.value = name;
            optionEl.textContent = name;
            targetEl.appendChild(optionEl);
         });
      },
   });

   await speciesEl.listeners.input();
   assert.equal(exhibitEl.value, 'Africa Savanna');
   assert.equal(populated.length, 0);

   speciesEl.value = '';
   await speciesEl.listeners.input();

   assert.equal(exhibitEl.value, '');
   assert.equal(populated.length, 1);
   assert.deepEqual(populated[0], ['Africa Savanna', 'Eurasia Wilds']);
});

test('Test_CreateAnimalExhibitAutofillController_TestManualExhibitChange_ExpectKeepsSpecies', () => {
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(['Africa Savanna', 'Eurasia Wilds']);
   speciesEl.value = 'Lesser Kudu';
   exhibitEl.value = 'Africa Savanna';

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => [],
      loadExhibitsForSpecies: async () => [],
      populateExhibits: () => {},
   });

   exhibitEl.dispatchEvent(new Event('change'));
   assert.equal(speciesEl.value, 'Lesser Kudu');
   assert.equal(exhibitEl.value, 'Africa Savanna');
});

test('Test_CreateAnimalExhibitAutofillController_TestNoMatches_ExpectEmptyExhibit', async () => {
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(['Africa Savanna']);
   speciesEl.value = 'African Lion';
   exhibitEl.value = 'Africa Savanna';

   AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
      speciesEl,
      exhibitEl,
      loadExhibits: async () => ['Africa Savanna', 'Eurasia Wilds'],
      loadExhibitsForSpecies: async () => [],
      populateExhibits: (targetEl, exhibits) => {
         targetEl.replaceChildren();
         exhibits.forEach((name) => {
            const optionEl = document.createElement('option');
            optionEl.value = name;
            optionEl.textContent = name;
            targetEl.appendChild(optionEl);
         });
      },
   });

   await speciesEl.listeners.change();

   assert.equal(exhibitEl.value, '');
   assert.equal(exhibitEl.children.length, 0);
});

test('Test_CreateAnimalExhibitAutofillController_TestMissingFields_ExpectNoop', async () => {
   const control = AnimalExhibitAutofillController.createAnimalExhibitAutofillController({});
   await control.applySpecies();
});

test('Test_CreateAnimalExhibitAutofillController_TestLoadThrows_ExpectClearsExhibit', async () => {
   const speciesEl = document.createElement('input');
   const exhibitEl = _createSelect(['Africa Savanna']);
   speciesEl.value = 'African Lion';
   exhibitEl.value = 'Africa Savanna';

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
   assert.equal(exhibitEl.value, '');

   speciesEl.value = '';
   exhibitEl.value = 'Africa Savanna';
   await speciesEl.listeners.change();
   assert.equal(exhibitEl.value, '');
});
