import assert from 'node:assert/strict';
import test from 'node:test';

import { CancelOccurrencePanelBuilder } from '../../../../scripts/consoleOperations/forms/cancelOccurrencePanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Strings } from '../../../../scripts/strings.js';

function _installBuilderMocks() {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createScheduleTimesCheckboxField: ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };

   let captured;
   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return { panel: true };
   };
   ConsoleSelectFieldBuilder.createSelectField = (options) => ({ kind: 'createSelectField', ...options });
   ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = (options) => ({
      kind: 'createScheduleTimesCheckboxField',
      ...options,
   });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   return { originals, getCaptured: () => captured };
}

function _restoreBuilderMocks(originals) {
   ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
   ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
   ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = originals.createScheduleTimesCheckboxField;
   ConsoleActionsBuilder.createActions = originals.createActions;
   ConsoleStatusBuilder.createStatus = originals.createStatus;
}

test('Test_CreatePanel_TestGuardiansTalkConfig_ExpectLocationTalkFields', () => {
   const { originals, getCaptured } = _installBuilderMocks();

   try {
      const result = CancelOccurrencePanelBuilder.createPanel({
         panelId: 'cancelGuardiansTalkOccurrencePanel',
         title: Strings.panelTitles.cancelGuardiansTalkOccurrence,
         locationLabel: Strings.labels.location,
         locationInputId: 'cancelGuardiansTalkOccurrenceLocation',
         locationEmptyOptionLabel: Strings.placeholders.location,
         talkLabel: Strings.labels.talkName,
         talkInputId: 'cancelGuardiansTalkOccurrenceTalkName',
         talkEmptyOptionLabel: Strings.placeholders.talk,
         dateLabel: Strings.labels.date,
         dateInputId: 'cancelGuardiansTalkOccurrenceDate',
         dateEmptyOptionLabel: Strings.placeholders.date,
         timesLabel: Strings.labels.talkTimes,
         timesInputId: 'cancelGuardiansTalkOccurrenceTimes',
         timesHelpText: Strings.help.cancelOccurrenceTimes,
         submitId: 'submitCancelGuardiansTalkOccurrence',
         statusId: 'cancelGuardiansTalkOccurrenceStatus',
      });

      const captured = getCaptured();
      assert.deepEqual(result, { panel: true });
      assert.equal(captured.panelId, 'cancelGuardiansTalkOccurrencePanel');
      assert.equal(captured.bodyChildren.length, 6);
      assert.equal(captured.bodyChildren[0].inputId, 'cancelGuardiansTalkOccurrenceLocation');
      assert.equal(captured.bodyChildren[1].inputId, 'cancelGuardiansTalkOccurrenceTalkName');
      assert.equal(captured.bodyChildren[2].inputId, 'cancelGuardiansTalkOccurrenceDate');
      assert.equal(captured.bodyChildren[3].inputId, 'cancelGuardiansTalkOccurrenceTimes');
      assert.equal(captured.bodyChildren[4].submitId, 'submitCancelGuardiansTalkOccurrence');
      assert.equal(captured.bodyChildren[5].statusId, 'cancelGuardiansTalkOccurrenceStatus');
   } finally {
      _restoreBuilderMocks(originals);
   }
});

test('Test_CreatePanel_TestWildEncounterConfig_ExpectEntityField', () => {
   const { originals, getCaptured } = _installBuilderMocks();

   try {
      CancelOccurrencePanelBuilder.createPanel({
         panelId: 'cancelWildEncounterOccurrencePanel',
         title: Strings.panelTitles.cancelWildEncounterOccurrence,
         entityLabel: Strings.entityLabels.wildEncounter,
         entityInputId: 'cancelWildEncounterOccurrenceName',
         entityEmptyOptionLabel: Strings.placeholders.wildEncounter,
         dateLabel: Strings.labels.date,
         dateInputId: 'cancelWildEncounterOccurrenceDate',
         dateEmptyOptionLabel: Strings.placeholders.date,
         timesLabel: Strings.labels.encounterTimes,
         timesInputId: 'cancelWildEncounterOccurrenceTimes',
         timesHelpText: Strings.help.cancelOccurrenceTimes,
         submitId: 'submitCancelWildEncounterOccurrence',
         statusId: 'cancelWildEncounterOccurrenceStatus',
      });

      const captured = getCaptured();
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'cancelWildEncounterOccurrenceName');
      assert.equal(captured.bodyChildren[1].inputId, 'cancelWildEncounterOccurrenceDate');
      assert.equal(captured.bodyChildren[2].inputId, 'cancelWildEncounterOccurrenceTimes');
      assert.equal(captured.bodyChildren[3].submitId, 'submitCancelWildEncounterOccurrence');
      assert.equal(captured.bodyChildren[4].statusId, 'cancelWildEncounterOccurrenceStatus');
   } finally {
      _restoreBuilderMocks(originals);
   }
});
