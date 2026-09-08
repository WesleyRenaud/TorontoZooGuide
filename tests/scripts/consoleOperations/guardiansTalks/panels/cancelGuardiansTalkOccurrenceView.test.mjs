import assert from 'node:assert/strict';
import test from 'node:test';

import { CancelGuardiansTalkOccurrenceView } from '../../../../../scripts/consoleOperations/guardiansTalks/panels/cancelGuardiansTalkOccurrenceView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateCancelGuardiansTalkOccurrencePanel_TestWiring_ExpectShellOptions', () => {
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
      const result = CancelGuardiansTalkOccurrenceView.createCancelGuardiansTalkOccurrencePanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'cancelGuardiansTalkOccurrencePanel');
      assert.equal(captured.title, Strings.panelTitles.cancelGuardiansTalkOccurrence);
      assert.equal(captured.bodyChildren.length, 6);
      assert.equal(captured.bodyChildren[0].inputId, 'cancelGuardiansTalkOccurrenceLocation');
      assert.equal(captured.bodyChildren[1].inputId, 'cancelGuardiansTalkOccurrenceTalkName');
      assert.equal(captured.bodyChildren[2].inputId, 'cancelGuardiansTalkOccurrenceDate');
      assert.equal(captured.bodyChildren[3].inputId, 'cancelGuardiansTalkOccurrenceTimes');
      assert.equal(captured.bodyChildren[3].helpText, Strings.help.cancelOccurrenceTimes);
      assert.equal(captured.bodyChildren[4].submitId, 'submitCancelGuardiansTalkOccurrence');
      assert.equal(captured.bodyChildren[5].statusId, 'cancelGuardiansTalkOccurrenceStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField = originals.createScheduleTimesCheckboxField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
