import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemSearchRowTagger } from '../../../../scripts/itinerary/panel/scheduleItemSearchRowTagger.js';
import { WildEncounterScheduleItemKey } from '../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';


test('Test_ItineraryWildEncounterId_TestTimedRow_ExpectWire', () => {
   const giraffeRow = {
      name: 'Giraffe',
      start_time: '1:00 PM',
      end_time: '1:30 PM',
   };

   const encounterId = ScheduleItemSearchRowTagger.itineraryWildEncounterId(giraffeRow);

   assert.equal(encounterId, WildEncounterScheduleItemKey.fromRow(giraffeRow).toWire());
});


test('Test_ItineraryWildEncounterId_TestNameOnly_ExpectNull', () => {
   const giraffeRow = { name: 'Giraffe' };

   const encounterId = ScheduleItemSearchRowTagger.itineraryWildEncounterId(giraffeRow);

   assert.equal(encounterId, null);
});


test('Test_TagAnimalRows_TestRow_ExpectAnimalKind', () => {
   const row = { id: 1 };

   const tagged = ScheduleItemSearchRowTagger.tagAnimalRows([row]);

   assert.deepEqual(tagged, [{ ...row, scheduleItemKind: ScheduleItemKind.ANIMAL.itemType }]);
});


test('Test_TagAttractionRows_TestRow_ExpectAttractionKind', () => {
   const row = { id: 2 };

   const tagged = ScheduleItemSearchRowTagger.tagAttractionRows([row]);

   assert.deepEqual(tagged, [{ ...row, scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType }]);
});


test('Test_TagTransportationRows_TestRow_ExpectTransportationKind', () => {
   const row = { id: 3 };

   const tagged = ScheduleItemSearchRowTagger.tagTransportationRows([row]);

   assert.deepEqual(tagged, [{ ...row, scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType }]);
});


test('Test_TagGuardiansTalkRows_TestRow_ExpectTalkKind', () => {
   const row = { id: 4 };

   const tagged = ScheduleItemSearchRowTagger.tagGuardiansTalkRows([row]);

   assert.deepEqual(tagged, [{ ...row, scheduleItemKind: ScheduleItemKind.GUARDIANS_TALK.itemType }]);
});


test('Test_TagWildEncounterRows_TestRow_ExpectWildKind', () => {
   const row = { id: 5 };

   const tagged = ScheduleItemSearchRowTagger.tagWildEncounterRows([row]);

   assert.deepEqual(tagged, [{ ...row, scheduleItemKind: ScheduleItemKind.WILD_ENCOUNTER.itemType }]);
});
