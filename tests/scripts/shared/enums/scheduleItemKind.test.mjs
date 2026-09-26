import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import scheduleItemKindValues from '../../../../shared/enums/scheduleItemKind.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_ScheduleItemKind_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/scheduleItemKind.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(scheduleItemKindValues).map((key) => [key, ScheduleItemKind[key]])
   );

   assert.deepEqual(mapped, scheduleItemKindValues);
   assert.deepEqual(scheduleItemKindValues, diskValues);
});


test('Test_ScheduleItemKindFromItemType_TestAnimalItemType_ExpectAnimal', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;

   const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

   assert.equal(kind, ScheduleItemKind.ANIMAL);
});


test('Test_ScheduleItemKindFromItemType_TestAttractionItemType_ExpectAttraction', () => {
   const itemType = ScheduleItemKind.ATTRACTION.itemType;

   const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

   assert.equal(kind, ScheduleItemKind.ATTRACTION);
});


test('Test_ScheduleItemKindFromItemType_TestAnimalKind_ExpectAnimal', () => {
   const itemType = ScheduleItemKind.ANIMAL.kind;

   const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

   assert.equal(kind, ScheduleItemKind.ANIMAL);
});


test('Test_IsScheduleItemModuleItemType_TestAnimal_ExpectTrue', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;

   const isModuleType = ScheduleItemKind.isScheduleItemModuleItemType(itemType);

   assert.equal(isModuleType, true);
});


test('Test_IsScheduleItemModuleItemType_TestAttraction_ExpectTrue', () => {
   const itemType = ScheduleItemKind.ATTRACTION.itemType;

   const isModuleType = ScheduleItemKind.isScheduleItemModuleItemType(itemType);

   assert.equal(isModuleType, true);
});


test('Test_IsScheduleItemModuleItemType_TestTransportation_ExpectTrue', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;

   const isModuleType = ScheduleItemKind.isScheduleItemModuleItemType(itemType);

   assert.equal(isModuleType, true);
});


test('Test_IsScheduleItemModuleItemType_TestGuardiansTalk_ExpectTrue', () => {
   const itemType = ScheduleItemKind.GUARDIANS_TALK.itemType;

   const isModuleType = ScheduleItemKind.isScheduleItemModuleItemType(itemType);

   assert.equal(isModuleType, true);
});


test('Test_IsScheduleItemModuleItemType_TestWildEncounter_ExpectTrue', () => {
   const itemType = ScheduleItemKind.WILD_ENCOUNTER.itemType;

   const isModuleType = ScheduleItemKind.isScheduleItemModuleItemType(itemType);

   assert.equal(isModuleType, true);
});


test('Test_IsScheduleItemModuleItemType_TestLunch_ExpectFalse', () => {
   const itemType = 'lunch';

   const isModuleType = ScheduleItemKind.isScheduleItemModuleItemType(itemType);

   assert.equal(isModuleType, false);
});


test('Test_IsScheduleItemModuleItemType_TestAnimalKind_ExpectFalse', () => {
   const itemType = ScheduleItemKind.ANIMAL.kind;

   const isModuleType = ScheduleItemKind.isScheduleItemModuleItemType(itemType);

   assert.equal(isModuleType, false);
});


test('Test_IsScheduleItemModuleItemType_TestAnimalItemTypeUppercase_ExpectTrue', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;

   const isModuleType = ScheduleItemKind.isScheduleItemModuleItemType(`  ${itemType.toUpperCase()}  `);

   assert.equal(isModuleType, true);
});


test('Test_IsScheduleItemModuleItemType_TestNull_ExpectFalse', () => {
   const itemType = null;

   const isModuleType = ScheduleItemKind.isScheduleItemModuleItemType(itemType);

   assert.equal(isModuleType, false);
});


test('Test_IsFixedTimeScheduleItemKind_TestGuardiansTalkItemType_ExpectTrue', () => {
   const itemType = ScheduleItemKind.GUARDIANS_TALK.itemType;

   const isFixedTime = ScheduleItemKind.isFixedTimeScheduleItemKind(itemType);

   assert.equal(isFixedTime, true);
});


test('Test_IsFixedTimeScheduleItemKind_TestGuardiansTalkKind_ExpectTrue', () => {
   const itemType = ScheduleItemKind.GUARDIANS_TALK.kind;

   const isFixedTime = ScheduleItemKind.isFixedTimeScheduleItemKind(itemType);

   assert.equal(isFixedTime, true);
});


test('Test_IsFixedTimeScheduleItemKind_TestWildEncounterItemType_ExpectTrue', () => {
   const itemType = ScheduleItemKind.WILD_ENCOUNTER.itemType;

   const isFixedTime = ScheduleItemKind.isFixedTimeScheduleItemKind(itemType);

   assert.equal(isFixedTime, true);
});


test('Test_IsFixedTimeScheduleItemKind_TestWildEncounterKind_ExpectTrue', () => {
   const itemType = ScheduleItemKind.WILD_ENCOUNTER.kind;

   const isFixedTime = ScheduleItemKind.isFixedTimeScheduleItemKind(itemType);

   assert.equal(isFixedTime, true);
});


