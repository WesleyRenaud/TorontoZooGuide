import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalDetailView } from '../../../scripts/animals/animalDetailView.js';
import { AnimalsClient } from '../../../scripts/api/animalsClient.js';
import { AnimalsRouter } from '../../../scripts/animals/animalsRouter.js';
import { ListView } from '../../../scripts/animals/listView.js';

async function _flush() {
   await Promise.resolve();
   await Promise.resolve();
}

test('Test_CreateAnimalsRouter_TestRegionExhibitAnimalDetail_ExpectNavigation', async () => {
   const originals = {
      createAnimalsListView: ListView.createAnimalsListView,
      createAnimalDetailView: AnimalDetailView.createAnimalDetailView,
      getRegions: AnimalsClient.getRegions,
      getExhibitsInRegion: AnimalsClient.getExhibitsInRegion,
      getAnimalsInExhibit: AnimalsClient.getAnimalsInExhibit,
      getAnimalInformation: AnimalsClient.getAnimalInformation,
   };
   const renders = {
      regions: [],
      exhibits: [],
      animals: [],
      detail: [],
   };
   let listHandlers;
   let detailHandlers;

   ListView.createAnimalsListView = () => ({
      renderRegions(regions, handlers) {
         renders.regions.push(regions);
         listHandlers = handlers;
      },
      renderExhibits(regionName, exhibits, handlers) {
         renders.exhibits.push({ regionName, exhibits });
         listHandlers = handlers;
      },
      renderAnimals(regionName, exhibitName, animals, handlers) {
         renders.animals.push({ regionName, exhibitName, animals });
         listHandlers = handlers;
      },
   });
   AnimalDetailView.createAnimalDetailView = () => ({
      render(animalInfo, handlers) {
         renders.detail.push({ animalInfo, handlers });
         detailHandlers = handlers;
      },
   });
   AnimalsClient.getRegions = async () => [
      { name: 'Africa', hasExhibits: true },
      { name: 'Australasia', hasExhibits: false },
   ];
   AnimalsClient.getExhibitsInRegion = async (regionName) => [`${regionName}-exhibit`];
   AnimalsClient.getAnimalsInExhibit = async (exhibitName) => [`${exhibitName}-animal`];
   AnimalsClient.getAnimalInformation = async ({ species, exhibit }) => ({
      species,
      exhibit,
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });
      await router.start();
      await _flush();

      assert.equal(renders.regions.length, 1);
      listHandlers.onRegionSelected({ name: 'Africa', hasExhibits: true });
      await _flush();
      assert.equal(renders.exhibits[0].regionName, 'Africa');

      listHandlers.onExhibitSelected('Africa-exhibit');
      await _flush();
      assert.equal(renders.animals[0].exhibitName, 'Africa-exhibit');

      listHandlers.onAnimalSelected('Lion');
      await _flush();
      assert.equal(renders.detail[0].animalInfo.species, 'Lion');

      detailHandlers.onBack();
      await _flush();
      assert.equal(renders.animals.length, 2);

      listHandlers.onBack();
      await _flush();
      assert.equal(renders.exhibits.length, 2);

      listHandlers.onBack();
      await _flush();
      assert.equal(renders.regions.length, 2);

      listHandlers.onRegionSelected({ name: 'Australasia', hasExhibits: false });
      await _flush();
      assert.equal(renders.animals.at(-1).regionName, 'Australasia');
      assert.equal(renders.animals.at(-1).exhibitName, 'Australasia');

      listHandlers.onBack();
      await _flush();
      assert.equal(renders.regions.length, 3);
   } finally {
      ListView.createAnimalsListView = originals.createAnimalsListView;
      AnimalDetailView.createAnimalDetailView = originals.createAnimalDetailView;
      AnimalsClient.getRegions = originals.getRegions;
      AnimalsClient.getExhibitsInRegion = originals.getExhibitsInRegion;
      AnimalsClient.getAnimalsInExhibit = originals.getAnimalsInExhibit;
      AnimalsClient.getAnimalInformation = originals.getAnimalInformation;
   }
});

test('Test_CreateAnimalsRouter_TestStaleNavigation_ExpectSkippedRender', async () => {
   const originals = {
      createAnimalsListView: ListView.createAnimalsListView,
      createAnimalDetailView: AnimalDetailView.createAnimalDetailView,
      getRegions: AnimalsClient.getRegions,
   };
   let resolveFirst;
   const renders = [];

   ListView.createAnimalsListView = () => ({
      renderRegions(regions) {
         renders.push(regions);
      },
      renderExhibits() {},
      renderAnimals() {},
   });
   AnimalDetailView.createAnimalDetailView = () => ({ render() {} });
   AnimalsClient.getRegions = () => new Promise((resolve) => {
      resolveFirst = resolve;
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: {} });
      const first = router.start();
      AnimalsClient.getRegions = async () => [{ name: 'Second' }];
      await router.start();
      resolveFirst([{ name: 'First' }]);
      await first;
      assert.deepEqual(renders, [[{ name: 'Second' }]]);
   } finally {
      ListView.createAnimalsListView = originals.createAnimalsListView;
      AnimalDetailView.createAnimalDetailView = originals.createAnimalDetailView;
      AnimalsClient.getRegions = originals.getRegions;
   }
});
