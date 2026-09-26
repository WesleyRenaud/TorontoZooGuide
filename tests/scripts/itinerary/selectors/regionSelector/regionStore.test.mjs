import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RegionStore } from '../../../../../scripts/itinerary/selectors/regionSelector/regionStore.js';
import { AnimalIdentity } from '../../../../../scripts/itinerary/animalIdentity.js';
import { ScheduleItemKeySeparator } from '../../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_GetExhibitNamesFromAnimals_TestNormalizedAnimals_ExpectDedupedExhibits', () => {
   const savanna = 'Africa Savanna';
   const eurasia = 'Eurasia Wilds';
   const animals = [
      { species: 'African Lion', exhibit: savanna },
      { species: 'African Penguin', exhibit: savanna },
      { species: 'Amur Tiger', exhibit: eurasia },
   ];

   const exhibits = RegionStore.getExhibitNamesFromAnimals(animals);

   assert.deepEqual(exhibits, [savanna, eurasia]);
});


test('Test_OmitRemovedAnimals_TestRemovalKeys_ExpectFiltered', () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   const animals = [lion, penguin];
   const removedKeys = new Set([AnimalIdentity.buildAnimalIdentityStorageKey(penguin)]);

   const remaining = RegionStore.omitRemovedAnimals(animals, removedKeys);

   assert.equal(remaining.at(Position.FIRST).species, lion.species);
   assert.equal(remaining.length, 1);
});


test('Test_BuildSelectedAnimalKey_TestExplicitId_ExpectPreferred', () => {
   const id = 'Custom-Id';
   const animal = {
      id,
      species: 'African Lion',
      exhibit: 'Africa Savanna',
   };

   const key = RegionStore.buildSelectedAnimalKey(animal);

   assert.equal(key, id.toLowerCase());
});


test('Test_ParseAnimalWireKey_TestSpeciesExhibitEnclosure_ExpectSplit', () => {
   const species = 'Masai Giraffe';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'Giraffe House';
   const wireKey = [species, exhibit, enclosureName].join(ScheduleItemKeySeparator.VALUE);

   const parsed = RegionStore.parseAnimalWireKey(wireKey);

   assert.equal(parsed.species, species);
   assert.equal(parsed.exhibit, exhibit);
   assert.equal(parsed.enclosure_name, enclosureName);
});


test('Test_ParseAnimalWireKey_TestSpeciesAndExhibit_ExpectSplit', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const wireKey = [species, exhibit].join(ScheduleItemKeySeparator.VALUE);

   const parsed = RegionStore.parseAnimalWireKey(wireKey);

   assert.equal(parsed.species, species);
   assert.equal(parsed.exhibit, exhibit);
});


test('Test_BuildSelectedAnimalKeyFromWire_TestWireKey_ExpectNormalized', () => {
   const species = 'African Penguin';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'Outdoor';
   const wireKey = [species, exhibit, enclosureName].join(ScheduleItemKeySeparator.VALUE);

   const key = RegionStore.buildSelectedAnimalKeyFromWire(wireKey);

   assert.equal(
      key,
      AnimalIdentity.buildAnimalIdentityStorageKey({
         species,
         exhibit,
         enclosure_name: enclosureName,
      })
   );
});


test('Test_NormalizeSelectedAnimal_TestSpeciesAndExhibit_ExpectSynthesizedId', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const animal = { species, exhibit };

   const normalized = RegionStore.normalizeSelectedAnimal(animal);

   assert.equal(normalized.id, [species, exhibit].join(ScheduleItemKeySeparator.VALUE));
   assert.equal(normalized.imageSrc, null);
});


test('Test_MergeAnimals_TestDuplicates_ExpectDedupedByKey', () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };

   const merged = RegionStore.mergeAnimals([lion], [lion, penguin]);

   assert.deepEqual(
      merged.map((animal) => animal.species).sort(),
      [lion.species, penguin.species].sort()
   );
});


test('Test_ShouldHideDuplicateSingleExhibit_TestMirrorRegionName_ExpectHidden', () => {
   const name = 'Americas';
   const region = { name, exhibits: [name] };

   const hidden = RegionStore.shouldHideDuplicateSingleExhibit(region);

   assert.equal(hidden, true);
});


test('Test_ShouldHideDuplicateSingleExhibit_TestMultipleExhibits_ExpectVisible', () => {
   const region = {
      name: 'Africa',
      exhibits: ['Africa Savanna', 'Africa Rainforest'],
   };

   const hidden = RegionStore.shouldHideDuplicateSingleExhibit(region);

   assert.equal(hidden, false);
});


