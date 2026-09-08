import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationRefsCollector } from '../../../../scripts/consoleOperations/bootstrap/consoleOperationRefsCollector.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _fakeDoc(ids = {}) {
   return {
      getElementById: (id) => ids[id] ?? null,
   };
}

test('Test_CapitalizeFirstLetter_TestValues_ExpectCapitalized', () => {
   assert.equal(ConsoleOperationRefsCollector.capitalizeFirstLetter('offDisplay'), 'OffDisplay');
   assert.equal(ConsoleOperationRefsCollector.capitalizeFirstLetter(''), '');
   assert.equal(ConsoleOperationRefsCollector.capitalizeFirstLetter(), '');
});

test('Test_GetById_TestDocument_ExpectElement', () => {
   const el = { id: 'panel' };
   assert.equal(ConsoleOperationRefsCollector.getById(_fakeDoc({ panel: el }), 'panel'), el);
   assert.equal(ConsoleOperationRefsCollector.getById(_fakeDoc(), 'missing'), null);
});

test('Test_CreateElementRefs_TestIds_ExpectMapped', () => {
   const show = { id: 'show' };
   const panel = { id: 'panel' };
   const refs = ConsoleOperationRefsCollector.createElementRefs(
      _fakeDoc({ show, panel }),
      { showButtonEl: 'show', panelEl: 'panel' }
   );

   assert.deepEqual(refs, { showButtonEl: show, panelEl: panel });
});

test('Test_CreatePrefixedRefs_TestSuffixes_ExpectPrefixedIds', () => {
   const start = { id: 'opStartDate' };
   const end = { id: 'opEndDate' };
   const refs = ConsoleOperationRefsCollector.createPrefixedRefs(
      _fakeDoc({ opStartDate: start, opEndDate: end }),
      'op',
      { startDateEl: 'StartDate', endDateEl: 'EndDate' }
   );

   assert.deepEqual(refs, { startDateEl: start, endDateEl: end });
});

test('Test_CreateFormRefs_TestOperationName_ExpectFormControls', () => {
   const ids = {
      showOffDisplayForm: { id: 'show' },
      offDisplayPanel: { id: 'panel' },
      submitOffDisplay: { id: 'submit' },
      offDisplayStatus: { id: 'status' },
   };
   const refs = ConsoleOperationRefsCollector.createFormRefs(_fakeDoc(ids), 'offDisplay');

   assert.deepEqual(refs, {
      showButtonEl: ids.showOffDisplayForm,
      panelEl: ids.offDisplayPanel,
      submitButtonEl: ids.submitOffDisplay,
      statusEl: ids.offDisplayStatus,
   });
});

test('Test_CreateAnimalSpeciesAndDateRangeRefs_TestOperation_ExpectFields', () => {
   const species = { id: 'species' };
   const results = { id: 'results' };
   const exhibit = { id: 'exhibit' };
   const start = { id: 'start' };
   const end = { id: 'end' };
   const doc = _fakeDoc({
      opSpecies: species,
      opSpeciesResults: results,
      opExhibit: exhibit,
      opStartDate: start,
      opEndDate: end,
   });

   assert.deepEqual(ConsoleOperationRefsCollector.createAnimalSpeciesRefs(doc, 'op'), {
      speciesEl: species,
      speciesResultsEl: results,
      exhibitEl: exhibit,
   });
   assert.deepEqual(ConsoleOperationRefsCollector.createDateRangeRefs(doc, 'op'), {
      startDateEl: start,
      endDateEl: end,
   });
});

