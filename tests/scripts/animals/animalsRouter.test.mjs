import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalDetailView } from '../../../scripts/animals/animalDetailView.js';
import { AnimalsClient } from '../../../scripts/api/animalsClient.js';
import { AnimalsRouter } from '../../../scripts/animals/animalsRouter.js';
import { ListView } from '../../../scripts/animals/listView.js';
import { Position } from '../../../scripts/shared/enums/position.js';


async function _flush() {
   await Promise.resolve();
   await Promise.resolve();
}


function _installRouterStubs({
   renders,
   getListHandlers,
   setListHandlers,
   setDetailHandlers,
}) {
   const originals = {
      createAnimalsListView: ListView.createAnimalsListView,
      createAnimalDetailView: AnimalDetailView.createAnimalDetailView,
      getRegions: AnimalsClient.getRegions,
      getExhibitsInRegion: AnimalsClient.getExhibitsInRegion,
      getAnimalsInExhibit: AnimalsClient.getAnimalsInExhibit,
      getAnimalInformation: AnimalsClient.getAnimalInformation,
   };

   ListView.createAnimalsListView = () => ({
      renderRegions(regions, handlers) {
         renders.regions.push(regions);
         setListHandlers(handlers);
      },
      renderExhibits(regionName, exhibits, handlers) {
         renders.exhibits.push({ regionName, exhibits });
         setListHandlers(handlers);
      },
      renderAnimals(regionName, exhibitName, animals, handlers) {
         renders.animals.push({ regionName, exhibitName, animals });
         setListHandlers(handlers);
      },
   });
   AnimalDetailView.createAnimalDetailView = () => ({
      render(animalInfo, handlers) {
         renders.detail.push({ animalInfo, handlers });
         setDetailHandlers(handlers);
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

   return originals;
}


function _restoreRouterStubs(originals) {
   ListView.createAnimalsListView = originals.createAnimalsListView;
   AnimalDetailView.createAnimalDetailView = originals.createAnimalDetailView;
   AnimalsClient.getRegions = originals.getRegions;
   AnimalsClient.getExhibitsInRegion = originals.getExhibitsInRegion;
   AnimalsClient.getAnimalsInExhibit = originals.getAnimalsInExhibit;
   AnimalsClient.getAnimalInformation = originals.getAnimalInformation;
}


test('Test_CreateAnimalsRouter_TestStart_ExpectRegions', async () => {
   const renders = { regions: [], exhibits: [], animals: [], detail: [] };
   let listHandlers;
   let detailHandlers;
   const originals = _installRouterStubs({
      renders,
      setListHandlers: (handlers) => { listHandlers = handlers; },
      setDetailHandlers: (handlers) => { detailHandlers = handlers; },
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });

      await router.start();
      await _flush();

      assert.equal(renders.regions.length, Position.SECOND);
      assert.ok(listHandlers);
      assert.equal(detailHandlers, undefined);
   } finally {
      _restoreRouterStubs(originals);
   }
});


test('Test_CreateAnimalsRouter_TestRegionSelected_ExpectExhibits', async () => {
   const renders = { regions: [], exhibits: [], animals: [], detail: [] };
   let listHandlers;
   const region = { name: 'Africa', hasExhibits: true };
   const originals = _installRouterStubs({
      renders,
      setListHandlers: (handlers) => { listHandlers = handlers; },
      setDetailHandlers: () => {},
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });
      await router.start();
      await _flush();

      listHandlers.onRegionSelected(region);
      await _flush();

      assert.equal(renders.exhibits.at(Position.FIRST).regionName, region.name);
   } finally {
      _restoreRouterStubs(originals);
   }
});


test('Test_CreateAnimalsRouter_TestExhibitSelected_ExpectAnimals', async () => {
   const renders = { regions: [], exhibits: [], animals: [], detail: [] };
   let listHandlers;
   const region = { name: 'Africa', hasExhibits: true };
   const exhibitName = `${region.name}-exhibit`;
   const originals = _installRouterStubs({
      renders,
      setListHandlers: (handlers) => { listHandlers = handlers; },
      setDetailHandlers: () => {},
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });
      await router.start();
      await _flush();
      listHandlers.onRegionSelected(region);
      await _flush();

      listHandlers.onExhibitSelected(exhibitName);
      await _flush();

      assert.equal(renders.animals.at(Position.FIRST).exhibitName, exhibitName);
   } finally {
      _restoreRouterStubs(originals);
   }
});


test('Test_CreateAnimalsRouter_TestAnimalSelected_ExpectDetail', async () => {
   const renders = { regions: [], exhibits: [], animals: [], detail: [] };
   let listHandlers;
   const region = { name: 'Africa', hasExhibits: true };
   const exhibitName = `${region.name}-exhibit`;
   const species = 'Lion';
   const originals = _installRouterStubs({
      renders,
      setListHandlers: (handlers) => { listHandlers = handlers; },
      setDetailHandlers: () => {},
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });
      await router.start();
      await _flush();
      listHandlers.onRegionSelected(region);
      await _flush();
      listHandlers.onExhibitSelected(exhibitName);
      await _flush();

      listHandlers.onAnimalSelected(species);
      await _flush();

      assert.equal(renders.detail.at(Position.FIRST).animalInfo.species, species);
   } finally {
      _restoreRouterStubs(originals);
   }
});


