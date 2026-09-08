import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDiffBuilder } from '../../../../scripts/itinerary/wizard/itineraryDiffBuilder.js';
import { TransportationSelectorModel } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { RemovedItems } from '../../../../scripts/itinerary/wizard/diff/removedItems.js';
import { AnimalPresenter } from '../../../../scripts/itinerary/wizard/diff/animalPresenter.js';

test('Test_ValidatedAttractionPresenceItems_TestTransportAsAttraction_ExpectIncluded', () => {
   const original = TransportationSelectorModel.isTransportationAddedAsAttraction;
   TransportationSelectorModel.isTransportationAddedAsAttraction = (row) => row.addedAsAttraction;

   try {
      assert.deepEqual(
         ItineraryDiffBuilder.validatedAttractionPresenceItems({
            attractions: [{ name: 'Carousel' }],
            transportations: [
               { name: 'Zoomobile', addedAsAttraction: true },
               { name: 'Shuttle', addedAsAttraction: false },
            ],
         }),
         [
            { name: 'Carousel' },
            { name: 'Zoomobile', addedAsAttraction: true },
         ]
      );
   } finally {
      TransportationSelectorModel.isTransportationAddedAsAttraction = original;
   }
});

test('Test_HasScheduleTimes_TestItem_ExpectBoolean', () => {
   assert.equal(ItineraryDiffBuilder.hasScheduleTimes({
      start_time: '10:00 AM',
      end_time: '11:00 AM',
   }), true);
   assert.equal(ItineraryDiffBuilder.hasScheduleTimes({ start_time: '10:00 AM' }), false);
});

test('Test_BuildUnscheduledItemsByKey_TestLostTimes_ExpectItems', () => {
   const unscheduled = ItineraryDiffBuilder.buildUnscheduledItemsByKey(
      [
         { name: 'Carousel', start_time: '10:00 AM', end_time: '11:00 AM' },
         { name: 'Train', start_time: '1:00 PM', end_time: '2:00 PM' },
      ],
      [
         { name: 'Carousel' },
         { name: 'Train', start_time: '1:00 PM', end_time: '2:00 PM' },
      ],
      (item) => item.name
   );

   assert.deepEqual(unscheduled, [{
      name: 'Carousel',
      start_time: '10:00 AM',
      end_time: '11:00 AM',
   }]);
});

test('Test_MergeRemovedItemLists_TestKeys_ExpectDeduped', () => {
   assert.deepEqual(
      ItineraryDiffBuilder.mergeRemovedItemLists(
         [{ name: 'A' }],
         [{ name: 'A' }, { name: 'B' }],
         (item) => item.name
      ),
      [{ name: 'A' }, { name: 'B' }]
   );
});

test('Test_BuildRemovedItemsAndVisibility_TestDelegation_ExpectCalls', () => {
   const originalMerge = RemovedItems.mergeRemovedItems;
   const originalVisibility = AnimalPresenter.buildAnimalVisibilityChanges;
   RemovedItems.mergeRemovedItems = (...args) => ({ merged: args[3] });
   AnimalPresenter.buildAnimalVisibilityChanges = () => ({ reduced: [], improved: [{ species: 'Lion' }] });

   try {
      const removed = ItineraryDiffBuilder.buildRemovedItems(
         { animals: [], attractions: [], guardiansTalks: [], wildEncounters: [] },
         { animals: [], attractions: [], guardiansTalks: [], wildEncounters: [], transportations: [] },
         {}
      );
      assert.equal(removed.animals.merged, 'species');

      const visibility = ItineraryDiffBuilder.buildAnimalVisibilityDiff(
         { animals: [] },
         { animals: [] },
         { animals: [] },
         0.2
      );
      assert.deepEqual(visibility.improved, [{ species: 'Lion' }]);
   } finally {
      RemovedItems.mergeRemovedItems = originalMerge;
      AnimalPresenter.buildAnimalVisibilityChanges = originalVisibility;
   }
});

test('Test_BuildUnscheduledItems_TestAnimalsAndAttractions_ExpectBuckets', () => {
   const unscheduled = ItineraryDiffBuilder.buildUnscheduledItems(
      {
         animals: [{
            species: 'African Lion',
            exhibit: 'Savanna',
            start_time: '10:00 AM',
            end_time: '11:00 AM',
         }],
         attractions: [{
            name: 'Carousel',
            start_time: '1:00 PM',
            end_time: '2:00 PM',
         }],
      },
      {
         animals: [{ species: 'African Lion', exhibit: 'Savanna' }],
         attractions: [{ name: 'Carousel' }],
         transportations: [],
      }
   );

   assert.equal(unscheduled.animals.length, 1);
   assert.equal(unscheduled.attractions.length, 1);
});
