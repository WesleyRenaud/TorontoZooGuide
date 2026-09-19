import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { AnimalViewingScopeController } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeController.js';
import { AnimalViewingScopeControlHelper } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeControlHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

const originalFetch = globalThis.fetch;

function _createField(value = '') {
   const listeners = {};

   return {
      value,
      id: 'offDisplayViewingScope',
      addEventListener(eventName, handler) {
         listeners[eventName] = handler;
      },
      trigger(eventName) {
         return listeners[eventName]?.();
      },
   };
}

function _createGrid() {
   const fieldEl = document.createElement('div');
   fieldEl.className = 'console-operations-field';
   const gridEl = document.createElement('div');
   gridEl.id = 'offDisplayViewingScope';
   fieldEl.appendChild(gridEl);
   return gridEl;
}

function _mockViewingScopesResponse(viewingScopes) {
   globalThis.fetch = async () => new Response(JSON.stringify({ viewingScopes }), {
      status: 200,
      headers: {
         'Content-Type': 'application/json',
      },
   });
}

afterEach(() => {
   globalThis.fetch = originalFetch;
});

test('Test_CreateAnimalViewingScopeControl_TestEnclosures_ExpectAllSelected', async () => {
   const speciesEl = _createField('Wood Bison');
   const exhibitEl = _createField('Canadian Domain');
   const viewingScopeEl = _createGrid();

   _mockViewingScopesResponse([
      { enclosureName: 'Male Herd', label: 'Male Herd' },
      { enclosureName: 'Female Herd', label: 'Female Herd' },
   ]);

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   assert.deepEqual(control.selectedEnclosureNames(), []);

   await speciesEl.trigger('change');

   assert.deepEqual(control.selectedEnclosureNames(), [ 'Male Herd', 'Female Herd' ]);
   assert.equal(viewingScopeEl.querySelectorAll('input[type="checkbox"]').length, 2);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      false
   );
});

test('Test_CreateAnimalViewingScopeControl_TestExhibitSelectedAfterSpecies_ExpectLoadsScopes', async () => {
   const speciesEl = _createField('Lesser Kudu');
   const exhibitEl = _createField('');
   const viewingScopeEl = _createGrid();

   _mockViewingScopesResponse([
      { enclosureName: 'Main', label: 'Main' },
      { enclosureName: 'Yard', label: 'Yard' },
   ]);

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   await speciesEl.trigger('change');
   assert.equal(viewingScopeEl.querySelectorAll('input[type="checkbox"]').length, 0);

   exhibitEl.value = 'Africa Savanna';
   await exhibitEl.trigger('change');

   assert.deepEqual(control.selectedEnclosureNames(), [ 'Main', 'Yard' ]);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      false
   );
});

test('Test_CreateAnimalViewingScopeControl_TestUnnamedEnclosure_ExpectMainSelected', async () => {
   const speciesEl = _createField('African Lion');
   const exhibitEl = _createField('Africa Savanna');
   const viewingScopeEl = _createGrid();

   _mockViewingScopesResponse([
      { enclosureName: '', label: 'Main' },
   ]);

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   await speciesEl.trigger('change');

   assert.deepEqual(control.selectedEnclosureNames(), [ '' ]);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      true
   );
});

test('Test_CreateAnimalViewingScopeControl_TestInjectedLoader_ExpectUsed', async () => {
   const speciesEl = _createField('Sumatran Orangutan');
   const exhibitEl = _createField('Indo-Malaya Pavilion');
   const viewingScopeEl = _createGrid();
   const payloads = [];

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      loadViewingScopes: async (payload) => {
         payloads.push(payload);
         return [
            { enclosureName: 'Indoor', label: 'Indoor' },
         ];
      },
   });

   await speciesEl.trigger('change');

   assert.deepEqual(payloads, [
      { species: 'Sumatran Orangutan', exhibit: 'Indo-Malaya Pavilion' },
   ]);
   assert.deepEqual(control.selectedEnclosureNames(), [ 'Indoor' ]);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      true
   );
});

test('Test_CreateAnimalViewingScopeControl_TestSingleClosedAmongMany_ExpectFieldVisible', async () => {
   const speciesEl = _createField('Sumatran Orangutan');
   const exhibitEl = _createField('Indo-Malaya Pavilion');
   const viewingScopeEl = _createGrid();

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      loadViewingScopes: async () => [
         { enclosureName: 'Indoor', label: 'Indoor' },
      ],
      loadAnimalViewingScopes: async () => [
         { enclosureName: 'Indoor', label: 'Indoor' },
         { enclosureName: 'Outdoor', label: 'Outdoor' },
      ],
   });

   await speciesEl.trigger('change');

   assert.deepEqual(control.selectedEnclosureNames(), [ 'Indoor' ]);
   assert.equal(viewingScopeEl.querySelectorAll('input[type="checkbox"]').length, 1);
   assert.equal(viewingScopeEl.textContent.includes('Indoor'), true);
   assert.equal(viewingScopeEl.textContent.includes('Outdoor'), false);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      false
   );
});

test('Test_CreateAnimalViewingScopeControl_TestMissingFieldsAndErrors_ExpectReset', async () => {
   const speciesEl = _createField('');
   const exhibitEl = _createField('');
   const viewingScopeEl = _createGrid();
   viewingScopeEl.appendChild(document.createElement('input'));

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   assert.equal(viewingScopeEl.children.length, 0);

   await control.refresh();
   assert.equal(viewingScopeEl.children.length, 0);

   AnimalViewingScopeController.createAnimalViewingScopeControl({});

   speciesEl.value = 'Lion';
   exhibitEl.value = 'Savanna';
   globalThis.fetch = async () => {
      throw new Error('network');
   };
   await control.refresh();
   assert.equal(viewingScopeEl.children.length, 0);

   _mockViewingScopesResponse([]);
   await control.refresh();
   assert.equal(viewingScopeEl.children.length, 0);
   assert.deepEqual(
      AnimalViewingScopeControlHelper.selectedEnclosureNames(viewingScopeEl),
      []
   );
});
