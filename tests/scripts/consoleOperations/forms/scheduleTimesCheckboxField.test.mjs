import assert from 'node:assert/strict';
import test from 'node:test';

import { Strings } from '../../../../scripts/strings.js';
import { Fragments } from '../../../../scripts/consoleOperations/templates/fragments.js';
import { ScheduleTimesCheckboxField } from '../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

function getCheckboxEls(listEl) {
   return [
      ...listEl?.children ?? [],
   ].flatMap((optionEl) =>
      (optionEl.children ?? []).filter((child) => child.type === 'checkbox')
   );
}

test.describe('Test_ScheduleTimesCheckboxField', () => {
   installDomTestHooks();

   test('Test_CreateScheduleTimesCheckboxField_TestIdle_ExpectPlaceholder', () => {
      const fieldEl = Fragments.createScheduleTimesCheckboxField({
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
      const fieldEl = Fragments.createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimes',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, [ '2:00 PM', '3:30 PM' ]);

      const checkboxes = getCheckboxEls(listEl);

      assert.equal(listEl.hidden, false);
      assert.equal(checkboxes.length, 2);
      assert.equal(checkboxes[0].value, '2:00 PM');
      assert.equal(checkboxes[1].value, '3:30 PM');
      assert.equal(checkboxes[0].checked, false);
   });

   test('Test_PopulateScheduleTimesCheckboxList_TestSingleTime_ExpectAutoSelect', () => {
      const fieldEl = Fragments.createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimesSingle',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, [ '2:00 PM' ], {
         autoSelectSingleTime: true,
      });

      assert.equal(getCheckboxEls(listEl).length, 0);
      assert.equal(
         listEl.querySelector('.console-operations-schedule-times-single')?.textContent,
         '2:00 PM'
      );
      assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(listEl), [ '2:00 PM' ]);
   });

   test('Test_UpdateScheduleTimesCheckboxList_TestSingleOccurrence_ExpectAutoSelect', () => {
      const fieldEl = Fragments.createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimesSingleUpdate',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
         times: [ '3:30 PM' ],
         hasWildEncounter: true,
         hasDate: true,
         autoSelectSingleTime: true,
      });

      assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(listEl), [ '3:30 PM' ]);
   });

   test('Test_PopulateScheduleTimesCheckboxList_TestEmpty_ExpectNoTimesMessage', () => {
      const fieldEl = Fragments.createScheduleTimesCheckboxField({
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
      const fieldEl = Fragments.createScheduleTimesCheckboxField({
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
      const fieldEl = Fragments.createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimesSelectDate',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
         times: [],
         hasWildEncounter: true,
         hasDate: false,
      });

      assert.equal(
         listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
         Strings.placeholders.selectDateFirst
      );
   });

   test('Test_GetSelectedScheduleTimes_TestChecked_ExpectValues', () => {
      const fieldEl = Fragments.createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimesSelected',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, [ '2:00 PM', '3:30 PM' ]);

      const checkboxes = getCheckboxEls(listEl);
      checkboxes[0].checked = true;

      assert.deepEqual(ScheduleTimesCheckboxField.getSelectedScheduleTimes(listEl), [ '2:00 PM' ]);
   });
});
