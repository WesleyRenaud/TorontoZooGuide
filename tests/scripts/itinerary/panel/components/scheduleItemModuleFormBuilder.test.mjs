import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemModuleFormBuilder } from '../../../../../scripts/itinerary/panel/components/scheduleItemModuleFormBuilder.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateFieldLabel_TestText_ExpectLabel', () => {
   const label = ScheduleItemModuleFormBuilder.createFieldLabel('Item type');
   assert.equal(label.className, 'schedule-item-field-label');
   assert.equal(label.textContent, 'Item type');
});

test('Test_CreateOnlyItineraryItemsCheckbox_TestLabel_ExpectUnchecked', () => {
   const { wrap, checkbox } = ScheduleItemModuleFormBuilder.createOnlyItineraryItemsCheckbox(
      'Only itinerary items'
   );

   assert.match(wrap.textContent, /Only itinerary items/);
   assert.equal(checkbox.type, 'checkbox');
   assert.equal(checkbox.checked, false);
   assert.equal(checkbox.className, 'schedule-item-only-itinerary-checkbox');
});

test('Test_CreateSelectField_TestOptions_ExpectSelect', () => {
   const { field, select } = ScheduleItemModuleFormBuilder.createSelectField({
      label: 'Type',
      options: [
         { value: 'animal', label: 'Animal', selected: true },
         { value: 'attraction', label: 'Attraction' },
      ],
      getOptionValue: (option) => option.value,
      getOptionLabel: (option) => option.label,
   });

   assert.equal(field.className, 'schedule-item-field schedule-item-type-field');
   assert.equal(select.className, 'schedule-item-select');
   assert.equal(select.children.length, 2);
   assert.equal(select.children[0].value, 'animal');
   assert.equal(select.children[0].selected, true);
   assert.equal(select.children[1].textContent, 'Attraction');
});
