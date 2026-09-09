import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import scheduleItemKindValues from '../../../../shared/enums/scheduleItemKind.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_ScheduleItemKind_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(scheduleItemKindValues)) {
      assert.deepEqual(ScheduleItemKind[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/scheduleItemKind.json'), 'utf8')
   );
   assert.deepEqual(scheduleItemKindValues, diskValues);
});

test('Test_ScheduleItemKindFromItemType_TestModuleAndKindStrings_ExpectMatchingKind', () => {
   assert.equal(
      ScheduleItemKind.scheduleItemKindFromItemType(ScheduleItemKind.ANIMAL.itemType),
      ScheduleItemKind.ANIMAL
   );
   assert.equal(
      ScheduleItemKind.scheduleItemKindFromItemType(ScheduleItemKind.ATTRACTION.itemType),
      ScheduleItemKind.ATTRACTION
   );
   assert.equal(
      ScheduleItemKind.scheduleItemKindFromItemType(ScheduleItemKind.ANIMAL.kind),
      ScheduleItemKind.ANIMAL
   );
});

test('Test_IsScheduleItemModuleItemType_TestModuleTypes_ExpectRecognizedOnly', () => {
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType(ScheduleItemKind.ANIMAL.itemType), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType(ScheduleItemKind.ATTRACTION.itemType), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType(ScheduleItemKind.TRANSPORTATION.itemType), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType(ScheduleItemKind.GUARDIANS_TALK.itemType), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType(ScheduleItemKind.WILD_ENCOUNTER.itemType), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType('lunch'), false);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType(ScheduleItemKind.ANIMAL.kind), false);
   assert.equal(
      ScheduleItemKind.isScheduleItemModuleItemType(`  ${ScheduleItemKind.ANIMAL.itemType.toUpperCase()}  `),
      true
   );
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType(null), false);
});

test('Test_IsFixedTimeScheduleItemKind_TestTalksAndEncounters_ExpectTrueOnly', () => {
   assert.equal(
      ScheduleItemKind.isFixedTimeScheduleItemKind(ScheduleItemKind.GUARDIANS_TALK.itemType),
      true
   );
   assert.equal(
      ScheduleItemKind.isFixedTimeScheduleItemKind(ScheduleItemKind.GUARDIANS_TALK.kind),
      true
   );
   assert.equal(
      ScheduleItemKind.isFixedTimeScheduleItemKind(ScheduleItemKind.WILD_ENCOUNTER.itemType),
      true
   );
   assert.equal(
      ScheduleItemKind.isFixedTimeScheduleItemKind(ScheduleItemKind.WILD_ENCOUNTER.kind),
      true
   );
   assert.equal(ScheduleItemKind.isFixedTimeScheduleItemKind(ScheduleItemKind.ANIMAL.itemType), false);
   assert.equal(ScheduleItemKind.isFixedTimeScheduleItemKind(ScheduleItemKind.ATTRACTION.itemType), false);
   assert.equal(ScheduleItemKind.isFixedTimeScheduleItemKind('lunch'), false);
});

test('Test_UsesScheduledTimelineEventCard_TestFixedTimeAndAttractions_ExpectTrue', () => {
   assert.equal(
      ScheduleItemKind.usesScheduledTimelineEventCard(ScheduleItemKind.GUARDIANS_TALK.itemType),
      true
   );
   assert.equal(
      ScheduleItemKind.usesScheduledTimelineEventCard(ScheduleItemKind.WILD_ENCOUNTER.kind),
      true
   );
   assert.equal(
      ScheduleItemKind.usesScheduledTimelineEventCard(ScheduleItemKind.ATTRACTION.itemType),
      true
   );
   assert.equal(
      ScheduleItemKind.usesScheduledTimelineEventCard(ScheduleItemKind.ATTRACTION.kind),
      true
   );
   assert.equal(
      ScheduleItemKind.usesScheduledTimelineEventCard(ScheduleItemKind.ANIMAL.itemType),
      false
   );
   assert.equal(
      ScheduleItemKind.isFixedTimeScheduleItemKind(ScheduleItemKind.ATTRACTION.itemType),
      false
   );
});

test('Test_ScheduleItemKindFromItemType_TestUnknownAndBlank_ExpectNullOrEvent', () => {
   assert.equal(ScheduleItemKind.scheduleItemKindFromItemType(ScheduleItemKind.EVENT.kind), ScheduleItemKind.EVENT);
   assert.equal(ScheduleItemKind.scheduleItemKindFromItemType('lunch'), null);
   assert.equal(ScheduleItemKind.scheduleItemKindFromItemType(''), null);
   assert.equal(ScheduleItemKind.scheduleItemKindFromItemType(null), null);
   assert.equal(
      ScheduleItemKind.scheduleItemKindFromItemType(`  ${ScheduleItemKind.ATTRACTION.kind.toUpperCase()}  `),
      ScheduleItemKind.ATTRACTION
   );
});

test('Test_ScheduleItemModuleItemTypeForKind_TestSchedulableKinds_ExpectItemTypes', () => {
   assert.equal(
      ScheduleItemKind.scheduleItemModuleItemTypeForKind(ScheduleItemKind.ANIMAL.kind),
      ScheduleItemKind.ANIMAL.itemType
   );
   assert.equal(
      ScheduleItemKind.scheduleItemModuleItemTypeForKind(ScheduleItemKind.ATTRACTION.kind),
      ScheduleItemKind.ATTRACTION.itemType
   );
   assert.equal(ScheduleItemKind.scheduleItemModuleItemTypeForKind(ScheduleItemKind.EVENT.kind), null);
   assert.equal(ScheduleItemKind.scheduleItemModuleItemTypeForKind(''), null);
   assert.equal(ScheduleItemKind.scheduleItemModuleItemTypeForKind(null), null);
});