test('Test_SelectedExhibitsNeedAnimalRebuild_TestEmptyAnimals_ExpectTrue', () => {
   const exhibit = 'Africa Savanna';
   const selectedExhibits = new Set([exhibit]);

   const needsRebuild = RegionStore.selectedExhibitsNeedAnimalRebuild(selectedExhibits, []);

   assert.equal(needsRebuild, true);
});


test('Test_SelectedExhibitsNeedAnimalRebuild_TestCoveredExhibit_ExpectFalse', () => {
   const exhibit = 'Africa Savanna';
   const selectedExhibits = new Set([exhibit]);
   const animals = [{ species: 'African Lion', exhibit }];

   const needsRebuild = RegionStore.selectedExhibitsNeedAnimalRebuild(selectedExhibits, animals);

   assert.equal(needsRebuild, false);
});


test('Test_SelectedExhibitsNeedAnimalRebuild_TestMissingExhibit_ExpectTrue', () => {
   const savanna = 'Africa Savanna';
   const eurasia = 'Eurasia Wilds';
   const selectedExhibits = new Set([savanna, eurasia]);
   const animals = [{ species: 'African Lion', exhibit: savanna }];

   const needsRebuild = RegionStore.selectedExhibitsNeedAnimalRebuild(selectedExhibits, animals);

   assert.equal(needsRebuild, true);
});


test('Test_DraftAnimalsCoverCatalogAnimals_TestFullCoverage_ExpectTrue', () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const cattle = { species: 'Watusi Cattle', exhibit: 'Africa Savanna' };
   const draft = [lion, cattle];
   const catalog = [lion, cattle];

   const covers = RegionStore.draftAnimalsCoverCatalogAnimals(draft, catalog);

   assert.equal(covers, true);
});


test('Test_DraftAnimalsCoverCatalogAnimals_TestMissingCatalogAnimal_ExpectFalse', () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const cattle = { species: 'Watusi Cattle', exhibit: 'Africa Savanna' };
   const catalog = [lion, cattle];

   const covers = RegionStore.draftAnimalsCoverCatalogAnimals([lion], catalog);

   assert.equal(covers, false);
});


test('Test_DraftAnimalsCoverCatalogAnimals_TestEmptyCatalog_ExpectTrue', () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };

   const covers = RegionStore.draftAnimalsCoverCatalogAnimals([lion], []);

   assert.equal(covers, true);
});


test('Test_CreateEmptyRegion_TestDefaults_ExpectEmptyNameAndExhibits', () => {
   const region = RegionStore.createEmptyRegion();

   assert.equal(region.name, '');
   assert.deepEqual(region.exhibits, []);
});


test('Test_NormalizeRegion_TestWhitespace_ExpectTrimmed', () => {
   const name = 'Africa';
   const exhibit = 'Africa Savanna';
   const region = { name: `  ${name}  `, exhibits: [` ${exhibit} `, ''] };

   const normalized = RegionStore.normalizeRegion(region);

   assert.equal(normalized.name, name);
   assert.deepEqual(normalized.exhibits, [exhibit]);
});


test('Test_NormalizeRegions_TestBlankName_ExpectOmitted', () => {
   const name = 'Africa';
   const exhibit = 'Africa Savanna';
   const regions = [
      { name: `  ${name}  `, exhibits: [exhibit] },
      { name: '   ', exhibits: ['Ignored'] },
   ];

   const normalized = RegionStore.normalizeRegions(regions);

   assert.equal(normalized.at(Position.FIRST).name, name);
   assert.deepEqual(normalized.at(Position.FIRST).exhibits, [exhibit]);
   assert.equal(normalized.length, 1);
});


test('Test_NormalizeSelectedAnimal_TestNull_ExpectNull', () => {
   const animal = null;

   const normalized = RegionStore.normalizeSelectedAnimal(animal);

   assert.equal(normalized, null);
});


test('Test_NormalizeSelectedAnimal_TestString_ExpectNull', () => {
   const animal = 'lion';

   const normalized = RegionStore.normalizeSelectedAnimal(animal);

   assert.equal(normalized, null);
});


test('Test_NormalizeSelectedAnimal_TestMissingSpecies_ExpectNull', () => {
   const animal = { exhibit: 'Africa' };

   const normalized = RegionStore.normalizeSelectedAnimal(animal);

   assert.equal(normalized, null);
});


