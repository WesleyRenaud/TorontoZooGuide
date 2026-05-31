import test from 'node:test';
import assert from 'node:assert/strict';

import {
   isScheduleItemModuleItemType,
   scheduleItemKindFromItemType,
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
});
