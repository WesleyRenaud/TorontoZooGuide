import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleTimesCheckboxField } from '../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

function _getCheckboxEls(listEl) {
   return [
      ...listEl?.children ?? [],
   ].flatMap((optionEl) =>
      (optionEl.children ?? []).filter((child) => child.type === 'checkbox')
   );
}

function _createListEl(inputId) {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Encounter times',
      inputId,
   });
   return fieldEl.querySelector('.console-operations-schedule-times-list');
}

installDomTestHooks();


test('Test_CreateScheduleTimesCheckboxField_TestIdle_ExpectPlaceholder', () => {
   const listEl = _createListEl('testEncounterTimesIdle');

   const placeholderEl = listEl.querySelector('.console-operations-schedule-times-placeholder');

   assert.equal(listEl.hidden, false);
   assert.equal(placeholderEl?.textContent, Strings.placeholders.selectWildEncounterFirst);
});


test('Test_PopulateScheduleTimesCheckboxList_TestTimes_ExpectUnchecked', () => {
   const afternoon = '2:00 PM';
   const later = '3:30 PM';
   const times = [afternoon, later];
   const listEl = _createListEl('testEncounterTimes');

   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, times);

   const checkboxes = _getCheckboxEls(listEl);
   assert.equal(listEl.hidden, false);
   assert.equal(checkboxes.length, times.length);
   assert.equal(checkboxes[Position.FIRST].value, afternoon);
   assert.equal(checkboxes[Position.SECOND].value, later);
   assert.equal(checkboxes[Position.FIRST].checked, false);
});


test('Test_PopulateScheduleTimesCheckboxList_TestSingleTime_ExpectAutoSelect', () => {
   const afternoon = '2:00 PM';
   const times = [afternoon];
   const listEl = _createListEl('testEncounterTimesSingle');

   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, times, {
      autoSelectSingleTime: true,
   });

   const selected = ScheduleTimesCheckboxField.getSelectedScheduleTimes(listEl);
   assert.equal(_getCheckboxEls(listEl).length, 0);
   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-single')?.textContent,
      afternoon
   );
   assert.deepEqual(selected, times);
});


test('Test_UpdateScheduleTimesCheckboxList_TestSingleOccurrence_ExpectAutoSelect', () => {
   const later = '3:30 PM';
   const times = [later];
   const listEl = _createListEl('testEncounterTimesSingleUpdate');

   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
      times,
      hasSelectedEntity: true,
      hasDate: true,
      autoSelectSingleTime: true,
   });

   const selected = ScheduleTimesCheckboxField.getSelectedScheduleTimes(listEl);
   assert.deepEqual(selected, times);
});


test('Test_PopulateScheduleTimesCheckboxList_TestEmpty_ExpectNoTimesMessage', () => {
   const listEl = _createListEl('testEncounterTimesEmpty');

   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, []);

   const placeholderEl = listEl.querySelector('.console-operations-schedule-times-placeholder');
   assert.equal(listEl.hidden, false);
   assert.equal(placeholderEl?.textContent, Strings.help.noScheduledEncounterTimes);
});


test('Test_ResetScheduleTimesCheckboxList_TestReset_ExpectIdlePlaceholder', () => {
   const listEl = _createListEl('testEncounterTimesReset');
   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, ['2:00 PM']);

   ScheduleTimesCheckboxField.resetScheduleTimesCheckboxList(listEl);

   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
      Strings.placeholders.selectWildEncounterFirst
   );
});


test('Test_UpdateScheduleTimesCheckboxList_TestEncounterNoDate_ExpectSelectDate', () => {
   const listEl = _createListEl('testEncounterTimesSelectDate');

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
   const afternoon = '2:00 PM';
   const later = '3:30 PM';
   const listEl = _createListEl('testEncounterTimesSelected');
   ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(listEl, [afternoon, later]);

   _getCheckboxEls(listEl)[Position.FIRST].checked = true;
   const selected = ScheduleTimesCheckboxField.getSelectedScheduleTimes(listEl);

   assert.deepEqual(selected, [afternoon]);
});


test('Test_ResolveScheduleTimesListEl_TestSameElement_ExpectSameReference', () => {
   const listEl = document.createElement('div');
   listEl.className = ScheduleTimesCheckboxField.SCHEDULE_TIMES_LIST_CLASS;
   listEl.id = 'resolvedScheduleTimesList';
   const originalGetById = document.getElementById;
   document.getElementById = (id) => (
      id === listEl.id ? listEl : originalGetById.call(document, id)
   );

   try {
      const resolved = ScheduleTimesCheckboxField.resolveScheduleTimesListEl(listEl);

      assert.equal(resolved, listEl);
   } finally {
      document.getElementById = originalGetById;
   }
});