test('Test_MakeSelectedAnimal_TestFields_ExpectStored', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'Overlook';
   const imageSrc = '../images/lion.png';
   const animal = {
      species,
      exhibit,
      enclosure_name: enclosureName,
      imageSrc: ` ${imageSrc} `,
   };

   const selected = RegionStore.makeSelectedAnimal(animal);

   assert.equal(selected.species, species);
   assert.equal(selected.exhibit, exhibit);
   assert.equal(selected.enclosure_name, enclosureName);
   assert.equal(selected.imageSrc, imageSrc);
   assert.equal(
      selected.id,
      [species, exhibit, enclosureName].join(ScheduleItemKeySeparator.VALUE)
   );
});


test('Test_BuildSelectedAnimalKey_TestNull_ExpectEmpty', () => {
   const animal = null;

   const key = RegionStore.buildSelectedAnimalKey(animal);

   assert.equal(key, '');
});


test('Test_ParseAnimalWireKey_TestEmpty_ExpectNull', () => {
   const wireKey = '';

   const parsed = RegionStore.parseAnimalWireKey(wireKey);

   assert.equal(parsed, null);
});


test('Test_ParseAnimalWireKey_TestMissingSpecies_ExpectNull', () => {
   const exhibit = 'Africa';
   const wireKey = `${ScheduleItemKeySeparator.VALUE}${exhibit}`;

   const parsed = RegionStore.parseAnimalWireKey(wireKey);

   assert.equal(parsed, null);
});


test('Test_IsRegionFullySelected_TestAllExhibits_ExpectTrue', () => {
   const name = 'Africa';
   const savanna = 'Africa Savanna';
   const rainforest = 'Africa Rainforest';
   const region = { name, exhibits: [savanna, rainforest] };
   const selectedExhibits = new Set([savanna, rainforest]);

   const isSelected = RegionStore.isRegionFullySelected(region, selectedExhibits);

   assert.equal(isSelected, true);
});


test('Test_IsRegionFullySelected_TestEmptyExhibits_ExpectFalse', () => {
   const region = { name: 'Empty', exhibits: [] };
   const selectedExhibits = new Set(['Africa Savanna']);

   const isSelected = RegionStore.isRegionFullySelected(region, selectedExhibits);

   assert.equal(isSelected, false);
});


test('Test_SyncRegionSelection_TestFullySelected_ExpectRegionAdded', () => {
   const name = 'Africa';
   const savanna = 'Africa Savanna';
   const rainforest = 'Africa Rainforest';
   const region = { name, exhibits: [savanna, rainforest] };
   const selectedRegionNames = new Set();
   const selectedExhibits = new Set([savanna, rainforest]);

   RegionStore.syncRegionSelection(region, selectedRegionNames, selectedExhibits);

   assert.equal(selectedRegionNames.has(name), true);
});


test('Test_SyncRegionSelection_TestPartial_ExpectRegionRemoved', () => {
   const name = 'Africa';
   const savanna = 'Africa Savanna';
   const rainforest = 'Africa Rainforest';
   const region = { name, exhibits: [savanna, rainforest] };
   const selectedRegionNames = new Set([name]);

   RegionStore.syncRegionSelection(region, selectedRegionNames, new Set([savanna]));

   assert.equal(selectedRegionNames.has(name), false);
});


test('Test_SyncRegionSelection_TestEmptyName_ExpectNoOp', () => {
   const selectedRegionNames = new Set();
   const selectedExhibits = new Set(['Africa Savanna']);

   RegionStore.syncRegionSelection(
      { name: '', exhibits: [] },
      selectedRegionNames,
      selectedExhibits
   );

   assert.equal(selectedRegionNames.size, 0);
});


test('Test_SelectedExhibitsNeedAnimalRebuild_TestEmpty_ExpectFalse', () => {
   const needsRebuild = RegionStore.selectedExhibitsNeedAnimalRebuild(new Set(), []);

   assert.equal(needsRebuild, false);
});


test('Test_BuildSelectedAnimalKey_TestMissingId_ExpectIdentityKey', () => {
   const originalNormalize = RegionStore.normalizeSelectedAnimal;
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   RegionStore.normalizeSelectedAnimal = () => ({
      species,
      exhibit,
      id: '',
   });

   try {
      const key = RegionStore.buildSelectedAnimalKey({ species });

      assert.equal(
         key,
         AnimalIdentity.buildAnimalIdentityStorageKey({
            species,
            exhibit,
         })
      );
   } finally {
      RegionStore.normalizeSelectedAnimal = originalNormalize;
   }
});
