import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityClosedPanelBuilder } from '../../../../scripts/consoleOperations/forms/amenityClosedPanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';

function _installBuilderMocks() {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createDateRangeFields: ConsoleDateRangeFieldsBuilder.createDateRangeFields,
      createTextareaField: ConsoleTextareaFieldBuilder.createTextareaField,
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
   ConsoleDateRangeFieldsBuilder.createDateRangeFields = (options) => ({ kind: 'createDateRangeFields', ...options });
   ConsoleTextareaFieldBuilder.createTextareaField = (options) => ({ kind: 'createTextareaField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   return {
      panel,
      getCaptured: () => captured,
      restore() {
         ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
         ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
         ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
         ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
         ConsoleActionsBuilder.createActions = originals.createActions;
         ConsoleStatusBuilder.createStatus = originals.createStatus;
      },
   };
}


test('Test_CreatePanel_TestGiftShopConfig_ExpectShellOptions', () => {
   const mocks = _installBuilderMocks();
   const panelId = 'giftShopClosedPanel';
   const idPrefix = 'giftShopClosed';
   const entityFieldName = 'GiftShop';
   const endHelpText = Strings.help.continueUntilReopened('gift shop');
   const messageLabel = Strings.labels.closedMessage;
   const messagePlaceholder = Strings.textareas.closedMessage('gift shop');
   const submitId = 'submitGiftShopClosed';
   const statusId = 'giftShopClosedStatus';

   try {
      const result = AmenityClosedPanelBuilder.createPanel({
         panelId,
         title: Strings.panelTitles.giftShopClosed,
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

      const captured = mocks.getCaptured();
      const entityField = captured.bodyChildren[Position.FIRST];
      const dateRange = captured.bodyChildren[Position.SECOND];
      const messageField = captured.bodyChildren[Position.THIRD];
      const actions = captured.bodyChildren[Position.FOURTH];
      const status = captured.bodyChildren.at(Position.LAST);
      assert.equal(result, mocks.panel);
      assert.equal(captured.panelId, panelId);
      assert.equal(entityField.inputId, `${idPrefix}${entityFieldName}`);
      assert.equal(dateRange.startDateId, `${idPrefix}StartDate`);
      assert.equal(dateRange.startHelpText, undefined);
      assert.equal(dateRange.endHelpText, endHelpText);
      assert.equal(messageField.label, messageLabel);
      assert.equal(messageField.placeholder, messagePlaceholder);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      mocks.restore();
   }
});


test('Test_CreatePanel_TestAttractionConfig_ExpectStartHelpText', () => {
   const mocks = _installBuilderMocks();
   const startHelpText = Strings.help.startImmediately;
   const endHelpText = Strings.help.keepClosedUntilManuallyReopened('attraction');
   const messageLabel = Strings.labels.closureMessage;
   const messagePlaceholder = Strings.textareas.closureMessage;

   try {
      AmenityClosedPanelBuilder.createPanel({
         panelId: 'attractionClosedPanel',
         title: Strings.panelTitles.attractionClosed,
         entityLabel: Strings.entityLabels.attraction,
         emptyOptionLabel: Strings.placeholders.attraction,
         idPrefix: 'attractionClosed',
         entityFieldName: 'Attraction',
         startHelpText,
         endHelpText,
         messageLabel,
         messagePlaceholder,
         submitId: 'submitAttractionClosed',
         statusId: 'attractionClosedStatus',
      });

      const captured = mocks.getCaptured();
      const dateRange = captured.bodyChildren[Position.SECOND];
      const messageField = captured.bodyChildren[Position.THIRD];
      assert.equal(dateRange.startHelpText, startHelpText);
      assert.equal(dateRange.endHelpText, endHelpText);
      assert.equal(messageField.label, messageLabel);
      assert.equal(messageField.placeholder, messagePlaceholder);
   } finally {
      mocks.restore();
   }
});
