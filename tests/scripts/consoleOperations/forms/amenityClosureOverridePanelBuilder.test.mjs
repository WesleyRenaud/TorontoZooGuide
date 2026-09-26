import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityClosureOverridePanelBuilder } from '../../../../scripts/consoleOperations/forms/amenityClosureOverridePanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_CreatePanel_TestGiftShopConfig_ExpectShellOptions', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createDateRangeFields: ConsoleDateRangeFieldsBuilder.createDateRangeFields,
      createTextareaField: ConsoleTextareaFieldBuilder.createTextareaField,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };
   const panel = { panel: true };
   const panelId = 'giftShopClosureOverridePanel';
   const title = Strings.panelTitles.giftShopClosureOverride;
   const idPrefix = 'giftShopClosureOverride';
   const entityFieldName = 'GiftShop';
   const endHelpText = Strings.help.continueUntilReopened('gift shop');
   const messageLabel = Strings.labels.closedMessage;
   const messagePlaceholder = Strings.textareas.closedMessage('gift shop');
   const submitId = 'submitGiftShopClosureOverride';
   const statusId = 'giftShopClosureOverrideStatus';
   let captured;

   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return panel;
   };
   ConsoleSelectFieldBuilder.createSelectField = (options) => ({ kind: 'createSelectField', ...options });
   ConsoleDateRangeFieldsBuilder.createDateRangeFields = (options) => ({ kind: 'createDateRangeFields', ...options });
   ConsoleTextareaFieldBuilder.createTextareaField = (options) => ({ kind: 'createTextareaField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = AmenityClosureOverridePanelBuilder.createPanel({
         panelId,
         title,
         entityLabel: Strings.entityLabels.giftShop,
         emptyOptionLabel: Strings.placeholders.giftShop,
         idPrefix,
         entityFieldName,
         endHelpText,
         messageLabel,
         messagePlaceholder,
         submitId,
         statusId,
      });

      const entityField = captured.bodyChildren[Position.FIRST];
      const dateRange = captured.bodyChildren[Position.SECOND];
      const messageField = captured.bodyChildren[Position.THIRD];
      const actions = captured.bodyChildren[Position.FOURTH];
      const status = captured.bodyChildren.at(Position.LAST);
      assert.equal(result, panel);
      assert.equal(captured.panelId, panelId);
      assert.equal(captured.title, title);
      assert.equal(entityField.inputId, `${idPrefix}${entityFieldName}`);
      assert.equal(dateRange.startDateId, `${idPrefix}StartDate`);
      assert.equal(dateRange.startHelpText, Strings.help.startImmediately);
      assert.equal(dateRange.endDateId, `${idPrefix}EndDate`);
      assert.equal(dateRange.endHelpText, endHelpText);
      assert.equal(messageField.inputId, `${idPrefix}Message`);
      assert.equal(messageField.label, messageLabel);
      assert.equal(messageField.placeholder, messagePlaceholder);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
