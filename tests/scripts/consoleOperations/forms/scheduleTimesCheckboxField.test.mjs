import assert from 'node:assert/strict';
import test from 'node:test';

import { Strings } from '../../../../scripts/strings.js';
import { ScheduleTimesCheckboxField } from '../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';

function _getCheckboxEls(listEl) {
   return [
      ...listEl?.children ?? [],
   ].flatMap((optionEl) =>
      (optionEl.children ?? []).filter((child) => child.type === 'checkbox')
   );
}

installDomTestHooks();

test('Test_CreateScheduleTimesCheckboxField_TestIdle_ExpectPlaceholder', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testEncounterTimesIdle',
   });
   const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');
   const placeholderEl = listEl.querySelector('.console-operations-schedule-times-placeholder');

   assert.equal(listEl.hidden, false);
   assert.equal(
      placeholderEl?.textContent,
      Strings.placeholders.selectWildEncounterFirst
   );
});

test('Test_PopulateScheduleTimesCheckboxList_TestTimes_ExpectUnchecked', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testEncounterTimes',
   });
   const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, [ '2:00 PM', '3:30 PM' ]);

   const checkboxes = _getCheckboxEls(listEl);

   assert.equal(listEl.hidden, false);
   assert.equal(checkboxes.length, 2);
   assert.equal(checkboxes[0].value, '2:00 PM');
   assert.equal(checkboxes[1].value, '3:30 PM');
   assert.equal(checkboxes[0].checked, false);
});

test('Test_PopulateScheduleTimesCheckboxList_TestSingleTime_ExpectAutoSelect', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testEncounterTimesSingle',
   });
   const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, [ '2:00 PM' ], {
      autoSelectSingleTime: true,
   });

   assert.equal(_getCheckboxEls(listEl).length, 0);
   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-single')?.textContent,
      '2:00 PM'
   );
   assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(listEl), [ '2:00 PM' ]);
});

test('Test_UpdateScheduleTimesCheckboxList_TestSingleOccurrence_ExpectAutoSelect', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testEncounterTimesSingleUpdate',
   });
   const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
      times: [ '3:30 PM' ],
      hasSelectedEntity: true,
      hasDate: true,
      autoSelectSingleTime: true,
   });

   assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(listEl), [ '3:30 PM' ]);
});

test('Test_PopulateScheduleTimesCheckboxList_TestEmpty_ExpectNoTimesMessage', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testEncounterTimesEmpty',
   });
   const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, []);

   const placeholderEl = listEl.querySelector('.console-operations-schedule-times-placeholder');

   assert.equal(listEl.hidden, false);
   assert.equal(
      placeholderEl?.textContent,
      Strings.help.noScheduledEncounterTimes
   );
});

test('Test_ResetScheduleTimesCheckboxList_TestReset_ExpectIdlePlaceholder', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testEncounterTimesReset',
   });
   const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, [ '2:00 PM' ]);
   ScheduleTimesCheckboxField.resetScheduleTimesCheckboxList(listEl);

   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
      Strings.placeholders.selectWildEncounterFirst
   );
});

test('Test_UpdateScheduleTimesCheckboxList_TestEncounterNoDate_ExpectSelectDate', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testEncounterTimesSelectDate',
   });
   const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
      times: [],
      hasSelectedEntity: true,
      hasDate: false,
   });

   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
      Strings.placeholders.selectDateFirst
   );
});

test('Test_GetSelectedScheduleTimes_TestChecked_ExpectValues', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testEncounterTimesSelected',
   });
   const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, [ '2:00 PM', '3:30 PM' ]);

   const checkboxes = _getCheckboxEls(listEl);
   checkboxes[0].checked = true;

   assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(listEl), [ '2:00 PM' ]);
});

test('Test_ResolveScheduleTimesListEl_TestIdNestedAndFallback_ExpectResolved', () => {
   const listEl = document.createElement('div');
   listEl.className = ScheduleTimesCheckboxField.SCHEDULE_TIMES_LIST_CLASS;
   listEl.id = 'resolvedScheduleTimesList';

   const fallback = document.createElement('div');
   fallback.id = 'endWildEncounterScheduleTimes';
   fallback.className = ScheduleTimesCheckboxField.SCHEDULE_TIMES_LIST_CLASS;

   const originalGetById = document.getElementById;
   document.getElementById = (id) => {
      if (id === listEl.id) {
         return listEl;
      }
      if (id === fallback.id) {
         return fallback;
      }
      return originalGetById.call(document, id);
   };

   try {
      assert.equal(ScheduleTimesCheckboxField.resolveScheduleTimesListEl(listEl), listEl);

      const wrapper = document.createElement('div');
      wrapper.id = 'resolvedScheduleTimesList';
      assert.equal(ScheduleTimesCheckboxField.resolveScheduleTimesListEl(wrapper), listEl);

      const nestedHost = document.createElement('div');
      nestedHost.appendChild(listEl);
      assert.equal(ScheduleTimesCheckboxField.resolveScheduleTimesListEl(nestedHost), listEl);

      assert.equal(
         ScheduleTimesCheckboxField.resolveScheduleTimesListEl(document.createElement('div')),
         fallback
      );
   } finally {
      document.getElementById = originalGetById;
   }
});

test('Test_ScheduleTimesCheckboxField_TestMissingListEl_ExpectNoOps', () => {
   const originalGet = document.getElementById;
   document.getElementById = () => null;

   try {
      assert.doesNotThrow(() => {
         ScheduleTimesCheckboxField.setScheduleTimesCheckboxListMessage(null, 'msg');
         ScheduleTimesCheckboxField.resetScheduleTimesCheckboxList(null);
         ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(null, [ '1:00 PM' ]);
         ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(null, {
            times: [ '1:00 PM' ],
            hasSelectedEntity: true,
            hasDate: true,
         });
         ScheduleTimesCheckboxField.clearScheduleTimesCheckboxList(null);
      });
      assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(null), []);
   } finally {
      document.getElementById = originalGet;
   }
});

test('Test_UpdateScheduleTimesCheckboxList_TestEncounterWithDateNoTimes_ExpectNoTimesMessage', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId: 'testEncounterTimesNoTimesWithDate',
   });
   const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
      times: [],
      hasSelectedEntity: true,
      hasDate: true,
   });

   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
      Strings.help.noScheduledEncounterTimes
   );

   ScheduleTimesCheckboxField.clearScheduleTimesCheckboxList(listEl);
   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
      Strings.placeholders.selectWildEncounterFirst
   );

   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
      times: [],
      hasSelectedEntity: false,
   });
   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
      Strings.placeholders.selectWildEncounterFirst
   );
});
