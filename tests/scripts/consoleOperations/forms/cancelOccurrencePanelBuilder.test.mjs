import assert from 'node:assert/strict';
import test from 'node:test';

import { CancelOccurrencePanelBuilder } from '../../../../scripts/consoleOperations/forms/cancelOccurrencePanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
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
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   return {
      panel,
      getCaptured: () => captured,
      restore() {
         ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
         ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
         ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = originals.createScheduleTimesCheckboxField;
         ConsoleActionsBuilder.createActions = originals.createActions;
         ConsoleStatusBuilder.createStatus = originals.createStatus;
      },
   };
}


test('Test_CreatePanel_TestGuardiansTalkConfig_ExpectLocationTalkFields', () => {
   const mocks = _installBuilderMocks();
   const panelId = 'cancelGuardiansTalkOccurrencePanel';
   const locationInputId = 'cancelGuardiansTalkOccurrenceLocation';
   const talkInputId = 'cancelGuardiansTalkOccurrenceTalkName';
   const dateInputId = 'cancelGuardiansTalkOccurrenceDate';
   const timesInputId = 'cancelGuardiansTalkOccurrenceTimes';
   const submitId = 'submitCancelGuardiansTalkOccurrence';
   const statusId = 'cancelGuardiansTalkOccurrenceStatus';

   try {
      const result = CancelOccurrencePanelBuilder.createPanel({
         panelId,
         title: Strings.panelTitles.cancelGuardiansTalkOccurrence,
         locationLabel: Strings.labels.location,
         locationInputId,
         locationEmptyOptionLabel: Strings.placeholders.location,
         talkLabel: Strings.labels.talkName,
         talkInputId,
         talkEmptyOptionLabel: Strings.placeholders.talk,
         dateLabel: Strings.labels.date,
         dateInputId,
         dateEmptyOptionLabel: Strings.placeholders.date,
         timesLabel: Strings.labels.talkTimes,
         timesInputId,
         timesHelpText: Strings.help.cancelOccurrenceTimes,
         submitId,
         statusId,
      });

      const captured = mocks.getCaptured();
      const [
         locationField,
         talkField,
         dateField,
         timesField,
         actions,
         status,
      ] = captured.bodyChildren;
      assert.equal(result, mocks.panel);
      assert.equal(captured.panelId, panelId);
      assert.equal(locationField.inputId, locationInputId);
      assert.equal(talkField.inputId, talkInputId);
      assert.equal(dateField.inputId, dateInputId);
      assert.equal(timesField.inputId, timesInputId);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      mocks.restore();
   }
});


test('Test_CreatePanel_TestWildEncounterConfig_ExpectEntityField', () => {
   const mocks = _installBuilderMocks();
   const entityInputId = 'cancelWildEncounterOccurrenceName';
   const dateInputId = 'cancelWildEncounterOccurrenceDate';
   const timesInputId = 'cancelWildEncounterOccurrenceTimes';
   const submitId = 'submitCancelWildEncounterOccurrence';
   const statusId = 'cancelWildEncounterOccurrenceStatus';

   try {
      CancelOccurrencePanelBuilder.createPanel({
         panelId: 'cancelWildEncounterOccurrencePanel',
         title: Strings.panelTitles.cancelWildEncounterOccurrence,
         entityLabel: Strings.entityLabels.wildEncounter,
         entityInputId,
         entityEmptyOptionLabel: Strings.placeholders.wildEncounter,
         dateLabel: Strings.labels.date,
         dateInputId,
         dateEmptyOptionLabel: Strings.placeholders.date,
         timesLabel: Strings.labels.encounterTimes,
         timesInputId,
         timesHelpText: Strings.help.cancelOccurrenceTimes,
         submitId,
         statusId,
      });

      const captured = mocks.getCaptured();
      const entityField = captured.bodyChildren[Position.FIRST];
      const dateField = captured.bodyChildren[Position.SECOND];
      const timesField = captured.bodyChildren[Position.THIRD];
      const actions = captured.bodyChildren[Position.FOURTH];
      const status = captured.bodyChildren.at(Position.LAST);
      assert.equal(entityField.inputId, entityInputId);
      assert.equal(dateField.inputId, dateInputId);
      assert.equal(timesField.inputId, timesInputId);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      mocks.restore();
   }
});
