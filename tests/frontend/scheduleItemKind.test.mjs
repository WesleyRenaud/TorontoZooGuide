import test from 'node:test';
import assert from 'node:assert/strict';

import {
   isScheduleItemModuleItemType,
   scheduleItemKindFromItemType,
   scheduleItemModuleItemTypeForKind,
   ScheduleItemKind,
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
   assert.equal(isScheduleItemModuleItemType('lunch'), false);
   assert.equal(isScheduleItemModuleItemType('animal'), false);
   assert.equal(isScheduleItemModuleItemType('  ANIMALS  '), true);
   assert.equal(isScheduleItemModuleItemType(null), false);
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
