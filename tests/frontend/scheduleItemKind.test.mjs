import test from 'node:test';
import assert from 'node:assert/strict';

import {
   isFixedTimeScheduleItemKind,
   isScheduleItemModuleItemType,
   scheduleItemKindFromItemType,
   scheduleItemModuleItemTypeForKind,
   ScheduleItemKind,
   usesScheduledTimelineEventCard,
} from '../../scripts/shared/enums/scheduleItemKind.js';

test('ScheduleItemKind pairs kind with API itemType', () => {
   assert.equal(ScheduleItemKind.ANIMAL.kind, 'animal');
   assert.equal(ScheduleItemKind.ANIMAL.itemType, 'animals');
   assert.equal(ScheduleItemKind.ATTRACTION.kind, 'attraction');
   assert.equal(ScheduleItemKind.ATTRACTION.itemType, 'attractions');
});

test('scheduleItemKindFromItemType accepts module and kind strings', () => {
   assert.equal(
      scheduleItemKindFromItemType('animals'),
      ScheduleItemKind.ANIMAL
   );
   assert.equal(
      scheduleItemKindFromItemType('attractions'),
      ScheduleItemKind.ATTRACTION
   );
   assert.equal(
      scheduleItemKindFromItemType('animal'),
      ScheduleItemKind.ANIMAL
   );
});

test('isScheduleItemModuleItemType recognizes module item types only', () => {
   assert.equal(isScheduleItemModuleItemType('animals'), true);
   assert.equal(isScheduleItemModuleItemType('attractions'), true);
   assert.equal(isScheduleItemModuleItemType('transportations'), true);
   assert.equal(isScheduleItemModuleItemType('guardians_talks'), true);
   assert.equal(isScheduleItemModuleItemType('wild_encounters'), true);
   assert.equal(isScheduleItemModuleItemType('lunch'), false);
   assert.equal(isScheduleItemModuleItemType('animal'), false);
   assert.equal(isScheduleItemModuleItemType('  ANIMALS  '), true);
   assert.equal(isScheduleItemModuleItemType(null), false);
});

test('isFixedTimeScheduleItemKind applies to guardians talks and wild encounters only', () => {
   assert.equal(
      isFixedTimeScheduleItemKind(ScheduleItemKind.GUARDIANS_TALK.itemType),
      true
   );
   assert.equal(
      isFixedTimeScheduleItemKind(ScheduleItemKind.GUARDIANS_TALK.kind),
      true
   );
   assert.equal(
      isFixedTimeScheduleItemKind(ScheduleItemKind.WILD_ENCOUNTER.itemType),
      true
   );
   assert.equal(
      isFixedTimeScheduleItemKind(ScheduleItemKind.WILD_ENCOUNTER.kind),
      true
   );
   assert.equal(isFixedTimeScheduleItemKind(ScheduleItemKind.ANIMAL.itemType), false);
   assert.equal(isFixedTimeScheduleItemKind(ScheduleItemKind.ATTRACTION.itemType), false);
   assert.equal(isFixedTimeScheduleItemKind('lunch'), false);
});

test('usesScheduledTimelineEventCard covers fixed-time items and attractions', () => {
   assert.equal(
      usesScheduledTimelineEventCard(ScheduleItemKind.GUARDIANS_TALK.itemType),
      true
   );
   assert.equal(
      usesScheduledTimelineEventCard(ScheduleItemKind.WILD_ENCOUNTER.kind),
      true
   );
   assert.equal(
      usesScheduledTimelineEventCard(ScheduleItemKind.ATTRACTION.itemType),
      true
   );
   assert.equal(
      usesScheduledTimelineEventCard(ScheduleItemKind.ATTRACTION.kind),
      true
   );
   assert.equal(
      usesScheduledTimelineEventCard(ScheduleItemKind.ANIMAL.itemType),
      false
   );
   assert.equal(
      isFixedTimeScheduleItemKind(ScheduleItemKind.ATTRACTION.itemType),
      false
   );
});

test('scheduleItemKindFromItemType returns null for unknown and blank values', () => {
   assert.equal(scheduleItemKindFromItemType('event'), ScheduleItemKind.EVENT);
   assert.equal(scheduleItemKindFromItemType('lunch'), null);
   assert.equal(scheduleItemKindFromItemType(''), null);
   assert.equal(scheduleItemKindFromItemType(null), null);
   assert.equal(
      scheduleItemKindFromItemType('  ATTRACTION  '),
      ScheduleItemKind.ATTRACTION
   );
});

test('scheduleItemModuleItemTypeForKind maps schedulable kinds to API item types', () => {
   assert.equal(
      scheduleItemModuleItemTypeForKind('animal'),
      ScheduleItemKind.ANIMAL.itemType
   );
   assert.equal(
      scheduleItemModuleItemTypeForKind('attraction'),
      ScheduleItemKind.ATTRACTION.itemType
   );
   assert.equal(scheduleItemModuleItemTypeForKind('event'), null);
   assert.equal(scheduleItemModuleItemTypeForKind(''), null);
   assert.equal(scheduleItemModuleItemTypeForKind(null), null);
});
