import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { AnimalsApi } from '../../../scripts/api/animalsApi.js';

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

test('Test_GetRegions_TestMixedRows_ExpectNormalizedNames', async () => {
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

   assert.deepEqual(await AnimalsApi.getRegions(), [
      { name: 'Americas', hasExhibits: true },
      { name: 'Indo-Malaya', hasExhibits: false },
   ]);
});

test('Test_GetExhibitsInRegion_TestNames_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-exhibits-in-region');
      assert.deepEqual(JSON.parse(options.body), { region: 'Americas' });

      return mockResponse(JSON.stringify({
         exhibits: ['  African Savanna  ', '', null],
      }));
   };

   assert.deepEqual(await AnimalsApi.getExhibitsInRegion('Americas'), ['African Savanna']);
});

test('Test_GetAnimalsInExhibit_TestNames_ExpectNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-animal-names-by-exhibit');
      assert.deepEqual(JSON.parse(options.body), { exhibit: 'African Savanna' });

      return mockResponse(JSON.stringify({
         animals: ['  African Lion  ', '  '],
      }));
   };

   assert.deepEqual(await AnimalsApi.getAnimalsInExhibit('African Savanna'), ['African Lion']);
});

test('Test_GetAnimalViewingScopes_TestMixedScopes_ExpectValidOnly', async () => {
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

   assert.deepEqual(await AnimalsApi.getAnimalViewingScopes({
      species: 'African Lion',
      exhibit: 'African Savanna',
   }), ['all', 'indoor', 'outdoor']);
});

test('Test_GetAnimalInformation_TestRows_ExpectFirstNormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/get-animal-information');
      assert.deepEqual(JSON.parse(options.body), {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      });

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

   assert.deepEqual(
      await AnimalsApi.getAnimalInformation({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      {
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
      }
   );
});

test('Test_GetAnimalInformation_TestBlankRows_ExpectNull', async () => {
   globalThis.fetch = async () => mockResponse(JSON.stringify({
      information: [{ species: ' ' }],
   }));

   assert.equal(
      await AnimalsApi.getAnimalInformation({ species: 'African Lion', exhibit: 'Africa Savanna' }),
      null
   );
});