test('Test_CreateWeekdayAndWeeklyAvailabilityRefs_TestOperation_ExpectDays', () => {
   const monday = { id: 'monday' };
   const holidays = { id: 'holidays' };
   const preset = { id: 'preset' };
   const start = { id: 'start' };
   const end = { id: 'end' };
   const doc = _fakeDoc({
      opMonday: monday,
      opTuesday: { id: 'tue' },
      opWednesday: { id: 'wed' },
      opThursday: { id: 'thu' },
      opFriday: { id: 'fri' },
      opSaturday: { id: 'sat' },
      opSunday: { id: 'sun' },
      opHolidaysOnly: holidays,
      opPreset: preset,
      opStartDate: start,
      opEndDate: end,
   });

   const weekdayRefs = ConsoleOperationRefsCollector.createWeekdayScheduleRefs(doc, 'op');
   assert.equal(weekdayRefs.mondayEl, monday);
   assert.equal(Object.keys(weekdayRefs).length, 7);

   const weeklyRefs = ConsoleOperationRefsCollector.createWeeklyAvailabilityRefs(doc, 'op');
   assert.equal(weeklyRefs.presetEl, preset);
   assert.equal(weeklyRefs.holidaysOnlyEl, holidays);
   assert.equal(weeklyRefs.startDateEl, start);
   assert.equal(weeklyRefs.endDateEl, end);
   assert.equal(weeklyRefs.mondayEl, monday);
});

test('Test_CreateOperationRefs_TestFlagsAndOverrides_ExpectCombined', () => {
   const doc = _fakeDoc({
      showOpForm: { id: 'show' },
      opPanel: { id: 'panel' },
      submitOp: { id: 'submit' },
      opStatus: { id: 'status' },
      opSpecies: { id: 'species' },
      opSpeciesResults: { id: 'results' },
      opExhibit: { id: 'exhibit' },
      opStartDate: { id: 'start' },
      opEndDate: { id: 'end' },
      opMessage: { id: 'message' },
      customName: { id: 'custom' },
   });

   const refs = ConsoleOperationRefsCollector.createOperationRefs(doc, {
      operationName: 'op',
      includeAnimalSpecies: true,
      includeDateRange: true,
      fieldSuffixes: { messageEl: 'Message' },
      fieldIds: { wildEncounterEl: 'customName' },
   });

   assert.equal(refs.showButtonEl.id, 'show');
   assert.equal(refs.speciesEl.id, 'species');
   assert.equal(refs.startDateEl.id, 'start');
   assert.equal(refs.messageEl.id, 'message');
   assert.equal(refs.wildEncounterEl.id, 'custom');
});

test('Test_CreateGroupRefs_TestConfig_ExpectKeyedOperations', () => {
   const doc = _fakeDoc({
      showClosedForm: { id: 'show' },
      closedPanel: { id: 'panel' },
      submitClosed: { id: 'submit' },
      closedStatus: { id: 'status' },
   });

   const group = ConsoleOperationRefsCollector.createGroupRefs(doc, {
      closed: { operationName: 'closed' },
   });

   assert.equal(group.closed.panelEl.id, 'panel');
   assert.equal(group.closed.showButtonEl.id, 'show');
});

test('Test_CollectConsoleOperationRefs_TestConfig_ExpectAllGroups', () => {
   const originalGet = ConsoleOperationRefsCollector.getById;
   ConsoleOperationRefsCollector.getById = (_doc, id) => ({ id });

   try {
      const refs = ConsoleOperationRefsCollector.collectConsoleOperationRefs({});
      const expectedGroups = Object.keys(ConsoleOperationRefsCollector.CONSOLE_OPERATION_REF_CONFIG);

      assert.deepEqual(Object.keys(refs).sort(), expectedGroups.slice().sort());
      assert.ok(refs.animals.offDisplay.showButtonEl);
      assert.ok(refs.wildEncounters.cancelOccurrence.wildEncounterEl);
      assert.equal(refs.wildEncounters.cancelOccurrence.wildEncounterEl.id, 'cancelWildEncounterOccurrenceName');
      assert.ok(refs.restaurants.openingSchedule.presetEl);
      assert.ok(refs.updates.edit.updateEl);
   } finally {
      ConsoleOperationRefsCollector.getById = originalGet;
   }
});
