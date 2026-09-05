import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { AnimalViewingScopeControl } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeControl.js';
import { AnimalViewingScope } from '../../../../../scripts/shared/enums/animalViewingScope.js';

const originalFetch = globalThis.fetch;

function createField(value = '') {
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

function mockViewingScopesResponse(viewingScopes) {
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
   const speciesEl = createField('Southern White Rhinoceros');
   const exhibitEl = createField('Africa Savanna');
   const viewingScopeEl = createField('');

   mockViewingScopesResponse([
      AnimalViewingScope.INDOOR,
      AnimalViewingScope.OUTDOOR,
   ]);

   AnimalViewingScopeControl.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   assert.equal(viewingScopeEl.disabled, true);
   assert.equal(viewingScopeEl.value, '');

   await speciesEl.trigger('change');

   assert.equal(viewingScopeEl.disabled, false);
   assert.equal(viewingScopeEl.value, AnimalViewingScope.ALL);
});

test('Test_CreateAnimalViewingScopeControl_TestSingleScope_ExpectLocked', async () => {
   const speciesEl = createField('African Lion');
   const exhibitEl = createField('Africa Savanna');
   const viewingScopeEl = createField('');

   mockViewingScopesResponse([
      AnimalViewingScope.OUTDOOR,
   ]);

   AnimalViewingScopeControl.createAnimalViewingScopeControl({
      speciesEl,
      exhibitEl,
      viewingScopeEl,
   });

   await speciesEl.trigger('change');

   assert.equal(viewingScopeEl.disabled, true);
   assert.equal(viewingScopeEl.value, AnimalViewingScope.OUTDOOR);
});