test('Test_IsFixedTimeScheduleItemKind_TestAnimal_ExpectFalse', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;

   const isFixedTime = ScheduleItemKind.isFixedTimeScheduleItemKind(itemType);

   assert.equal(isFixedTime, false);
});


test('Test_IsFixedTimeScheduleItemKind_TestAttraction_ExpectFalse', () => {
   const itemType = ScheduleItemKind.ATTRACTION.itemType;

   const isFixedTime = ScheduleItemKind.isFixedTimeScheduleItemKind(itemType);

   assert.equal(isFixedTime, false);
});


test('Test_IsFixedTimeScheduleItemKind_TestLunch_ExpectFalse', () => {
   const itemType = 'lunch';

   const isFixedTime = ScheduleItemKind.isFixedTimeScheduleItemKind(itemType);

   assert.equal(isFixedTime, false);
});


test('Test_UsesScheduledTimelineEventCard_TestGuardiansTalk_ExpectTrue', () => {
   const itemType = ScheduleItemKind.GUARDIANS_TALK.itemType;

   const usesCard = ScheduleItemKind.usesScheduledTimelineEventCard(itemType);

   assert.equal(usesCard, true);
});


test('Test_UsesScheduledTimelineEventCard_TestWildEncounterKind_ExpectTrue', () => {
   const itemType = ScheduleItemKind.WILD_ENCOUNTER.kind;

   const usesCard = ScheduleItemKind.usesScheduledTimelineEventCard(itemType);

   assert.equal(usesCard, true);
});


test('Test_UsesScheduledTimelineEventCard_TestAttractionItemType_ExpectTrue', () => {
   const itemType = ScheduleItemKind.ATTRACTION.itemType;

   const usesCard = ScheduleItemKind.usesScheduledTimelineEventCard(itemType);

   assert.equal(usesCard, true);
});


test('Test_UsesScheduledTimelineEventCard_TestAttractionKind_ExpectTrue', () => {
   const itemType = ScheduleItemKind.ATTRACTION.kind;

   const usesCard = ScheduleItemKind.usesScheduledTimelineEventCard(itemType);

   assert.equal(usesCard, true);
});


test('Test_UsesScheduledTimelineEventCard_TestAnimal_ExpectFalse', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;

   const usesCard = ScheduleItemKind.usesScheduledTimelineEventCard(itemType);

   assert.equal(usesCard, false);
});


test('Test_IsFixedTimeScheduleItemKind_TestAttractionNotFixed_ExpectFalse', () => {
   const itemType = ScheduleItemKind.ATTRACTION.itemType;

   const isFixedTime = ScheduleItemKind.isFixedTimeScheduleItemKind(itemType);

   assert.equal(isFixedTime, false);
});


test('Test_ScheduleItemKindFromItemType_TestEventKind_ExpectEvent', () => {
   const itemType = ScheduleItemKind.EVENT.kind;

   const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

   assert.equal(kind, ScheduleItemKind.EVENT);
});


test('Test_ScheduleItemKindFromItemType_TestLunch_ExpectNull', () => {
   const itemType = 'lunch';

   const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

   assert.equal(kind, null);
});


test('Test_ScheduleItemKindFromItemType_TestEmpty_ExpectNull', () => {
   const itemType = '';

   const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

   assert.equal(kind, null);
});


test('Test_ScheduleItemKindFromItemType_TestNull_ExpectNull', () => {
   const itemType = null;

   const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

   assert.equal(kind, null);
});


test('Test_ScheduleItemKindFromItemType_TestAttractionKindUppercase_ExpectAttraction', () => {
   const itemType = ScheduleItemKind.ATTRACTION.kind;

   const kind = ScheduleItemKind.scheduleItemKindFromItemType(`  ${itemType.toUpperCase()}  `);

   assert.equal(kind, ScheduleItemKind.ATTRACTION);
});


test('Test_ScheduleItemModuleItemTypeForKind_TestAnimal_ExpectItemType', () => {
   const kind = ScheduleItemKind.ANIMAL.kind;

   const itemType = ScheduleItemKind.scheduleItemModuleItemTypeForKind(kind);

   assert.equal(itemType, ScheduleItemKind.ANIMAL.itemType);
});


test('Test_ScheduleItemModuleItemTypeForKind_TestAttraction_ExpectItemType', () => {
   const kind = ScheduleItemKind.ATTRACTION.kind;

   const itemType = ScheduleItemKind.scheduleItemModuleItemTypeForKind(kind);

   assert.equal(itemType, ScheduleItemKind.ATTRACTION.itemType);
});


test('Test_ScheduleItemModuleItemTypeForKind_TestEvent_ExpectNull', () => {
   const kind = ScheduleItemKind.EVENT.kind;

   const itemType = ScheduleItemKind.scheduleItemModuleItemTypeForKind(kind);

   assert.equal(itemType, null);
});


test('Test_ScheduleItemModuleItemTypeForKind_TestEmpty_ExpectNull', () => {
   const kind = '';

   const itemType = ScheduleItemKind.scheduleItemModuleItemTypeForKind(kind);

   assert.equal(itemType, null);
});


test('Test_ScheduleItemModuleItemTypeForKind_TestNull_ExpectNull', () => {
   const kind = null;

   const itemType = ScheduleItemKind.scheduleItemModuleItemTypeForKind(kind);

   assert.equal(itemType, null);
});
