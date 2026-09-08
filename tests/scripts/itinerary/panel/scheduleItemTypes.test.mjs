import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemTypes } from '../../../../scripts/itinerary/panel/scheduleItemTypes.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../scripts/strings.js';
import { ScheduleItemEventFormatter } from '../../../../scripts/itinerary/panel/scheduleItemEventFormatter.js';

test('Test_IsScheduleItemTypeUnset_TestPlaceholder_ExpectBoolean', () => {
   assert.equal(ScheduleItemTypes.isScheduleItemTypeUnset(''), true);
   assert.equal(ScheduleItemTypes.isScheduleItemTypeUnset('animals'), false);
});

test('Test_IsScheduleItemSearchEnabled_TestEventTypes_ExpectBoolean', () => {
   assert.equal(ScheduleItemTypes.isScheduleItemSearchEnabled('animals', ['arrival']), true);
   assert.equal(ScheduleItemTypes.isScheduleItemSearchEnabled('arrival', ['arrival']), false);
});

test('Test_BuildScheduleItemTypeOptions_TestEvents_ExpectOptions', () => {
   const original = ScheduleItemEventFormatter.formatItineraryEventTypeLabel;
   ScheduleItemEventFormatter.formatItineraryEventTypeLabel = (value) => `Label:${value}`;

   try {
      const options = ScheduleItemTypes.buildScheduleItemTypeOptions(['arrival'], {
         typePlaceholder: 'Pick type',
      });

      assert.equal(options[0].value, '');
      assert.equal(options[0].label, 'Pick type');
      assert.equal(options[0].selected, true);
      assert.deepEqual(options[1], { value: 'arrival', label: 'Label:arrival' });
      assert.ok(options.some((option) => option.value === ScheduleItemKind.ANIMAL.itemType
         && option.label === Strings.entityLabels.animal));
      assert.ok(options.some((option) => option.value === ScheduleItemKind.WILD_ENCOUNTER.itemType));
   } finally {
      ScheduleItemEventFormatter.formatItineraryEventTypeLabel = original;
   }
});

test('Test_BuildScheduleItemTypeOptions_TestDefaults_ExpectEmptyPlaceholder', () => {
   const original = ScheduleItemEventFormatter.formatItineraryEventTypeLabel;
   ScheduleItemEventFormatter.formatItineraryEventTypeLabel = (value) => value;

   try {
      const options = ScheduleItemTypes.buildScheduleItemTypeOptions();
      assert.equal(options[0].label, '');
      assert.equal(options[0].value, ScheduleItemTypes.SCHEDULE_ITEM_TYPE_PLACEHOLDER);
      assert.equal(
         options.some((option) => option.value === ScheduleItemKind.ATTRACTION.itemType),
         true
      );
   } finally {
      ScheduleItemEventFormatter.formatItineraryEventTypeLabel = original;
   }
});
