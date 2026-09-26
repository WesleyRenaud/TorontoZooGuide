import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { OccurrenceFilterController } from '../../../../../scripts/consoleOperations/helpers/occurrenceFilterController.js';
import { WildEncounterOccurrenceFilter } from '../../../../../scripts/consoleOperations/wildEncounters/controllers/wildEncounterOccurrenceFilter.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_CreateWildEncounterOccurrenceFilterController_TestCreate_ExpectFilter', () => {
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   OccurrenceFilterController.createOccurrenceFilterController = () => ({ filter: true });
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({ id: 'list' });
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = () => {};

   try {
      const created = WildEncounterOccurrenceFilter.createWildEncounterOccurrenceFilterController({
         wildEncounterEl: { value: 'Giraffe' },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });

      assert.deepEqual(created, { filter: true });
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});


test('Test_CreateWildEncounterOccurrenceFilterController_TestSelectionValues_ExpectEncounter', () => {
   const wildEncounter = 'Giraffe';
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   let captured;
   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({ id: 'list' });
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = () => {};

   try {
      WildEncounterOccurrenceFilter.createWildEncounterOccurrenceFilterController({
         wildEncounterEl: { value: wildEncounter },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });
      const selection = captured.getSelectionValues();

      assert.deepEqual(selection, { wildEncounter });
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});


test('Test_CreateWildEncounterOccurrenceFilterController_TestLoadOccurrences_ExpectClientOccurrences', async () => {
   const wildEncounter = 'Giraffe';
   const time = '1:00 PM';
   const occurrences = [{ time }];
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   const originalGet = ConsoleOperationsClient.getWildEncounterOccurrences;
   let captured;
   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({ id: 'list' });
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = () => {};
   ConsoleOperationsClient.getWildEncounterOccurrences = async () => ({ occurrences });

   try {
      WildEncounterOccurrenceFilter.createWildEncounterOccurrenceFilterController({
         wildEncounterEl: { value: wildEncounter },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });
      const loaded = await captured.loadOccurrences({ wildEncounter });

      assert.deepEqual(loaded, occurrences);
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
      ConsoleOperationsClient.getWildEncounterOccurrences = originalGet;
   }
});


test('Test_CreateWildEncounterOccurrenceFilterController_TestPopulateTimes_ExpectUpdate', () => {
   const times = ['11:00 AM'];
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   let captured;
   const updates = [];
   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({ id: 'list' });
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = (...args) => {
      updates.push(args);
   };

   try {
      WildEncounterOccurrenceFilter.createWildEncounterOccurrenceFilterController({
         wildEncounterEl: { value: 'Giraffe' },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });
      captured.populateTimes(times);

      assert.equal(updates.length, 1);
      assert.deepEqual(updates.at(Position.FIRST)[Position.SECOND].times, times);
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});
