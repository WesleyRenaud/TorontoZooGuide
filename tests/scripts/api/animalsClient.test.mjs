import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { AnimalsApiNormalizer } from '../../../scripts/api/animalsApiNormalizer.js';
import { AnimalsClient } from '../../../scripts/api/animalsClient.js';
import { ValueNormalizer } from '../../../scripts/api/valueNormalizer.js';

function _mockResponse(text = '{}') {
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
   const americas = 'Americas';
   const hasExhibits = true;
   const indoMalaya = 'Indo-Malaya';
   const url = '/get-regions';
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), {});

      return _mockResponse(JSON.stringify({
         regions: [
            { name: `  ${americas}  `, hasExhibits },
            { name: ' ', hasExhibits },
            { name: indoMalaya, hasExhibits: 0 },
         ],
      }));
   };

   const regions = await AnimalsClient.getRegions();

   assert.deepEqual(regions, [
      { name: americas, hasExhibits },
      { name: indoMalaya, hasExhibits: ValueNormalizer.asBoolean(0) },
   ]);
});


test('Test_GetExhibitsInRegion_TestNames_ExpectNormalized', async () => {
   const region = 'Americas';
   const exhibit = 'African Savanna';
   const url = '/get-exhibits-in-region';
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), { region });

      return _mockResponse(JSON.stringify({
         exhibits: [`  ${exhibit}  `, '', null],
      }));
   };

   const exhibits = await AnimalsClient.getExhibitsInRegion(region);

   assert.deepEqual(exhibits, [exhibit]);
});


test('Test_GetAnimalsInExhibit_TestNames_ExpectNormalized', async () => {
   const exhibit = 'African Savanna';
   const species = 'African Lion';
   const url = '/get-animal-names-by-exhibit';
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), { exhibit });

      return _mockResponse(JSON.stringify({
         animals: [`  ${species}  `, '  '],
      }));
   };

   const animals = await AnimalsClient.getAnimalsInExhibit(exhibit);

   assert.deepEqual(animals, [species]);
});


test('Test_GetAnimalViewingScopes_TestResponse_ExpectScopes', async () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const url = '/get-animal-viewing-scopes';
   const viewingScopes = [
      { enclosureName: 'Male Herd', label: 'Male Herd' },
      { enclosureName: '', label: 'Main' },
   ];
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), {
         species,
         exhibit,
      });

      return _mockResponse(JSON.stringify({ viewingScopes }));
   };

   const scopes = await AnimalsClient.getAnimalViewingScopes({
      species,
      exhibit,
   });

   assert.deepEqual(scopes, viewingScopes);
});


test('Test_GetAnimalInformation_TestRows_ExpectFirstNormalized', async () => {
   const species = 'African Lion';
   const requestExhibit = 'Africa Savanna';
   const exhibit = 'African Savanna';
   const latinName = 'Panthera leo';
   const url = '/get-animal-information';
   const validRow = {
      species: `  ${species}  `,
      latin_name: `  ${latinName}  `,
      exhibit: `  ${exhibit}  `,
      animals_at_the_zoo: '',
   };
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), {
         species,
         exhibit: requestExhibit,
      });

      return _mockResponse(JSON.stringify({
         information: [
            { species: ' ', exhibit },
            validRow,
         ],
      }));
   };

   const animal = await AnimalsClient.getAnimalInformation({
      species,
      exhibit: requestExhibit,
   });

   assert.deepEqual(animal, AnimalsApiNormalizer.normalizeAnimalInformation(validRow));
});


test('Test_GetAnimalInformation_TestBlankRows_ExpectNull', async () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   globalThis.fetch = async () => _mockResponse(JSON.stringify({
      information: [{ species: ' ' }],
   }));

   const animal = await AnimalsClient.getAnimalInformation({ species, exhibit });

   assert.equal(animal, null);
});
