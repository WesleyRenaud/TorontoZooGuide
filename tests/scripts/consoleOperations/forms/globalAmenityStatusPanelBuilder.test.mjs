import assert from 'node:assert/strict';
import test from 'node:test';

import { GlobalAmenityStatusPanelBuilder } from '../../../../scripts/consoleOperations/forms/globalAmenityStatusPanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';

function _installBuilderMocks() {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createDateRangeFields: ConsoleDateRangeFieldsBuilder.createDateRangeFields,
      createTextareaField: ConsoleTextareaFieldBuilder.createTextareaField,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };
   const panel = { panel: true };
   let captured;
   let textareaCalls = 0;

   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return panel;
   };
   ConsoleDateRangeFieldsBuilder.createDateRangeFields = (options) => ({ kind: 'createDateRangeFields', ...options });
   ConsoleTextareaFieldBuilder.createTextareaField = (options) => {
      textareaCalls += 1;
      return { kind: 'createTextareaField', ...options };
   };
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   return {
      panel,
      getCaptured: () => captured,
      getTextareaCalls: () => textareaCalls,
      restore() {
         ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
         ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
         ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
         ConsoleActionsBuilder.createActions = originals.createActions;
         ConsoleStatusBuilder.createStatus = originals.createStatus;
      },
   };
}


test('Test_CreatePanel_TestOpenConfig_ExpectDateRangeOnly', () => {
   const mocks = _installBuilderMocks();
   const panelId = 'drinkingFountainsOpenPanel';
   const title = Strings.panelTitles.drinkingFountainsOpen;
   const idPrefix = 'drinkingFountainsOpen';
   const endHelpText = Strings.help.keepExplicitlyOpenUntilChanged('drinking fountains', 'they are');
   const submitId = 'submitDrinkingFountainsOpen';
   const statusId = 'drinkingFountainsOpenStatus';

   try {
      const result = GlobalAmenityStatusPanelBuilder.createPanel({
         panelId,
         title,
         idPrefix,
         endHelpText,
         submitId,
         statusId,
      });

      const captured = mocks.getCaptured();
      const dateRange = captured.bodyChildren[Position.FIRST];
      const actions = captured.bodyChildren[Position.SECOND];
      const status = captured.bodyChildren[Position.THIRD];
      assert.equal(result, mocks.panel);
      assert.equal(captured.panelId, panelId);
      assert.equal(captured.title, title);
      assert.equal(dateRange.startDateId, `${idPrefix}StartDate`);
      assert.equal(dateRange.startHelpText, Strings.help.startImmediately);
      assert.equal(dateRange.endDateId, `${idPrefix}EndDate`);
      assert.equal(dateRange.endHelpText, endHelpText);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
      assert.equal(mocks.getTextareaCalls(), 0);
   } finally {
      mocks.restore();
   }
});


test('Test_CreatePanel_TestClosedConfig_ExpectDateRangeAndMessage', () => {
   const mocks = _installBuilderMocks();
   const idPrefix = 'drinkingFountainsClosed';
   const endHelpText = Strings.help.continueUntilReopened('drinking fountains');
   const messageLabel = Strings.labels.closedMessage;
   const messagePlaceholder = Strings.textareas.drinkingFountainsClosedMessage;
   const submitId = 'submitDrinkingFountainsClosed';
   const statusId = 'drinkingFountainsClosedStatus';

   try {
      GlobalAmenityStatusPanelBuilder.createPanel({
         panelId: 'drinkingFountainsClosedPanel',
         title: Strings.panelTitles.drinkingFountainsClosed,
         idPrefix,
         endHelpText,
         includeMessage: true,
         messageLabel,
         messagePlaceholder,
         submitId,
         statusId,
      });

      const captured = mocks.getCaptured();
      const dateRange = captured.bodyChildren[Position.FIRST];
      const messageField = captured.bodyChildren[Position.SECOND];
      const actions = captured.bodyChildren[Position.THIRD];
      const status = captured.bodyChildren[Position.FOURTH];
      assert.equal(dateRange.startDateId, `${idPrefix}StartDate`);
      assert.equal(dateRange.endHelpText, endHelpText);
      assert.equal(messageField.label, messageLabel);
      assert.equal(messageField.inputId, `${idPrefix}Message`);
      assert.equal(messageField.placeholder, messagePlaceholder);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      mocks.restore();
   }
});
