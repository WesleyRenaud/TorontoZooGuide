import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ScheduleTimesCheckboxField } from '../../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxField.js';
import { GuardiansTalkOccurrenceFilter } from '../../../../../scripts/consoleOperations/guardiansTalks/controllers/guardiansTalkOccurrenceFilter.js';
import { OccurrenceFilterController } from '../../../../../scripts/consoleOperations/helpers/occurrenceFilterController.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_CreateGuardiansTalkOccurrenceFilterController_TestSelectionValues_ExpectTalkAndLocation', () => {
   const talk = 'Tiger';
   const location = 'Eurasia';
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   let captured;
   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({});
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = () => {};

   try {
      GuardiansTalkOccurrenceFilter.createGuardiansTalkOccurrenceFilterController({
         talkNameEl: { value: talk },
         locationEl: { value: location },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });
      const selection = captured.getSelectionValues();

      assert.deepEqual(selection, { talk, location });
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});


test('Test_CreateGuardiansTalkOccurrenceFilterController_TestSelectionReady_ExpectFalse', () => {
   const talk = 'Tiger';
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   let captured;
   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({});
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = () => {};

   try {
      GuardiansTalkOccurrenceFilter.createGuardiansTalkOccurrenceFilterController({
         talkNameEl: { value: talk },
         locationEl: { value: '' },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });
      const ready = captured.isSelectionReady({ talk, location: '' });

      assert.equal(ready, false);
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});


test('Test_CreateGuardiansTalkOccurrenceFilterController_TestSelectionReady_ExpectTrue', () => {
   const talk = 'Tiger';
   const location = 'Eurasia';
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   let captured;
   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({});
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = () => {};

   try {
      GuardiansTalkOccurrenceFilter.createGuardiansTalkOccurrenceFilterController({
         talkNameEl: { value: talk },
         locationEl: { value: location },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });
      const ready = captured.isSelectionReady({ talk, location });

      assert.equal(ready, true);
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});


test('Test_CreateGuardiansTalkOccurrenceFilterController_TestLoadOccurrences_ExpectClientOccurrences', async () => {
   const talk = 'Tiger';
   const location = 'Eurasia';
   const time = '11:00 AM';
   const occurrences = [{ time }];
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   const originalGet = ConsoleOperationsClient.getGuardiansTalkOccurrences;
   let captured;
   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({});
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = () => {};
   ConsoleOperationsClient.getGuardiansTalkOccurrences = async () => ({ occurrences });

   try {
      GuardiansTalkOccurrenceFilter.createGuardiansTalkOccurrenceFilterController({
         talkNameEl: { value: talk },
         locationEl: { value: location },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });
      const loaded = await captured.loadOccurrences({ talk, location });

      assert.deepEqual(loaded, occurrences);
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
      ConsoleOperationsClient.getGuardiansTalkOccurrences = originalGet;
   }
});


test('Test_CreateGuardiansTalkOccurrenceFilterController_TestLoadOccurrencesMissing_ExpectEmpty', async () => {
   const talk = 'Tiger';
   const location = 'Eurasia';
   const originalCreate = OccurrenceFilterController.createOccurrenceFilterController;
   const originalResolve = ScheduleTimesCheckboxField.resolveScheduleTimesListEl;
   const originalUpdate = ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList;
   const originalGet = ConsoleOperationsClient.getGuardiansTalkOccurrences;
   let captured;
   OccurrenceFilterController.createOccurrenceFilterController = (options) => {
      captured = options;
      return { filter: true };
   };
   ScheduleTimesCheckboxField.resolveScheduleTimesListEl = () => ({});
   ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = () => {};
   ConsoleOperationsClient.getGuardiansTalkOccurrences = async () => null;

   try {
      GuardiansTalkOccurrenceFilter.createGuardiansTalkOccurrenceFilterController({
         talkNameEl: { value: talk },
         locationEl: { value: location },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });
      const loaded = await captured.loadOccurrences({ talk, location });

      assert.deepEqual(loaded, []);
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
      ConsoleOperationsClient.getGuardiansTalkOccurrences = originalGet;
   }
});


test('Test_CreateGuardiansTalkOccurrenceFilterController_TestPopulateTimes_ExpectUpdate', () => {
   const talk = 'Tiger';
   const location = 'Eurasia';
   const time = '11:00 AM';
   const times = [time];
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
      GuardiansTalkOccurrenceFilter.createGuardiansTalkOccurrenceFilterController({
         talkNameEl: { value: talk },
         locationEl: { value: location },
         dateEl: { value: '2026-06-15' },
         timesEl: {},
      });
      captured.populateTimes(times);

      assert.equal(updates.length, 1);
      assert.deepEqual(updates.at(Position.FIRST)[Position.SECOND].times, times);
      assert.equal(updates.at(Position.FIRST)[Position.SECOND].hasSelectedEntity, true);
      assert.equal(updates.at(Position.FIRST)[Position.SECOND].hasDate, true);
   } finally {
      OccurrenceFilterController.createOccurrenceFilterController = originalCreate;
      ScheduleTimesCheckboxField.resolveScheduleTimesListEl = originalResolve;
      ScheduleTimesCheckboxField.updateScheduleTimesCheckboxList = originalUpdate;
   }
});
