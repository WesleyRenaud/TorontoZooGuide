import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { AnimalViewingScopeController } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeController.js';
import { AnimalViewingModel } from '../../../../../scripts/shared/enums/animalViewingModel.js';

const originalFetch = globalThis.fetch;

function _createField(value = '') {
   const listeners = {};

   return {
      value,
      disabled: false,
      addEventListener(eventName, handler) {
         listeners[eventName] = handler;
      },
      trigger(eventName) {
         return listeners[eventName]?.();
      },
   };
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

test('Test_CreateAnimalViewingScopeControl_TestIndoorAndOutdoor_ExpectSelectEnabled', async () => {
   const speciesEl = _createField('Southern White Rhinoceros');
   const exhibitEl = _createField('Africa Savanna');
   const viewingScopeEl = _createField('');

   _mockViewingScopesResponse([
      AnimalViewingModel.INDOOR,
      AnimalViewingModel.OUTDOOR,
   ]);

   AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   assert.equal(viewingScopeEl.disabled, true);
   assert.equal(viewingScopeEl.value, '');

   await speciesEl.trigger('change');

   assert.equal(viewingScopeEl.disabled, false);
   assert.equal(viewingScopeEl.value, AnimalViewingModel.ALL);
});

test('Test_CreateAnimalViewingScopeControl_TestSingleScope_ExpectLocked', async () => {
   const speciesEl = _createField('African Lion');
   const exhibitEl = _createField('Africa Savanna');
   const viewingScopeEl = _createField('');

   _mockViewingScopesResponse([
      AnimalViewingModel.OUTDOOR,
   ]);

   AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   await speciesEl.trigger('change');

   assert.equal(viewingScopeEl.disabled, true);
   assert.equal(viewingScopeEl.value, AnimalViewingModel.OUTDOOR);
});

test('Test_CreateAnimalViewingScopeControl_TestMissingFieldsAndErrors_ExpectReset', async () => {
   const speciesEl = _createField('');
   const exhibitEl = _createField('');
   const viewingScopeEl = _createField('stale');

   const control = AnimalViewingScopeController.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   assert.equal(viewingScopeEl.value, '');
   assert.equal(viewingScopeEl.disabled, true);

   await control.refresh();
   assert.equal(viewingScopeEl.value, '');

   AnimalViewingScopeController.createAnimalViewingScopeControl({});

   speciesEl.value = 'Lion';
   exhibitEl.value = 'Savanna';
   globalThis.fetch = async () => {
      throw new Error('network');
   };
   await control.refresh();
   assert.equal(viewingScopeEl.value, '');
   assert.equal(viewingScopeEl.disabled, true);

   _mockViewingScopesResponse([]);
   await control.refresh();
   assert.equal(viewingScopeEl.value, '');
});
