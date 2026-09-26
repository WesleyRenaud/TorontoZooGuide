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
   const maleHerd = 'Male Herd';
   const femaleHerd = 'Female Herd';
   const viewingScopes = [
      { enclosureName: maleHerd, label: maleHerd },
      { enclosureName: femaleHerd, label: femaleHerd },
   ];
   const speciesEl = _createField('Wood Bison');
   const exhibitEl = _createField('Canadian Domain');
   const viewingScopeEl = _createGrid();
   _mockViewingScopesResponse(viewingScopes);

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });
   const selectedBeforeChange = control.selectedEnclosureNames();
   await speciesEl.trigger('change');

   assert.deepEqual(selectedBeforeChange, []);
   assert.deepEqual(control.selectedEnclosureNames(), [maleHerd, femaleHerd]);
   assert.equal(viewingScopeEl.querySelectorAll('input[type="checkbox"]').length, viewingScopes.length);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      false
   );
});


test('Test_CreateAnimalViewingScopeControl_TestExhibitSelectedAfterSpecies_ExpectLoadsScopes', async () => {
   const main = 'Main';
   const yard = 'Yard';
   const exhibit = 'Africa Savanna';
   const speciesEl = _createField('Lesser Kudu');
   const exhibitEl = _createField('');
   const viewingScopeEl = _createGrid();
   _mockViewingScopesResponse([
      { enclosureName: main, label: main },
      { enclosureName: yard, label: yard },
   ]);
   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   await speciesEl.trigger('change');
   exhibitEl.value = exhibit;
   await exhibitEl.trigger('change');

   assert.deepEqual(control.selectedEnclosureNames(), [main, yard]);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      false
   );
});


test('Test_CreateAnimalViewingScopeControl_TestSpeciesWithoutExhibit_ExpectNoCheckboxes', async () => {
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
   assert.deepEqual(control.selectedEnclosureNames(), []);
});


test('Test_CreateAnimalViewingScopeControl_TestUnnamedEnclosure_ExpectMainSelected', async () => {
   const unnamed = '';
   const speciesEl = _createField('African Lion');
   const exhibitEl = _createField('Africa Savanna');
   const viewingScopeEl = _createGrid();
   _mockViewingScopesResponse([
      { enclosureName: unnamed, label: 'Main' },
   ]);

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });
   await speciesEl.trigger('change');

   assert.deepEqual(control.selectedEnclosureNames(), [unnamed]);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      true
   );
});


test('Test_CreateAnimalViewingScopeControl_TestInjectedLoader_ExpectUsed', async () => {
   const species = 'Sumatran Orangutan';
   const exhibit = 'Indo-Malaya Pavilion';
   const indoor = 'Indoor';
   const speciesEl = _createField(species);
   const exhibitEl = _createField(exhibit);
   const viewingScopeEl = _createGrid();
   const payloads = [];

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      loadViewingScopes: async (payload) => {
         payloads.push(payload);
         return [
            { enclosureName: indoor, label: indoor },
         ];
      },
   });
   await speciesEl.trigger('change');

   assert.deepEqual(payloads, [{ species, exhibit }]);
   assert.deepEqual(control.selectedEnclosureNames(), [indoor]);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      true
   );
});


test('Test_CreateAnimalViewingScopeControl_TestSingleClosedAmongMany_ExpectFieldVisible', async () => {
   const indoor = 'Indoor';
   const outdoor = 'Outdoor';
   const speciesEl = _createField('Sumatran Orangutan');
   const exhibitEl = _createField('Indo-Malaya Pavilion');
   const viewingScopeEl = _createGrid();

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      loadViewingScopes: async () => [
         { enclosureName: indoor, label: indoor },
      ],
      loadAnimalViewingScopes: async () => [
         { enclosureName: indoor, label: indoor },
         { enclosureName: outdoor, label: outdoor },
      ],
   });
   await speciesEl.trigger('change');

   assert.deepEqual(control.selectedEnclosureNames(), [indoor]);
   assert.equal(viewingScopeEl.querySelectorAll('input[type="checkbox"]').length, 1);
   assert.equal(viewingScopeEl.textContent.includes(indoor), true);
   assert.equal(viewingScopeEl.textContent.includes(outdoor), false);
   assert.equal(
      viewingScopeEl.closest('.console-operations-field').classList.contains('is-invisible'),
      false
   );
});


test('Test_CreateAnimalViewingScopeControl_TestMissingFields_ExpectReset', () => {
   const viewingScopeEl = _createGrid();
   viewingScopeEl.appendChild(document.createElement('input'));

   AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl: _createField(''),
      exhibitEl: _createField(''),
      viewingScopeEl,
   });

   assert.equal(viewingScopeEl.children.length, 0);
});


test('Test_CreateAnimalViewingScopeControl_TestRefreshWithoutValues_ExpectEmpty', async () => {
   const viewingScopeEl = _createGrid();
   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl: _createField(''),
      exhibitEl: _createField(''),
      viewingScopeEl,
   });

   await control.refresh();

   assert.equal(viewingScopeEl.children.length, 0);
});


test('Test_CreateAnimalViewingScopeControl_TestMissingElements_ExpectNoop', () => {
   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({});

   assert.equal(typeof control.refresh, 'function');
});


test('Test_CreateAnimalViewingScopeControl_TestNetworkError_ExpectReset', async () => {
   const speciesEl = _createField('Lion');
   const exhibitEl = _createField('Savanna');
   const viewingScopeEl = _createGrid();
   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });
   globalThis.fetch = async () => {
      throw new Error('network');
   };

   await control.refresh();

   assert.equal(viewingScopeEl.children.length, 0);
});


test('Test_CreateAnimalViewingScopeControl_TestEmptyResponse_ExpectReset', async () => {
   const speciesEl = _createField('Lion');
   const exhibitEl = _createField('Savanna');
   const viewingScopeEl = _createGrid();
   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });
   _mockViewingScopesResponse([]);

   await control.refresh();

   assert.equal(viewingScopeEl.children.length, 0);
   assert.deepEqual(
      AnimalViewingScopeControlHelper.selectedEnclosureNames(viewingScopeEl),
      []
   );
});
