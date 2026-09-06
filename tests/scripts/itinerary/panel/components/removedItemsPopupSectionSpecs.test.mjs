import assert from 'node:assert/strict';
import test from 'node:test';

import { RemovedItemsPopupSectionSpecs } from '../../../../../scripts/itinerary/panel/components/removedItemsPopupSectionSpecs.js';
import { Strings } from '../../../../../scripts/strings.js';

const removedAnimal = {
   species: 'African Lion',
   exhibit: 'Africa Savanna',
};

const removedAttraction = {
   name: 'Conservation Carousel',
};

test('Test_HasRemovedItemsPopupContent_TestIsFalseWhenEverySectionIsEmpty_ExpectOk', () => {
   assert.equal(RemovedItemsPopupSectionSpecs.hasRemovedItemsPopupContent({}), false);
   assert.equal(
      RemovedItemsPopupSectionSpecs.hasRemovedItemsPopupContent({
         added: { animals: [] },
         removed: { animals: [] },
         adjustments: [],
      }),
      false
   );
});

test('Test_HasRemovedItemsPopupContent_TestDetectsAdjustmentsAndRemovedAnimals_ExpectOk', () => {
   assert.equal(
      RemovedItemsPopupSectionSpecs.hasRemovedItemsPopupContent({
         adjustments: [{
            type: 'arrivalTimeAdjusted',
            previousValue: '09:00',
            value: '09:30',
         }],
      }),
      true
   );
   assert.equal(
      RemovedItemsPopupSectionSpecs.hasRemovedItemsPopupContent({
         removed: { animals: [removedAnimal] },
      }),
      true
   );
});

test('Test_GetUnscheduledSectionSpecs_TestEmitsOnlyPopulatedUnscheduledGroups_ExpectOk', () => {
   assert.deepEqual(
      RemovedItemsPopupSectionSpecs.getUnscheduledSectionSpecs({
         animals: [removedAnimal],
      }).map((section) => section.title),
      [Strings.itinerary.dayPlanner.unscheduledTitle]
   );
   assert.deepEqual(
      RemovedItemsPopupSectionSpecs.getUnscheduledSectionSpecs({
         attractions: [removedAttraction],
      }).map((section) => section.title),
      [Strings.map.filter.attractions]
   );
});

test('Test_GetRemovedItemsPopupSectionSpecs_TestIncludesKeepOverridesForRemovedRows_ExpectOk', () => {
   const sections = RemovedItemsPopupSectionSpecs.getRemovedItemsPopupSectionSpecs({
      removed: {
         animals: [removedAnimal],
         attractions: [removedAttraction],
      },
   });

   const removedAnimalSection = sections.find(
      section => section.title === Strings.itinerary.removedItems.animalsRemovedTitle
   );
   const removedAttractionSection = sections.find(
      section => section.title === Strings.map.filter.attractions
         && section.keepOverrideKey === 'attraction'
   );

   assert.equal(removedAnimalSection?.keepOverrideKey, 'animal');
   assert.equal(removedAttractionSection?.keepOverrideKey, 'attraction');
   assert.equal(removedAnimalSection?.items.length, 1);
   assert.equal(removedAttractionSection?.items.length, 1);
});

test('Test_ResolveKeepOverride_TestMapsAnimalAndAttractionSectionsToKeepHandlers_ExpectOk', () => {
   const animalHandlers = {
      onToggleKeepAnimal: () => {},
      isKeepAnimalSelected: () => false,
   };
   const attractionHandlers = {
      onToggleKeepAttraction: () => {},
      isKeepAttractionSelected: () => true,
   };

   const animalOverride = RemovedItemsPopupSectionSpecs.resolveKeepOverride(
      { keepOverrideKey: 'animal' },
      animalHandlers
   );
   const attractionOverride = RemovedItemsPopupSectionSpecs.resolveKeepOverride(
      { keepOverrideKey: 'attraction' },
      attractionHandlers
   );

   assert.equal(
      animalOverride?.buildKey({ species: 'Lion', exhibit: 'Savanna' }),
      'lion|savanna'
   );
   assert.equal(animalOverride?.isSelected, animalHandlers.isKeepAnimalSelected);
   assert.equal(
      attractionOverride?.buildKey({ name: 'Carousel' }),
      'carousel'
   );
   assert.equal(
      RemovedItemsPopupSectionSpecs.resolveKeepOverride({ keepOverrideKey: 'wildEncounter' }, animalHandlers),
      null
   );
});
