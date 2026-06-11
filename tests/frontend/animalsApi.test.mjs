import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import {
   createAnimalsApi,
   getAnimalInformation,
   getAnimalsInExhibit,
   getAnimalViewingScopes,
   getExhibitsInRegion,
   getRegions,
} from '../../scripts/api/animalsApi.js';

function mockResponse(text = '{}') {
   return {
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => text,
   };
}

afterEach(() => {
   delete globalThis.fetch;
});

test('getRegions normalizes region rows and drops blank names', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-regions');
      assert.deepEqual(JSON.parse(options.body), {});

      return mockResponse(JSON.stringify({
         regions: [
            { name: '  Americas  ', hasExhibits: true },
            { name: ' ', hasExhibits: true },
            { name: 'Indo-Malaya', hasExhibits: 0 },
         ],
      }));
   };

   assert.deepEqual(await getRegions(), [
      { name: 'Americas', hasExhibits: true },
      { name: 'Indo-Malaya', hasExhibits: false },
   ]);
});

test('getExhibitsInRegion normalizes exhibit names', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-exhibits-in-region');
      assert.deepEqual(JSON.parse(options.body), { region: 'Americas' });

      return mockResponse(JSON.stringify({
         exhibits: ['  African Savanna  ', '', null],
      }));
   };

   assert.deepEqual(await getExhibitsInRegion('Americas'), ['African Savanna']);
});

test('getAnimalsInExhibit normalizes animal names', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-animal-names-by-exhibit');
      assert.deepEqual(JSON.parse(options.body), { exhibit: 'African Savanna' });

      return mockResponse(JSON.stringify({
         animals: ['  African Lion  ', '  '],
      }));
   };

   assert.deepEqual(await getAnimalsInExhibit('African Savanna'), ['African Lion']);
});

test('getAnimalViewingScopes keeps only valid viewing scopes', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-animal-viewing-scopes');
      assert.deepEqual(JSON.parse(options.body), {
         species: 'African Lion',
         exhibit: 'African Savanna',
      });

      return mockResponse(JSON.stringify({
         viewingScopes: ['all', 'indoor', 'invalid', '  outdoor  '],
      }));
   };

   assert.deepEqual(await getAnimalViewingScopes({
      species: 'African Lion',
      exhibit: 'African Savanna',
   }), ['all', 'indoor', 'outdoor']);
});

test('getAnimalInformation returns the first normalized animal row', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-animal-information');
      assert.deepEqual(JSON.parse(options.body), { species: 'African Lion' });

      return mockResponse(JSON.stringify({
         information: [
            { species: ' ', exhibit: 'African Savanna' },
            {
               species: '  African Lion  ',
               latin_name: '  Panthera leo  ',
               exhibit: '  African Savanna  ',
               animals_at_the_zoo: '',
            },
         ],
      }));
   };

   assert.deepEqual(await getAnimalInformation('African Lion'), {
      species: 'African Lion',
      latin_name: 'Panthera leo',
      general_viewing_tips: null,
      seasonal_viewing_tips: null,
      identification: null,
      habitat_and_range: null,
      diet_and_feeding: null,
      behaviour_and_life_cycle: null,
      adaptations: null,
      reproduction_and_life_cycle: null,
      animals_at_the_zoo: null,
      exhibit: 'African Savanna',
      seasonal_viewing_summary: null,
      seasonal_viewing_information: null,
   });
});

test('getAnimalInformation returns null when no animal rows remain', async () => {
   globalThis.fetch = async () => mockResponse(JSON.stringify({
      information: [{ species: ' ' }],
   }));

   assert.equal(await getAnimalInformation('African Lion'), null);
});

test('createAnimalsApi exposes animals API methods', () => {
   const api = createAnimalsApi();

   assert.equal(typeof api.getRegions, 'function');
   assert.equal(typeof api.getExhibitsInRegion, 'function');
   assert.equal(typeof api.getAnimalsInExhibit, 'function');
   assert.equal(typeof api.getAnimalViewingScopes, 'function');
   assert.equal(typeof api.getAnimalInformation, 'function');
});
