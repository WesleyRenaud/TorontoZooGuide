import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemController } from '../../../../scripts/itinerary/panel/scheduleItemController.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { ScheduleItemKeySeparator } from '../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { TransportationScheduleItemKey } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';
import { installScheduleItemActionsTestHooks } from '../../helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();


test('Test_BuildAnimalDraftEntry_TestSpeciesAndExhibit_ExpectEntry', () => {
   const species = 'Amur Tiger';
   const exhibit = 'Eurasia Wilds';
   const row = { species, exhibit };

   const entry = ScheduleItemController.buildAnimalDraftEntry(row);

   assert.deepEqual(entry, { species, exhibit });
});


test('Test_BuildAnimalDraftEntry_TestMissingExhibit_ExpectNull', () => {
   const row = { species: 'Amur Tiger' };

   const entry = ScheduleItemController.buildAnimalDraftEntry(row);

   assert.equal(entry, null);
});


test('Test_BuildAttractionDraftEntry_TestName_ExpectName', () => {
   const name = 'Conservation Carousel';
   const row = { name };

   const entry = ScheduleItemController.buildAttractionDraftEntry(row);

   assert.equal(entry, name);
});


test('Test_BuildAttractionDraftEntry_TestBlankName_ExpectNull', () => {
   const row = { name: '' };

   const entry = ScheduleItemController.buildAttractionDraftEntry(row);

   assert.equal(entry, null);
});


test('Test_BuildScheduleItemRequest_TestEventType_ExpectPayload', () => {
   const itemType = 'lunch';
   const eventTypes = [itemType];

   const request = ScheduleItemController.buildScheduleItemRequest(itemType, null, eventTypes);

   assert.deepEqual(request, { itemType, key: '' });
});


test('Test_BuildScheduleItemRequest_TestAnimalRow_ExpectPayload', () => {
   const species = 'Amur Tiger';
   const exhibit = 'Eurasia Wilds';
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const row = {
      species,
      exhibit,
      scheduleItemKind: itemType,
   };

   const request = ScheduleItemController.buildScheduleItemRequest(itemType, row, []);

   assert.deepEqual(request, {
      itemType,
      key: [species, exhibit].join(ScheduleItemKeySeparator.VALUE),
   });
});


test('Test_BuildScheduleItemRequest_TestAttractionRow_ExpectPayload', () => {
   const name = 'Zoomobile';
   const itemType = ScheduleItemKind.ATTRACTION.itemType;
   const row = {
      name,
      added_as_attraction: true,
      scheduleItemKind: itemType,
   };

   const request = ScheduleItemController.buildScheduleItemRequest(itemType, row, []);

   assert.deepEqual(request, { itemType, key: name });
});


test('Test_BuildScheduleItemRequest_TestTransportationRow_ExpectPayload', () => {
   const name = 'Zoomobile';
   const addedAsAttraction = false;
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const row = {
      name,
      added_as_attraction: addedAsAttraction,
      scheduleItemKind: itemType,
   };

   const request = ScheduleItemController.buildScheduleItemRequest(itemType, row, []);

   assert.deepEqual(request, {
      itemType,
      key: new TransportationScheduleItemKey(name, addedAsAttraction).toWire(),
   });
});


test('Test_BuildScheduleItemRequest_TestEventTimes_ExpectTimes', () => {
   const itemType = 'lunch';
   const startTime = '10:00 AM';
   const durationMinutes = 20;

   const request = ScheduleItemController.buildScheduleItemRequest(itemType, null, [itemType], {
      startTime,
      durationMinutes,
   });

   assert.deepEqual(request, {
      itemType,
      key: '',
      startTime,
      durationMinutes,
   });
});


test('Test_BuildScheduleItemRequest_TestAnimalDuration_ExpectDuration', () => {
   const species = 'Amur Tiger';
   const exhibit = 'Eurasia Wilds';
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const durationMinutes = 20;
   const row = {
      species,
      exhibit,
      scheduleItemKind: itemType,
   };

   const request = ScheduleItemController.buildScheduleItemRequest(itemType, row, [], { durationMinutes });

   assert.deepEqual(request, {
      itemType,
      key: [species, exhibit].join(ScheduleItemKeySeparator.VALUE),
      durationMinutes,
   });
});
