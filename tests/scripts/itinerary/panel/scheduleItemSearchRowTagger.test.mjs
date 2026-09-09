import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemSearchRowTagger } from '../../../../scripts/itinerary/panel/scheduleItemSearchRowTagger.js';
import { WildEncounterScheduleItemKey } from '../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';

test('Test_ItineraryWildEncounterId_TestRow_ExpectWireOrNull', () => {
   const giraffeRow = {
      name: 'Giraffe',
      start_time: '1:00 PM',
      end_time: '1:30 PM',
   };
   assert.equal(
      ScheduleItemSearchRowTagger.itineraryWildEncounterId(giraffeRow),
      WildEncounterScheduleItemKey.fromRow(giraffeRow).toWire()
   );
   assert.equal(ScheduleItemSearchRowTagger.itineraryWildEncounterId({ name: 'Giraffe' }), null);
});

test('Test_TagRowsByKind_TestCollections_ExpectTagged', () => {
   assert.deepEqual(ScheduleItemSearchRowTagger.tagAnimalRows([{ id: 1 }]), [
      { id: 1, scheduleItemKind: ScheduleItemKind.ANIMAL.itemType },
   ]);
   assert.deepEqual(ScheduleItemSearchRowTagger.tagAttractionRows([{ id: 2 }]), [
      { id: 2, scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType },
   ]);
   assert.deepEqual(ScheduleItemSearchRowTagger.tagTransportationRows([{ id: 3 }]), [
      { id: 3, scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType },
   ]);
   assert.deepEqual(ScheduleItemSearchRowTagger.tagGuardiansTalkRows([{ id: 4 }]), [
      { id: 4, scheduleItemKind: ScheduleItemKind.GUARDIANS_TALK.itemType },
   ]);
   assert.deepEqual(ScheduleItemSearchRowTagger.tagWildEncounterRows([{ id: 5 }]), [
      { id: 5, scheduleItemKind: ScheduleItemKind.WILD_ENCOUNTER.itemType },
   ]);
});
