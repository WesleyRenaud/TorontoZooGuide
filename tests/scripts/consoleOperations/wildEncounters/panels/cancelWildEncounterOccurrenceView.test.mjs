import assert from 'node:assert/strict';
import test from 'node:test';

import { CancelWildEncounterOccurrenceView } from '../../../../../scripts/consoleOperations/wildEncounters/panels/cancelWildEncounterOccurrenceView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateCancelWildEncounterOccurrencePanel_TestWiring_ExpectShellOptions', () => {
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
   ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = (options) => ({ kind: 'createScheduleTimesCheckboxField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = CancelWildEncounterOccurrenceView.createCancelWildEncounterOccurrencePanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'cancelWildEncounterOccurrencePanel');
      assert.equal(captured.title, Strings.panelTitles.cancelWildEncounterOccurrence);
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'cancelWildEncounterOccurrenceName');
      assert.equal(captured.bodyChildren[1].inputId, 'cancelWildEncounterOccurrenceDate');
      assert.equal(captured.bodyChildren[2].inputId, 'cancelWildEncounterOccurrenceTimes');
      assert.equal(captured.bodyChildren[2].helpText, Strings.help.cancelOccurrenceTimes);
      assert.equal(captured.bodyChildren[3].submitId, 'submitCancelWildEncounterOccurrence');
      assert.equal(captured.bodyChildren[4].statusId, 'cancelWildEncounterOccurrenceStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = originals.createScheduleTimesCheckboxField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
