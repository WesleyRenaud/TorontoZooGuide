import assert from 'node:assert/strict';
import test from 'node:test';

import { EndRecurringSchedulePanelBuilder } from '../../../../scripts/consoleOperations/forms/endRecurringSchedulePanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';

function _installBuilderMocks() {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createScheduleTimesCheckboxField: ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField,
      createDateField: ConsoleDateFieldBuilder.createDateField,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };
   const panel = { panel: true };
   let captured;

   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return panel;
   };
   ConsoleSelectFieldBuilder.createSelectField = (options) => ({ kind: 'createSelectField', ...options });
   ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = (options) => ({
      kind: 'createScheduleTimesCheckboxField',
      ...options,
   });
   ConsoleDateFieldBuilder.createDateField = (options) => ({ kind: 'createDateField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   return {
      panel,
      getCaptured: () => captured,
      restore() {
         ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
         ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
         ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = originals.createScheduleTimesCheckboxField;
         ConsoleDateFieldBuilder.createDateField = originals.createDateField;
         ConsoleActionsBuilder.createActions = originals.createActions;
         ConsoleStatusBuilder.createStatus = originals.createStatus;
      },
   };
}


test('Test_CreatePanel_TestGuardiansTalkConfig_ExpectLocationTalkFields', () => {
   const mocks = _installBuilderMocks();
   const panelId = 'endGuardiansTalkSchedulePanel';
   const locationInputId = 'endGuardiansTalkScheduleLocation';
   const talkInputId = 'endGuardiansTalkScheduleTalkName';
   const timesInputId = 'endGuardiansTalkScheduleTimes';
   const endDateInputId = 'endGuardiansTalkScheduleEndDate';
   const submitId = 'submitEndGuardiansTalkSchedule';
   const statusId = 'endGuardiansTalkScheduleStatus';

   try {
      const result = EndRecurringSchedulePanelBuilder.createPanel({
         panelId,
         title: Strings.panelTitles.endGuardiansTalkSchedule,
         locationLabel: Strings.labels.location,
         locationInputId,
         locationEmptyOptionLabel: Strings.placeholders.location,
         talkLabel: Strings.labels.talkName,
         talkInputId,
         talkEmptyOptionLabel: Strings.placeholders.talk,
         timesLabel: Strings.labels.talkTimes,
         timesInputId,
         timesHelpText: Strings.help.endScheduleTimes,
         endDateLabel: Strings.labels.stopsBeingOfferedOn,
         endDateInputId,
         endDatePlaceholder: Strings.placeholders.stopsBeingOfferedOn,
         endDateHelpText: Strings.help.endScheduleToday,
         submitId,
         statusId,
      });

      const captured = mocks.getCaptured();
      const [
         locationField,
         talkField,
         timesField,
         endDateField,
         actions,
         status,
      ] = captured.bodyChildren;
      assert.equal(result, mocks.panel);
      assert.equal(captured.panelId, panelId);
      assert.equal(locationField.inputId, locationInputId);
      assert.equal(talkField.inputId, talkInputId);
      assert.equal(timesField.inputId, timesInputId);
      assert.equal(endDateField.inputId, endDateInputId);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      mocks.restore();
   }
});


test('Test_CreatePanel_TestWildEncounterConfig_ExpectEntityField', () => {
   const mocks = _installBuilderMocks();
   const entityInputId = 'endWildEncounterScheduleName';
   const timesInputId = 'endWildEncounterScheduleTimes';
   const endDateInputId = 'endWildEncounterScheduleDate';
   const submitId = 'submitEndWildEncounterSchedule';
   const statusId = 'endWildEncounterScheduleStatus';

   try {
      EndRecurringSchedulePanelBuilder.createPanel({
         panelId: 'endWildEncounterSchedulePanel',
         title: Strings.panelTitles.endWildEncounterSchedule,
         entityLabel: Strings.entityLabels.wildEncounter,
         entityInputId,
         entityEmptyOptionLabel: Strings.placeholders.wildEncounter,
         timesLabel: Strings.labels.encounterTimes,
         timesInputId,
         timesHelpText: Strings.help.endScheduleTimes,
         endDateLabel: Strings.labels.stopsBeingOfferedOn,
         endDateInputId,
         endDatePlaceholder: Strings.placeholders.stopsBeingOfferedOn,
         endDateHelpText: Strings.help.endScheduleToday,
         submitId,
         statusId,
      });

      const captured = mocks.getCaptured();
      const entityField = captured.bodyChildren[Position.FIRST];
      const timesField = captured.bodyChildren[Position.SECOND];
      const endDateField = captured.bodyChildren[Position.THIRD];
      const actions = captured.bodyChildren[Position.FOURTH];
      const status = captured.bodyChildren.at(Position.LAST);
      assert.equal(entityField.inputId, entityInputId);
      assert.equal(timesField.inputId, timesInputId);
      assert.equal(endDateField.inputId, endDateInputId);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      mocks.restore();
   }
});
