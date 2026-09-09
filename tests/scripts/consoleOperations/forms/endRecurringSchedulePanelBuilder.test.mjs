import assert from 'node:assert/strict';
import test from 'node:test';

import { EndRecurringSchedulePanelBuilder } from '../../../../scripts/consoleOperations/forms/endRecurringSchedulePanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateFieldBuilder.js';
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
      createDateField: ConsoleDateFieldBuilder.createDateField,
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
   ConsoleDateFieldBuilder.createDateField = (options) => ({ kind: 'createDateField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   return { originals, getCaptured: () => captured };
}

function _restoreBuilderMocks(originals) {
   ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
   ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
   ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = originals.createScheduleTimesCheckboxField;
   ConsoleDateFieldBuilder.createDateField = originals.createDateField;
   ConsoleActionsBuilder.createActions = originals.createActions;
   ConsoleStatusBuilder.createStatus = originals.createStatus;
}

test('Test_CreatePanel_TestGuardiansTalkConfig_ExpectLocationTalkFields', () => {
   const { originals, getCaptured } = _installBuilderMocks();

   try {
      const result = EndRecurringSchedulePanelBuilder.createPanel({
         panelId: 'endGuardiansTalkSchedulePanel',
         title: Strings.panelTitles.endGuardiansTalkSchedule,
         locationLabel: Strings.labels.location,
         locationInputId: 'endGuardiansTalkScheduleLocation',
         locationEmptyOptionLabel: Strings.placeholders.location,
         talkLabel: Strings.labels.talkName,
         talkInputId: 'endGuardiansTalkScheduleTalkName',
         talkEmptyOptionLabel: Strings.placeholders.talk,
         timesLabel: Strings.labels.talkTimes,
         timesInputId: 'endGuardiansTalkScheduleTimes',
         timesHelpText: Strings.help.endScheduleTimes,
         endDateLabel: Strings.labels.endDate,
         endDateInputId: 'endGuardiansTalkScheduleEndDate',
         endDatePlaceholder: Strings.placeholders.scheduleEndDate,
         endDateHelpText: Strings.help.endScheduleToday,
         submitId: 'submitEndGuardiansTalkSchedule',
         statusId: 'endGuardiansTalkScheduleStatus',
      });

      const captured = getCaptured();
      assert.deepEqual(result, { panel: true });
      assert.equal(captured.panelId, 'endGuardiansTalkSchedulePanel');
      assert.equal(captured.bodyChildren.length, 6);
      assert.equal(captured.bodyChildren[0].inputId, 'endGuardiansTalkScheduleLocation');
      assert.equal(captured.bodyChildren[1].inputId, 'endGuardiansTalkScheduleTalkName');
      assert.equal(captured.bodyChildren[2].inputId, 'endGuardiansTalkScheduleTimes');
      assert.equal(captured.bodyChildren[3].inputId, 'endGuardiansTalkScheduleEndDate');
      assert.equal(captured.bodyChildren[4].submitId, 'submitEndGuardiansTalkSchedule');
      assert.equal(captured.bodyChildren[5].statusId, 'endGuardiansTalkScheduleStatus');
   } finally {
      _restoreBuilderMocks(originals);
   }
});

test('Test_CreatePanel_TestWildEncounterConfig_ExpectEntityField', () => {
   const { originals, getCaptured } = _installBuilderMocks();

   try {
      EndRecurringSchedulePanelBuilder.createPanel({
         panelId: 'endWildEncounterSchedulePanel',
         title: Strings.panelTitles.endWildEncounterSchedule,
         entityLabel: Strings.entityLabels.wildEncounter,
         entityInputId: 'endWildEncounterScheduleName',
         entityEmptyOptionLabel: Strings.placeholders.wildEncounter,
         timesLabel: Strings.labels.encounterTimes,
         timesInputId: 'endWildEncounterScheduleTimes',
         timesHelpText: Strings.help.endScheduleTimes,
         endDateLabel: Strings.labels.endDate,
         endDateInputId: 'endWildEncounterScheduleDate',
         endDatePlaceholder: Strings.placeholders.scheduleEndDate,
         endDateHelpText: Strings.help.endScheduleToday,
         submitId: 'submitEndWildEncounterSchedule',
         statusId: 'endWildEncounterScheduleStatus',
      });

      const captured = getCaptured();
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'endWildEncounterScheduleName');
      assert.equal(captured.bodyChildren[1].inputId, 'endWildEncounterScheduleTimes');
      assert.equal(captured.bodyChildren[2].inputId, 'endWildEncounterScheduleDate');
      assert.equal(captured.bodyChildren[3].submitId, 'submitEndWildEncounterSchedule');
      assert.equal(captured.bodyChildren[4].statusId, 'endWildEncounterScheduleStatus');
   } finally {
      _restoreBuilderMocks(originals);
   }
});
