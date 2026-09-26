import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemEventFormatter } from '../../../../scripts/itinerary/panel/scheduleItemEventFormatter.js';
import { ScheduleItemTypes } from '../../../../scripts/itinerary/panel/scheduleItemTypes.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_IsScheduleItemTypeUnset_TestPlaceholder_ExpectTrue', () => {
   const selection = ScheduleItemTypes.SCHEDULE_ITEM_TYPE_PLACEHOLDER;

   const isUnset = ScheduleItemTypes.isScheduleItemTypeUnset(selection);

   assert.equal(isUnset, true);
});


test('Test_IsScheduleItemTypeUnset_TestAnimals_ExpectFalse', () => {
   const selection = ScheduleItemKind.ANIMAL.itemType;

   const isUnset = ScheduleItemTypes.isScheduleItemTypeUnset(selection);

   assert.equal(isUnset, false);
});


test('Test_IsScheduleItemSearchEnabled_TestAnimals_ExpectTrue', () => {
   const selection = ScheduleItemKind.ANIMAL.itemType;
   const eventTypes = ['arrival'];

   const isEnabled = ScheduleItemTypes.isScheduleItemSearchEnabled(selection, eventTypes);

   assert.equal(isEnabled, true);
});


test('Test_IsScheduleItemSearchEnabled_TestArrivalEvent_ExpectFalse', () => {
   const selection = 'arrival';
   const eventTypes = [selection];

   const isEnabled = ScheduleItemTypes.isScheduleItemSearchEnabled(selection, eventTypes);

   assert.equal(isEnabled, false);
});


test('Test_BuildScheduleItemTypeOptions_TestEvents_ExpectOptions', () => {
   const original = ScheduleItemEventFormatter.formatItineraryEventTypeLabel;
   const eventType = 'arrival';
   const typePlaceholder = 'Pick type';
   ScheduleItemEventFormatter.formatItineraryEventTypeLabel = (value) => `Label:${value}`;

   try {
      const options = ScheduleItemTypes.buildScheduleItemTypeOptions([eventType], {
         typePlaceholder,
      });

      assert.equal(options.at(Position.FIRST).value, ScheduleItemTypes.SCHEDULE_ITEM_TYPE_PLACEHOLDER);
      assert.equal(options.at(Position.FIRST).label, typePlaceholder);
      assert.equal(options.at(Position.FIRST).selected, true);
      assert.deepEqual(options.at(Position.SECOND), {
         value: eventType,
         label: `Label:${eventType}`,
      });
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

      assert.equal(options.at(Position.FIRST).label, '');
      assert.equal(options.at(Position.FIRST).value, ScheduleItemTypes.SCHEDULE_ITEM_TYPE_PLACEHOLDER);
      assert.equal(
         options.some((option) => option.value === ScheduleItemKind.ATTRACTION.itemType),
         true
      );
   } finally {
      ScheduleItemEventFormatter.formatItineraryEventTypeLabel = original;
   }
});
