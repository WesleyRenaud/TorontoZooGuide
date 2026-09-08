import assert from 'node:assert/strict';
import test from 'node:test';

import { RestroomAlertView } from '../../../../../scripts/consoleOperations/restrooms/panels/restroomAlertView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateRestroomAlertPanel_TestWiring_ExpectShellOptions', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createDateRangeFields: ConsoleDateRangeFieldsBuilder.createDateRangeFields,
      createTextareaField: ConsoleTextareaFieldBuilder.createTextareaField,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };

   let captured;
   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return { panel: true };
   };
   ConsoleSelectFieldBuilder.createSelectField = (options) => ({ kind: 'createSelectField', ...options });
   ConsoleDateRangeFieldsBuilder.createDateRangeFields = (options) => ({ kind: 'createDateRangeFields', ...options });
   ConsoleTextareaFieldBuilder.createTextareaField = (options) => ({ kind: 'createTextareaField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = RestroomAlertView.createRestroomAlertPanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'restroomAlertPanel');
      assert.equal(captured.title, Strings.panelTitles.restroomAlert);
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'restroomAlertRestroom');
      assert.equal(captured.bodyChildren[1].startDateId, 'restroomAlertStartDate');
      assert.equal(captured.bodyChildren[1].endDateId, 'restroomAlertEndDate');
      assert.equal(captured.bodyChildren[1].endHelpText, Strings.help.keepAlertActiveUntilRemoved);
      assert.equal(captured.bodyChildren[2].inputId, 'restroomAlertMessage');
      assert.equal(captured.bodyChildren[2].label, Strings.labels.alertMessage);
      assert.equal(captured.bodyChildren[2].placeholder, Strings.placeholders.restroomAlertExample);
      assert.equal(captured.bodyChildren[3].submitId, 'submitRestroomAlert');
      assert.equal(captured.bodyChildren[4].statusId, 'restroomAlertStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