test('Test_ResolveScheduleTimesListEl_TestWrapperId_ExpectListById', () => {
   const listEl = document.createElement('div');
   listEl.className = ScheduleTimesCheckboxField.SCHEDULE_TIMES_LIST_CLASS;
   listEl.id = 'resolvedScheduleTimesList';
   const wrapper = document.createElement('div');
   wrapper.id = listEl.id;
   const originalGetById = document.getElementById;
   document.getElementById = (id) => (
      id === listEl.id ? listEl : originalGetById.call(document, id)
   );

   try {
      const resolved = ScheduleTimesCheckboxField.resolveScheduleTimesListEl(wrapper);

      assert.equal(resolved, listEl);
   } finally {
      document.getElementById = originalGetById;
   }
});


test('Test_ResolveScheduleTimesListEl_TestNestedHost_ExpectNestedList', () => {
   const listEl = document.createElement('div');
   listEl.className = ScheduleTimesCheckboxField.SCHEDULE_TIMES_LIST_CLASS;
   const nestedHost = document.createElement('div');
   nestedHost.appendChild(listEl);

   const resolved = ScheduleTimesCheckboxField.resolveScheduleTimesListEl(nestedHost);

   assert.equal(resolved, listEl);
});


test('Test_ResolveScheduleTimesListEl_TestMissingHost_ExpectFallback', () => {
   const fallback = document.createElement('div');
   fallback.id = 'endWildEncounterScheduleTimes';
   fallback.className = ScheduleTimesCheckboxField.SCHEDULE_TIMES_LIST_CLASS;
   const originalGetById = document.getElementById;
   document.getElementById = (id) => (
      id === fallback.id ? fallback : originalGetById.call(document, id)
   );

   try {
      const resolved = ScheduleTimesCheckboxField.resolveScheduleTimesListEl(
         document.createElement('div')
      );

      assert.equal(resolved, fallback);
   } finally {
      document.getElementById = originalGetById;
   }
});


test('Test_ScheduleTimesCheckboxField_TestMissingListEl_ExpectNoOps', () => {
   const originalGet = document.getElementById;
   document.getElementById = () => null;
   const message = 'msg';
   const time = '1:00 PM';

   try {
      assert.doesNotThrow(() => {
         ScheduleTimesCheckboxField.setScheduleTimesCheckboxListMessage(null, message);
         ScheduleTimesCheckboxField.resetScheduleTimesCheckboxList(null);
         ScheduleTimesCheckboxField.populateScheduleTimesCheckboxList(null, [time]);
         ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(null, {
            times: [time],
            hasSelectedEntity: true,
            hasDate: true,
         });
         ScheduleTimesCheckboxField.clearScheduleTimesCheckboxList(null);
      });

      const selected = ScheduleTimesCheckboxField.getSelectedScheduleTimes(null);
      assert.deepEqual(selected, []);
   } finally {
      document.getElementById = originalGet;
   }
});


test('Test_UpdateScheduleTimesCheckboxList_TestEncounterWithDateNoTimes_ExpectNoTimesMessage', () => {
   const listEl = _createListEl('testEncounterTimesNoTimesWithDate');

   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
      times: [],
      hasSelectedEntity: true,
      hasDate: true,
   });

   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
      Strings.help.noScheduledEncounterTimes
   );
});


test('Test_ClearScheduleTimesCheckboxList_TestAfterUpdate_ExpectIdlePlaceholder', () => {
   const listEl = _createListEl('testEncounterTimesClear');
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
      times: [],
      hasSelectedEntity: true,
      hasDate: true,
   });

   ScheduleTimesCheckboxField.clearScheduleTimesCheckboxList(listEl);

   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
      Strings.placeholders.selectWildEncounterFirst
   );
});


test('Test_UpdateScheduleTimesCheckboxList_TestNoSelectedEntity_ExpectIdlePlaceholder', () => {
   const listEl = _createListEl('testEncounterTimesNoEntity');

   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList(listEl, {
      times: [],
      hasSelectedEntity: false,
   });

   assert.equal(
      listEl.querySelector('.console-operations-schedule-times-placeholder')?.textContent,
      Strings.placeholders.selectWildEncounterFirst
   );
});
