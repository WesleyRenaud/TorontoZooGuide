import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RegionStore } from '../../../../../scripts/itinerary/selectors/regionSelector/regionStore.js';
import { AnimalIdentity } from '../../../../../scripts/itinerary/animalIdentity.js';

test('Test_GetExhibitNamesFromAnimals_TestNormalizedAnimals_ExpectDedupedExhibits', () => {
   assert.deepEqual(
      RegionStore.getExhibitNamesFromAnimals([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'African Penguin', exhibit: 'Africa Savanna' },
         { species: 'Amur Tiger', exhibit: 'Eurasia Wilds' },
      ]),
      ['Africa Savanna', 'Eurasia Wilds']
   );
});

test('Test_OmitRemovedAnimals_TestRemovalKeys_ExpectFiltered', () => {
   const animals = [
      { species: 'African Lion', exhibit: 'Africa Savanna' },
      { species: 'African Penguin', exhibit: 'Africa Savanna' },
   ];
   const removedKeys = new Set(['african penguin||africa savanna']);

   assert.deepEqual(
      RegionStore.omitRemovedAnimals(animals, removedKeys).map((animal) => animal.species),
      ['African Lion']
   );
});

test('Test_BuildSelectedAnimalKey_TestExplicitId_ExpectPreferred', () => {
   assert.equal(
      RegionStore.buildSelectedAnimalKey({
         id: 'Custom-Id',
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      'custom-id'
   );
});

test('Test_ParseAnimalWireKey_TestSpeciesExhibitEnclosure_ExpectSplit', () => {
   assert.deepEqual(
      RegionStore.parseAnimalWireKey('Masai Giraffe||Africa Savanna||Giraffe House'),
      {
         species: 'Masai Giraffe',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Giraffe House',
      }
   );
   assert.deepEqual(
      RegionStore.parseAnimalWireKey('African Lion||Africa Savanna'),
      {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }
   );
});

test('Test_BuildSelectedAnimalKeyFromWire_TestWireKey_ExpectNormalized', () => {
   assert.equal(
      RegionStore.buildSelectedAnimalKeyFromWire('African Penguin||Africa Savanna||Outdoor'),
      'african penguin||africa savanna||outdoor'
   );
});

test('Test_NormalizeSelectedAnimal_TestSpeciesAndExhibit_ExpectSynthesizedId', () => {
   const normalized = RegionStore.normalizeSelectedAnimal({
      species: 'African Lion',
      exhibit: 'Africa Savanna',
   });

   assert.equal(normalized.id, 'African Lion||Africa Savanna');
   assert.equal(normalized.imageSrc, null);
});

test('Test_MergeAnimals_TestDuplicates_ExpectDedupedByKey', () => {
   const merged = RegionStore.mergeAnimals(
      [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'African Penguin', exhibit: 'Africa Savanna' },
      ]
   );

   assert.deepEqual(
      merged.map((animal) => animal.species).sort(),
      ['African Lion', 'African Penguin']
   );
});

test('Test_ShouldHideDuplicateSingleExhibit_TestMirrorRegionName_ExpectHidden', () => {
   assert.equal(
      RegionStore.shouldHideDuplicateSingleExhibit({
         name: 'Americas',
         exhibits: ['Americas'],
      }),
      true
   );
   assert.equal(
      RegionStore.shouldHideDuplicateSingleExhibit({
         name: 'Africa',
         exhibits: ['Africa Savanna', 'Africa Rainforest'],
      }),
      false
   );
});

test('Test_SelectedExhibitsNeedAnimalRebuild_TestStaleSelection_ExpectDetected', () => {
   const selectedExhibits = new Set(['Africa Savanna']);

   assert.equal(
      RegionStore.selectedExhibitsNeedAnimalRebuild(selectedExhibits, []),
      true
   );
   assert.equal(
      RegionStore.selectedExhibitsNeedAnimalRebuild(
         selectedExhibits,
         [{ species: 'African Lion', exhibit: 'Africa Savanna' }]
      ),
      false
   );
   assert.equal(
      RegionStore.selectedExhibitsNeedAnimalRebuild(
         new Set(['Africa Savanna', 'Eurasia Wilds']),
         [{ species: 'African Lion', exhibit: 'Africa Savanna' }]
      ),
      true
   );
});

test('Test_DraftAnimalsCoverCatalogAnimals_TestCoverage_ExpectEveryCatalogAnimal', () => {
   const draft = [
      { species: 'African Lion', exhibit: 'Africa Savanna' },
      { species: 'Watusi Cattle', exhibit: 'Africa Savanna' },
   ];
   const catalog = [
      { species: 'African Lion', exhibit: 'Africa Savanna' },
      { species: 'Watusi Cattle', exhibit: 'Africa Savanna' },
   ];

   assert.equal(RegionStore.draftAnimalsCoverCatalogAnimals(draft, catalog), true);
   assert.equal(
      RegionStore.draftAnimalsCoverCatalogAnimals(
         [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
         catalog
      ),
      false
   );
   assert.equal(RegionStore.draftAnimalsCoverCatalogAnimals(draft, []), true);
});

test('Test_CreateEmptyRegionAndNormalizeSelectedAnimal_TestGuards_ExpectDefaults', () => {
   assert.deepEqual(RegionStore.createEmptyRegion(), {
      name: '',
      exhibits: [],
   });
   assert.deepEqual(
      RegionStore.normalizeRegion({ name: '  Africa  ', exhibits: [' Africa Savanna ', ''] }),
      { name: 'Africa', exhibits: ['Africa Savanna'] }
   );
   assert.deepEqual(
      RegionStore.normalizeRegions([
         { name: '  Africa  ', exhibits: ['Africa Savanna'] },
         { name: '   ', exhibits: ['Ignored'] },
      ]),
      [{ name: 'Africa', exhibits: ['Africa Savanna'] }]
   );
   assert.equal(RegionStore.normalizeSelectedAnimal(null), null);
   assert.equal(RegionStore.normalizeSelectedAnimal('lion'), null);
   assert.equal(RegionStore.normalizeSelectedAnimal({ exhibit: 'Africa' }), null);
   assert.deepEqual(
      RegionStore.makeSelectedAnimal({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Overlook',
         imageSrc: ' ../images/lion.png ',
      }),
      {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Overlook',
         imageSrc: '../images/lion.png',
         id: 'African Lion||Africa Savanna||Overlook',
      }
   );
   assert.equal(RegionStore.buildSelectedAnimalKey(null), '');
   assert.equal(RegionStore.parseAnimalWireKey(''), null);
   assert.equal(RegionStore.parseAnimalWireKey('||Africa'), null);

   const region = { name: 'Africa', exhibits: ['Africa Savanna', 'Africa Rainforest'] };
   const selectedExhibits = new Set(['Africa Savanna', 'Africa Rainforest']);
   assert.equal(RegionStore.isRegionFullySelected(region, selectedExhibits), true);
   assert.equal(RegionStore.isRegionFullySelected({ name: 'Empty', exhibits: [] }, selectedExhibits), false);

   const selectedRegionNames = new Set();
   RegionStore.syncRegionSelection(region, selectedRegionNames, selectedExhibits);
   assert.equal(selectedRegionNames.has('Africa'), true);
   RegionStore.syncRegionSelection(region, selectedRegionNames, new Set(['Africa Savanna']));
   assert.equal(selectedRegionNames.has('Africa'), false);
   RegionStore.syncRegionSelection({ name: '', exhibits: [] }, selectedRegionNames, selectedExhibits);

   assert.equal(RegionStore.selectedExhibitsNeedAnimalRebuild(new Set(), []), false);

   const originalNormalize = RegionStore.normalizeSelectedAnimal;
   RegionStore.normalizeSelectedAnimal = () => ({
      species: 'African Lion',
      exhibit: 'Africa Savanna',
      id: '',
   });
   try {
      assert.equal(
         RegionStore.buildSelectedAnimalKey({ species: 'African Lion' }),
         AnimalIdentity.buildAnimalIdentityStorageKey({
            species: 'African Lion',
            exhibit: 'Africa Savanna',
         })
      );
   } finally {
      RegionStore.normalizeSelectedAnimal = originalNormalize;
   }
});
