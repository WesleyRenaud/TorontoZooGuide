import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerPlanController } from '../../../../scripts/itinerary/panel/dayPlannerPlanController.js';


test('Test_HasScheduledItineraryItems_TestEmpty_ExpectFalse', () => {
   const itinerary = {};

   const hasScheduled = DayPlannerPlanController.hasScheduledItineraryItems(itinerary);

   assert.equal(hasScheduled, false);
});


test('Test_HasScheduledItineraryItems_TestUnscheduledAnimal_ExpectFalse', () => {
   const itinerary = {
      animals: [{ species: 'Amur Tiger', exhibit: 'Eurasia Wilds' }],
   };

   const hasScheduled = DayPlannerPlanController.hasScheduledItineraryItems(itinerary);

   assert.equal(hasScheduled, false);
});


test('Test_HasScheduledItineraryItems_TestScheduledAnimal_ExpectTrue', () => {
   const itinerary = {
      animals: [{
         species: 'Amur Tiger',
         exhibit: 'Eurasia Wilds',
         start_time: '10:00',
         end_time: '10:30',
      }],
   };

   const hasScheduled = DayPlannerPlanController.hasScheduledItineraryItems(itinerary);

   assert.equal(hasScheduled, true);
});


test('Test_HasScheduledItineraryItems_TestScheduledEvent_ExpectTrue', () => {
   const itinerary = {
      events: [{
         event_type: 'lunch',
         start_time: '12:00',
         end_time: '12:30',
      }],
   };

   const hasScheduled = DayPlannerPlanController.hasScheduledItineraryItems(itinerary);

   assert.equal(hasScheduled, true);
});


test('Test_HasScheduledItineraryItems_TestScheduledTransportation_ExpectTrue', () => {
   const itinerary = {
      transportations: [{
         name: 'Zoomobile',
         start_time: '11:00',
         end_time: '11:20',
      }],
   };

   const hasScheduled = DayPlannerPlanController.hasScheduledItineraryItems(itinerary);

   assert.equal(hasScheduled, true);
});
