import assert from 'node:assert/strict';
import test from 'node:test';

import { APP_STRINGS } from '../../scripts/strings.js';
import {
   createScheduleTimesCheckboxField,
} from '../../scripts/consoleOperations/templates/fragments.js';
import {
   getSelectedScheduleTimes,
   populateScheduleTimesCheckboxList,
   resetScheduleTimesCheckboxList,
   updateScheduleTimesCheckboxList,
} from '../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

function getCheckboxEls(listEl) {
   return [
      ...listEl?.children ?? [],
   ].flatMap((optionEl) =>
      (optionEl.children ?? []).filter((child) => child.type === 'checkbox')
   );
}

test.describe('schedule times checkbox field', () => {
   installDomTestHooks();

   test('createScheduleTimesCheckboxField starts with the idle placeholder in a full-height list', () => {
      const fieldEl = createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimesIdle',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');
      const placeholderEl = listEl.querySelector('.console-operations-schedule-times-placeholder');

      assert.equal(listEl.hidden, false);
      assert.equal(
         placeholderEl?.textContent,
         APP_STRINGS.placeholders.selectWildEncounterFirst
      );
   });

   test('populateScheduleTimesCheckboxList renders unchecked time options', () => {
      const fieldEl = createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimes',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      populateScheduleTimesCheckboxList(listEl, [ '2:00 PM', '3:30 PM' ]);

      const checkboxes = getCheckboxEls(listEl);

      assert.equal(listEl.hidden, false);
      assert.equal(checkboxes.length, 2);
      assert.equal(checkboxes[0].value, '2:00 PM');
      assert.equal(checkboxes[1].value, '3:30 PM');
      assert.equal(checkboxes[0].checked, false);
   });

   test('populateScheduleTimesCheckboxList shows the no-times message inside the list box', () => {
      const fieldEl = createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimesEmpty',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      populateScheduleTimesCheckboxList(listEl, []);

      const placeholderEl = listEl.querySelector('.console-operations-schedule-times-placeholder');

      assert.equal(listEl.hidden, false);
      assert.equal(
         placeholderEl?.textContent,
         APP_STRINGS.help.noScheduledEncounterTimes
      );
   });

   test('resetScheduleTimesCheckboxList restores the idle placeholder', () => {
      const fieldEl = createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimesReset',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      populateScheduleTimesCheckboxList(listEl, [ '2:00 PM' ]);
      resetScheduleTimesCheckboxList(listEl);

      assert.equal(
         listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
         APP_STRINGS.placeholders.selectWildEncounterFirst
      );
   });

   test('updateScheduleTimesCheckboxList shows the select-date placeholder when an encounter is selected', () => {
      const fieldEl = createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimesSelectDate',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      updateScheduleTimesCheckboxList(listEl, {
         times: [],
         hasWildEncounter: true,
         hasDate: false,
      });

      assert.equal(
         listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
         APP_STRINGS.placeholders.selectDateFirst
      );
   });

   test('getSelectedScheduleTimes returns checked values', () => {
      const fieldEl = createScheduleTimesCheckboxField({
         label: 'Encounter times',
         inputId: 'testEncounterTimesSelected',
      });
      const listEl = fieldEl.querySelector('.console-operations-schedule-times-list');

      populateScheduleTimesCheckboxList(listEl, [ '2:00 PM', '3:30 PM' ]);

      const checkboxes = getCheckboxEls(listEl);
      checkboxes[0].checked = true;

      assert.deepEqual(getSelectedScheduleTimes(listEl), [ '2:00 PM' ]);
   });
});
