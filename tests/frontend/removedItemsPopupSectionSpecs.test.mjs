import assert from 'node:assert/strict';
import test from 'node:test';

import {
   getRemovedItemsPopupSectionSpecs,
   getUnscheduledSectionSpecs,
   hasRemovedItemsPopupContent,
   resolveKeepOverride,
} from '../../scripts/itinerary/panel/components/removedItemsPopupSectionSpecs.js';
import { APP_STRINGS } from '../../scripts/strings.js';

const removedAnimal = {
   species: 'African Lion',
   exhibit: 'Africa Savanna',
};

const removedAttraction = {
   name: 'Conservation Carousel',
};

test('hasRemovedItemsPopupContent is false when every section is empty', () => {
   assert.equal(hasRemovedItemsPopupContent({}), false);
   assert.equal(
      hasRemovedItemsPopupContent({
         added: { animals: [] },
         removed: { animals: [] },
         adjustments: [],
      }),
      false
   );
});

test('hasRemovedItemsPopupContent detects adjustments and removed animals', () => {
   assert.equal(
      hasRemovedItemsPopupContent({
         adjustments: [{
            type: 'arrivalTimeAdjusted',
            previousValue: '09:00',
            value: '09:30',
         }],
      }),
      true
   );
   assert.equal(
      hasRemovedItemsPopupContent({
         removed: { animals: [removedAnimal] },
      }),
      true
   );
});

test('getUnscheduledSectionSpecs emits only populated unscheduled groups', () => {
   assert.deepEqual(
      getUnscheduledSectionSpecs({
         animals: [removedAnimal],
         wildEncounters: [],
      }).map((section) => section.title),
      [APP_STRINGS.itinerary.dayPlanner.unscheduledTitle]
   );
   assert.deepEqual(
      getUnscheduledSectionSpecs({
         attractions: [removedAttraction],
         guardiansTalks: [{ name: 'African Lion' }],
      }).map((section) => section.title),
      [
         APP_STRINGS.map.filter.attractions,
         APP_STRINGS.site.nav.meetTheGuardians,
      ]
   );
});

test('getRemovedItemsPopupSectionSpecs includes keep overrides for removed rows', () => {
   const sections = getRemovedItemsPopupSectionSpecs({
      removed: {
         animals: [removedAnimal],
         attractions: [removedAttraction],
      },
   });

   const removedAnimalSection = sections.find(
      section => section.title === APP_STRINGS.itinerary.removedItems.animalsRemovedTitle
   );
   const removedAttractionSection = sections.find(
      section => section.title === APP_STRINGS.map.filter.attractions
         && section.keepOverrideKey === 'attraction'
   );

   assert.equal(removedAnimalSection?.keepOverrideKey, 'animal');
   assert.equal(removedAttractionSection?.keepOverrideKey, 'attraction');
   assert.equal(removedAnimalSection?.items.length, 1);
   assert.equal(removedAttractionSection?.items.length, 1);
});

test('resolveKeepOverride maps animal and attraction sections to keep handlers', () => {
   const animalHandlers = {
      onToggleKeepAnimal: () => {},
      isKeepAnimalSelected: () => false,
   };
   const attractionHandlers = {
      onToggleKeepAttraction: () => {},
      isKeepAttractionSelected: () => true,
   };

   const animalOverride = resolveKeepOverride(
      { keepOverrideKey: 'animal' },
      animalHandlers
   );
   const attractionOverride = resolveKeepOverride(
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
      resolveKeepOverride({ keepOverrideKey: 'wildEncounter' }, animalHandlers),
      null
   );
});
