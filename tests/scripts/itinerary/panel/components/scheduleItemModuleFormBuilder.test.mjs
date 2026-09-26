import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemModuleFormBuilder } from '../../../../../scripts/itinerary/panel/components/scheduleItemModuleFormBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateFieldLabel_TestText_ExpectLabel', () => {
   const text = 'Item type';

   const label = ScheduleItemModuleFormBuilder.createFieldLabel(text);

   assert.equal(label.className, 'schedule-item-field-label');
   assert.equal(label.textContent, text);
});


test('Test_CreateOnlyItineraryItemsCheckbox_TestLabel_ExpectUnchecked', () => {
   const checkboxLabel = 'Only itinerary items';

   const { wrap, checkbox } = ScheduleItemModuleFormBuilder.createOnlyItineraryItemsCheckbox(
      checkboxLabel
   );

   assert.match(wrap.textContent, new RegExp(checkboxLabel));
   assert.equal(checkbox.type, 'checkbox');
   assert.equal(checkbox.checked, false);
   assert.equal(checkbox.className, 'schedule-item-only-itinerary-checkbox');
});


test('Test_CreateSelectField_TestOptions_ExpectSelect', () => {
   const animalValue = 'animal';
   const attractionLabel = 'Attraction';
   const options = [
      { value: animalValue, label: 'Animal', selected: true },
      { value: 'attraction', label: attractionLabel },
   ];

   const { field, select } = ScheduleItemModuleFormBuilder.createSelectField({
      label: 'Type',
      options,
      getOptionValue: (option) => option.value,
      getOptionLabel: (option) => option.label,
   });

   assert.equal(field.className, 'schedule-item-field schedule-item-type-field');
   assert.equal(select.className, 'schedule-item-select');
   assert.equal(select.children.length, options.length);
   assert.equal(select.children.at(Position.FIRST).value, animalValue);
   assert.equal(select.children.at(Position.FIRST).selected, true);
   assert.equal(select.children.at(Position.SECOND).textContent, attractionLabel);
});
