import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupSectionBuilder } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupSectionBuilder.js';
import { SpeciesExhibitKey } from '../../../../../scripts/itinerary/speciesExhibitKey.js';
import { ItemKey } from '../../../../../scripts/itinerary/wizard/diff/itemKey.js';
import { ItineraryAdjustmentType } from '../../../../../scripts/shared/enums/itineraryAdjustmentType.js';
import { Strings } from '../../../../../scripts/strings.js';

const _removedAnimal = {
   species: 'African Lion',
   exhibit: 'Africa Savanna',
};

const _removedAttraction = {
   name: 'Conservation Carousel',
};


test('Test_HasRemovedItemsPopupContent_TestEmptyObject_ExpectFalse', () => {
   const hasContent = RemovedItemsPopupSectionBuilder.hasRemovedItemsPopupContent({});

   assert.equal(hasContent, false);
});


test('Test_HasRemovedItemsPopupContent_TestEmptyCollections_ExpectFalse', () => {
   const hasContent = RemovedItemsPopupSectionBuilder.hasRemovedItemsPopupContent({
      added: { animals: [] },
      removed: { animals: [] },
      adjustments: [],
   });

   assert.equal(hasContent, false);
});


test('Test_HasRemovedItemsPopupContent_TestAdjustments_ExpectTrue', () => {
   const hasContent = RemovedItemsPopupSectionBuilder.hasRemovedItemsPopupContent({
      adjustments: [{
         type: ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
         previousValue: '09:00',
         value: '09:30',
      }],
   });

   assert.equal(hasContent, true);
});


test('Test_HasRemovedItemsPopupContent_TestRemovedAnimals_ExpectTrue', () => {
   const hasContent = RemovedItemsPopupSectionBuilder.hasRemovedItemsPopupContent({
      removed: { animals: [_removedAnimal] },
   });

   assert.equal(hasContent, true);
});


test('Test_GetUnscheduledSectionSpecs_TestAnimals_ExpectUnscheduledTitle', () => {
   const sections = RemovedItemsPopupSectionBuilder.getUnscheduledSectionSpecs({
      animals: [_removedAnimal],
   });

   assert.deepEqual(
      sections.map((section) => section.title),
      [Strings.itinerary.dayPlanner.unscheduledTitle]
   );
});


test('Test_GetUnscheduledSectionSpecs_TestAttractions_ExpectAttractionsTitle', () => {
   const sections = RemovedItemsPopupSectionBuilder.getUnscheduledSectionSpecs({
      attractions: [_removedAttraction],
   });

   assert.deepEqual(
      sections.map((section) => section.title),
      [Strings.map.filter.attractions]
   );
});


test('Test_GetRemovedItemsPopupSectionSpecs_TestRemovedRows_ExpectKeepOverrides', () => {
   const sections = RemovedItemsPopupSectionBuilder.getRemovedItemsPopupSectionSpecs({
      removed: {
         animals: [_removedAnimal],
         attractions: [_removedAttraction],
      },
   });
   const removedAnimalSection = sections.find(
      (section) => section.title === Strings.itinerary.removedItems.animalsRemovedTitle
   );
   const removedAttractionSection = sections.find(
      (section) => section.title === Strings.itinerary.removedItems.attractionsRemovedTitle
         && section.keepOverrideKey === 'attraction'
   );

   assert.equal(removedAnimalSection?.keepOverrideKey, 'animal');
   assert.equal(removedAttractionSection?.keepOverrideKey, 'attraction');
   assert.equal(removedAnimalSection?.items.length, 1);
   assert.equal(removedAttractionSection?.items.length, 1);
});


test('Test_ResolveKeepOverride_TestAnimal_ExpectAnimalHandlers', () => {
   const animal = { species: 'African Lion', exhibit: 'Savanna' };
   const animalHandlers = {
      onToggleKeepAnimal: () => {},
      isKeepAnimalSelected: () => false,
   };

   const animalOverride = RemovedItemsPopupSectionBuilder.resolveKeepOverride(
      { keepOverrideKey: 'animal' },
      animalHandlers
   );

   assert.equal(
      animalOverride?.buildKey(animal),
      SpeciesExhibitKey.buildSpeciesExhibitKey(animal)
   );
   assert.equal(animalOverride?.isSelected, animalHandlers.isKeepAnimalSelected);
});


test('Test_ResolveKeepOverride_TestAttraction_ExpectAttractionHandlers', () => {
   const attraction = { name: 'Conservation Carousel' };
   const attractionHandlers = {
      onToggleKeepAttraction: () => {},
      isKeepAttractionSelected: () => true,
   };

   const attractionOverride = RemovedItemsPopupSectionBuilder.resolveKeepOverride(
      { keepOverrideKey: 'attraction' },
      attractionHandlers
   );

   assert.equal(
      attractionOverride?.buildKey(attraction),
      ItemKey.buildItemKey(attraction, 'name')
   );
});


test('Test_ResolveKeepOverride_TestWildEncounter_ExpectNull', () => {
   const animalHandlers = {
      onToggleKeepAnimal: () => {},
      isKeepAnimalSelected: () => false,
   };

   const override = RemovedItemsPopupSectionBuilder.resolveKeepOverride(
      { keepOverrideKey: 'wildEncounter' },
      animalHandlers
   );

   assert.equal(override, null);
});
