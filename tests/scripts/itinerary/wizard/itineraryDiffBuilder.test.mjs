import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDiffBuilder } from '../../../../scripts/itinerary/wizard/itineraryDiffBuilder.js';
import { TransportationSelectorModel } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { RemovedItems } from '../../../../scripts/itinerary/wizard/diff/removedItems.js';
import { AnimalPresenter } from '../../../../scripts/itinerary/wizard/diff/animalPresenter.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


test('Test_ValidatedAttractionPresenceItems_TestTransportAsAttraction_ExpectIncluded', () => {
   const original = TransportationSelectorModel.isTransportationAddedAsAttraction;
   TransportationSelectorModel.isTransportationAddedAsAttraction = (row) => row.addedAsAttraction;
   const carousel = { name: 'Carousel' };
   const zoomobile = { name: 'Zoomobile', addedAsAttraction: true };
   const shuttle = { name: 'Shuttle', addedAsAttraction: false };
   const validated = {
      attractions: [carousel],
      transportations: [zoomobile, shuttle],
   };

   try {
      const items = ItineraryDiffBuilder.validatedAttractionPresenceItems(validated);

      assert.deepEqual(items, [carousel, zoomobile]);
   } finally {
      TransportationSelectorModel.isTransportationAddedAsAttraction = original;
   }
});


test('Test_HasScheduleTimes_TestStartAndEnd_ExpectTrue', () => {
   const item = {
      start_time: '10:00 AM',
      end_time: '11:00 AM',
   };

   const hasTimes = ItineraryDiffBuilder.hasScheduleTimes(item);

   assert.equal(hasTimes, true);
});


test('Test_HasScheduleTimes_TestStartOnly_ExpectFalse', () => {
   const item = { start_time: '10:00 AM' };

   const hasTimes = ItineraryDiffBuilder.hasScheduleTimes(item);

   assert.equal(hasTimes, false);
});


test('Test_BuildUnscheduledItemsByKey_TestLostTimes_ExpectItems', () => {
   const carouselName = 'Carousel';
   const trainName = 'Train';
   const carouselStart = '10:00 AM';
   const carouselEnd = '11:00 AM';
   const trainStart = '1:00 PM';
   const trainEnd = '2:00 PM';
   const scheduledCarousel = {
      name: carouselName,
      start_time: carouselStart,
      end_time: carouselEnd,
   };
   const scheduledTrain = {
      name: trainName,
      start_time: trainStart,
      end_time: trainEnd,
   };
   const validatedCarousel = { name: carouselName };
   const validatedTrain = {
      name: trainName,
      start_time: trainStart,
      end_time: trainEnd,
   };

   const unscheduled = ItineraryDiffBuilder.buildUnscheduledItemsByKey(
      [scheduledCarousel, scheduledTrain],
      [validatedCarousel, validatedTrain],
      (item) => item.name
   );

   assert.deepEqual(unscheduled, [scheduledCarousel]);
});


test('Test_MergeRemovedItemLists_TestKeys_ExpectDeduped', () => {
   const first = { name: 'A' };
   const second = { name: 'B' };
   const existing = [first];
   const incoming = [first, second];

   const merged = ItineraryDiffBuilder.mergeRemovedItemLists(
      existing,
      incoming,
      (item) => item.name
   );

   assert.deepEqual(merged, [first, second]);
});


test('Test_BuildRemovedItems_TestDelegation_ExpectCalls', () => {
   const originalMerge = RemovedItems.mergeRemovedItems;
   const speciesKey = 'species';
   RemovedItems.mergeRemovedItems = (...args) => ({ merged: args[3] });
   const previous = { animals: [], attractions: [], guardiansTalks: [], wildEncounters: [] };
   const validated = {
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [],
   };
   const backendRemoved = {};

   try {
      const removed = ItineraryDiffBuilder.buildRemovedItems(
         previous,
         validated,
         backendRemoved
      );

      assert.equal(removed.animals.merged, speciesKey);
   } finally {
      RemovedItems.mergeRemovedItems = originalMerge;
   }
});


test('Test_BuildAnimalVisibilityDiff_TestDelegation_ExpectCalls', () => {
   const originalVisibility = AnimalPresenter.buildAnimalVisibilityChanges;
   const lion = { species: 'Lion' };
   const improved = [lion];
   AnimalPresenter.buildAnimalVisibilityChanges = () => ({ reduced: [], improved });
   const previous = { animals: [] };
   const validated = { animals: [] };
   const removed = { animals: [] };
   const minDelta = 0.2;

   try {
      const visibility = ItineraryDiffBuilder.buildAnimalVisibilityDiff(
         previous,
         validated,
         removed,
         minDelta
      );

      assert.deepEqual(visibility.improved, improved);
   } finally {
      AnimalPresenter.buildAnimalVisibilityChanges = originalVisibility;
   }
});


test('Test_BuildUnscheduledItems_TestAnimalsAndAttractions_ExpectBuckets', () => {
   const lion = {
      species: 'African Lion',
      exhibit: 'Savanna',
      start_time: '10:00 AM',
      end_time: '11:00 AM',
   };
   const carousel = {
      name: 'Carousel',
      start_time: '1:00 PM',
      end_time: '2:00 PM',
   };
   const previous = {
      animals: [lion],
      attractions: [carousel],
   };
   const validated = {
      animals: [{ species: lion.species, exhibit: lion.exhibit }],
      attractions: [{ name: carousel.name }],
      transportations: [],
   };

   const unscheduled = ItineraryDiffBuilder.buildUnscheduledItems(previous, validated);

   assert.equal(unscheduled.animals.length, 1);
   assert.equal(unscheduled.attractions.length, 1);
   assert.deepEqual(unscheduled.animals[Position.FIRST], lion);
   assert.deepEqual(unscheduled.attractions[Position.FIRST], carousel);
});
