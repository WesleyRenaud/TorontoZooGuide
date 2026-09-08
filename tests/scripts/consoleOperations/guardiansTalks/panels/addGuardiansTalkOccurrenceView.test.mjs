import assert from 'node:assert/strict';
import test from 'node:test';

import { AddGuardiansTalkOccurrenceView } from '../../../../../scripts/consoleOperations/guardiansTalks/panels/addGuardiansTalkOccurrenceView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleDateFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateAddGuardiansTalkOccurrencePanel_TestWiring_ExpectShellOptions', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
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
   ConsoleDateFieldBuilder.createDateField = (options) => ({ kind: 'createDateField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = AddGuardiansTalkOccurrenceView.createAddGuardiansTalkOccurrencePanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'addGuardiansTalkOccurrencePanel');
      assert.equal(captured.title, Strings.panelTitles.addGuardiansTalkOccurrence);
      assert.equal(captured.bodyChildren.length, 6);
      assert.equal(captured.bodyChildren[0].inputId, 'addGuardiansTalkOccurrenceLocation');
      assert.equal(captured.bodyChildren[1].inputId, 'addGuardiansTalkOccurrenceTalkName');
      assert.equal(captured.bodyChildren[2].inputId, 'addGuardiansTalkOccurrenceDate');
      assert.equal(captured.bodyChildren[3].inputId, 'addGuardiansTalkOccurrenceTime');
      assert.equal(captured.bodyChildren[4].submitId, 'submitAddGuardiansTalkOccurrence');
      assert.equal(captured.bodyChildren[5].statusId, 'addGuardiansTalkOccurrenceStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleDateFieldBuilder.createDateField = originals.createDateField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
