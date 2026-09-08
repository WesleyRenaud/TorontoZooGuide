import assert from 'node:assert/strict';
import test from 'node:test';

import { EndWildEncounterScheduleView } from '../../../../../scripts/consoleOperations/wildEncounters/panels/endWildEncounterScheduleView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleDateFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateEndWildEncounterSchedulePanel_TestWiring_ExpectShellOptions', () => {
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
   ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = (options) => ({ kind: 'createScheduleTimesCheckboxField', ...options });
   ConsoleDateFieldBuilder.createDateField = (options) => ({ kind: 'createDateField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = EndWildEncounterScheduleView.createEndWildEncounterSchedulePanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'endWildEncounterSchedulePanel');
      assert.equal(captured.title, Strings.panelTitles.endWildEncounterSchedule);
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'endWildEncounterScheduleName');
      assert.equal(captured.bodyChildren[1].inputId, 'endWildEncounterScheduleTimes');
      assert.equal(captured.bodyChildren[1].helpText, Strings.help.endScheduleTimes);
      assert.equal(captured.bodyChildren[2].inputId, 'endWildEncounterScheduleDate');
      assert.equal(captured.bodyChildren[2].helpText, Strings.help.endScheduleToday);
      assert.equal(captured.bodyChildren[3].submitId, 'submitEndWildEncounterSchedule');
      assert.equal(captured.bodyChildren[4].statusId, 'endWildEncounterScheduleStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = originals.createScheduleTimesCheckboxField;
      ConsoleDateFieldBuilder.createDateField = originals.createDateField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
