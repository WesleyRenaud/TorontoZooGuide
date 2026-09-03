import test from 'node:test';
import assert from 'node:assert/strict';

import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';

test('ScheduleItemKind pairs kind with API itemType', () => {
   assert.equal(ScheduleItemKind.ANIMAL.kind, 'animal');
   assert.equal(ScheduleItemKind.ANIMAL.itemType, 'animals');
   assert.equal(ScheduleItemKind.ATTRACTION.kind, 'attraction');
   assert.equal(ScheduleItemKind.ATTRACTION.itemType, 'attractions');
});

test('ScheduleItemKind.scheduleItemKindFromItemType accepts module and kind strings', () => {
   assert.equal(
      ScheduleItemKind.scheduleItemKindFromItemType('animals'),
      ScheduleItemKind.ANIMAL
   );
   assert.equal(
      ScheduleItemKind.scheduleItemKindFromItemType('attractions'),
      ScheduleItemKind.ATTRACTION
   );
   assert.equal(
      ScheduleItemKind.scheduleItemKindFromItemType('animal'),
      ScheduleItemKind.ANIMAL
   );
});

test('ScheduleItemKind.isScheduleItemModuleItemType recognizes module item types only', () => {
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType('animals'), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType('attractions'), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType('transportations'), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType('guardians_talks'), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType('wild_encounters'), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType('lunch'), false);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType('animal'), false);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType('  ANIMALS  '), true);
   assert.equal(ScheduleItemKind.isScheduleItemModuleItemType(null), false);
});

test('ScheduleItemKind.isFixedTimeScheduleItemKind applies to guardians talks and wild encounters only', () => {
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

test('ScheduleItemKind.usesScheduledTimelineEventCard covers fixed-time items and attractions', () => {
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

test('ScheduleItemKind.scheduleItemKindFromItemType returns null for unknown and blank values', () => {
   assert.equal(ScheduleItemKind.scheduleItemKindFromItemType('event'), ScheduleItemKind.EVENT);
   assert.equal(ScheduleItemKind.scheduleItemKindFromItemType('lunch'), null);
   assert.equal(ScheduleItemKind.scheduleItemKindFromItemType(''), null);
   assert.equal(ScheduleItemKind.scheduleItemKindFromItemType(null), null);
   assert.equal(
      ScheduleItemKind.scheduleItemKindFromItemType('  ATTRACTION  '),
      ScheduleItemKind.ATTRACTION
   );
});

test('ScheduleItemKind.scheduleItemModuleItemTypeForKind maps schedulable kinds to API item types', () => {
   assert.equal(
      ScheduleItemKind.scheduleItemModuleItemTypeForKind('animal'),
      ScheduleItemKind.ANIMAL.itemType
   );
   assert.equal(
      ScheduleItemKind.scheduleItemModuleItemTypeForKind('attraction'),
      ScheduleItemKind.ATTRACTION.itemType
   );
   assert.equal(ScheduleItemKind.scheduleItemModuleItemTypeForKind('event'), null);
   assert.equal(ScheduleItemKind.scheduleItemModuleItemTypeForKind(''), null);
   assert.equal(ScheduleItemKind.scheduleItemModuleItemTypeForKind(null), null);
});