test('Test_CreateAnimalsRouter_TestBackFromDetail_ExpectAnimalsRerendered', async () => {
   const renders = { regions: [], exhibits: [], animals: [], detail: [] };
   let listHandlers;
   let detailHandlers;
   const region = { name: 'Africa', hasExhibits: true };
   const exhibitName = `${region.name}-exhibit`;
   const originals = _installRouterStubs({
      renders,
      setListHandlers: (handlers) => { listHandlers = handlers; },
      setDetailHandlers: (handlers) => { detailHandlers = handlers; },
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });
      await router.start();
      await _flush();
      listHandlers.onRegionSelected(region);
      await _flush();
      listHandlers.onExhibitSelected(exhibitName);
      await _flush();
      listHandlers.onAnimalSelected('Lion');
      await _flush();

      detailHandlers.onBack();
      await _flush();

      assert.equal(renders.animals.length, 2);
   } finally {
      _restoreRouterStubs(originals);
   }
});


test('Test_CreateAnimalsRouter_TestBackFromAnimals_ExpectExhibitsRerendered', async () => {
   const renders = { regions: [], exhibits: [], animals: [], detail: [] };
   let listHandlers;
   const region = { name: 'Africa', hasExhibits: true };
   const exhibitName = `${region.name}-exhibit`;
   const originals = _installRouterStubs({
      renders,
      setListHandlers: (handlers) => { listHandlers = handlers; },
      setDetailHandlers: () => {},
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });
      await router.start();
      await _flush();
      listHandlers.onRegionSelected(region);
      await _flush();
      listHandlers.onExhibitSelected(exhibitName);
      await _flush();

      listHandlers.onBack();
      await _flush();

      assert.equal(renders.exhibits.length, 2);
   } finally {
      _restoreRouterStubs(originals);
   }
});


test('Test_CreateAnimalsRouter_TestBackFromExhibits_ExpectRegionsRerendered', async () => {
   const renders = { regions: [], exhibits: [], animals: [], detail: [] };
   let listHandlers;
   const region = { name: 'Africa', hasExhibits: true };
   const originals = _installRouterStubs({
      renders,
      setListHandlers: (handlers) => { listHandlers = handlers; },
      setDetailHandlers: () => {},
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });
      await router.start();
      await _flush();
      listHandlers.onRegionSelected(region);
      await _flush();

      listHandlers.onBack();
      await _flush();

      assert.equal(renders.regions.length, 2);
   } finally {
      _restoreRouterStubs(originals);
   }
});


test('Test_CreateAnimalsRouter_TestRegionWithoutExhibits_ExpectAnimals', async () => {
   const renders = { regions: [], exhibits: [], animals: [], detail: [] };
   let listHandlers;
   const region = { name: 'Australasia', hasExhibits: false };
   const originals = _installRouterStubs({
      renders,
      setListHandlers: (handlers) => { listHandlers = handlers; },
      setDetailHandlers: () => {},
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });
      await router.start();
      await _flush();

      listHandlers.onRegionSelected(region);
      await _flush();
      const lastAnimals = renders.animals.at(Position.LAST);

      assert.equal(lastAnimals.regionName, region.name);
      assert.equal(lastAnimals.exhibitName, region.name);
   } finally {
      _restoreRouterStubs(originals);
   }
});


test('Test_CreateAnimalsRouter_TestBackFromRegionWithoutExhibits_ExpectRegions', async () => {
   const renders = { regions: [], exhibits: [], animals: [], detail: [] };
   let listHandlers;
   const region = { name: 'Australasia', hasExhibits: false };
   const originals = _installRouterStubs({
      renders,
      setListHandlers: (handlers) => { listHandlers = handlers; },
      setDetailHandlers: () => {},
   });

   try {
      const router = AnimalsRouter.createAnimalsRouter({ listEl: { id: 'list' } });
      await router.start();
      await _flush();
      listHandlers.onRegionSelected(region);
      await _flush();

      listHandlers.onBack();
      await _flush();

      assert.equal(renders.regions.length, 2);
   } finally {
      _restoreRouterStubs(originals);
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
   const firstRegions = [{ name: 'First' }];
   const secondRegions = [{ name: 'Second' }];

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
      AnimalsClient.getRegions = async () => secondRegions;
      await router.start();
      resolveFirst(firstRegions);
      await first;

      assert.deepEqual(renders, [secondRegions]);
   } finally {
      ListView.createAnimalsListView = originals.createAnimalsListView;
      AnimalDetailView.createAnimalDetailView = originals.createAnimalDetailView;
      AnimalsClient.getRegions = originals.getRegions;
   }
});
