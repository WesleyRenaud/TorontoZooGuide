import assert from 'node:assert/strict';
import test from 'node:test';

import { GlobalAmenityStatusPanelBuilder } from '../../../../scripts/consoleOperations/forms/globalAmenityStatusPanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_CreatePanel_TestOpenConfig_ExpectDateRangeOnly', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createDateRangeFields: ConsoleDateRangeFieldsBuilder.createDateRangeFields,
      createTextareaField: ConsoleTextareaFieldBuilder.createTextareaField,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };

   let captured;
   let textareaCalls = 0;
   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return { panel: true };
   };
   ConsoleDateRangeFieldsBuilder.createDateRangeFields = (options) => ({ kind: 'createDateRangeFields', ...options });
   ConsoleTextareaFieldBuilder.createTextareaField = (options) => {
      textareaCalls += 1;
      return { kind: 'createTextareaField', ...options };
   };
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = GlobalAmenityStatusPanelBuilder.createPanel({
         panelId: 'drinkingFountainsOpenPanel',
         title: Strings.panelTitles.drinkingFountainsOpen,
         idPrefix: 'drinkingFountainsOpen',
         endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('drinking fountains', 'they are'),
         submitId: 'submitDrinkingFountainsOpen',
         statusId: 'drinkingFountainsOpenStatus',
      });

      assert.deepEqual(result, { panel: true });
      assert.equal(captured.panelId, 'drinkingFountainsOpenPanel');
      assert.equal(captured.title, Strings.panelTitles.drinkingFountainsOpen);
      assert.equal(captured.bodyChildren.length, 3);
      assert.equal(captured.bodyChildren[0].startDateId, 'drinkingFountainsOpenStartDate');
      assert.equal(captured.bodyChildren[0].startHelpText, Strings.help.startImmediately);
      assert.equal(captured.bodyChildren[0].endDateId, 'drinkingFountainsOpenEndDate');
      assert.equal(
         captured.bodyChildren[0].endHelpText,
         Strings.help.keepExplicitlyOpenUntilChanged('drinking fountains', 'they are')
      );
      assert.equal(captured.bodyChildren[1].submitId, 'submitDrinkingFountainsOpen');
      assert.equal(captured.bodyChildren[2].statusId, 'drinkingFountainsOpenStatus');
      assert.equal(textareaCalls, 0);
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});

test('Test_CreatePanel_TestClosedConfig_ExpectDateRangeAndMessage', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
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
   ConsoleDateRangeFieldsBuilder.createDateRangeFields = (options) => ({ kind: 'createDateRangeFields', ...options });
   ConsoleTextareaFieldBuilder.createTextareaField = (options) => ({ kind: 'createTextareaField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      GlobalAmenityStatusPanelBuilder.createPanel({
         panelId: 'drinkingFountainsClosedPanel',
         title: Strings.panelTitles.drinkingFountainsClosed,
         idPrefix: 'drinkingFountainsClosed',
         endHelpText: Strings.help.continueUntilReopened('drinking fountains'),
         includeMessage: true,
         messageLabel: Strings.labels.closedMessage,
         messagePlaceholder: Strings.textareas.drinkingFountainsClosedMessage,
         submitId: 'submitDrinkingFountainsClosed',
         statusId: 'drinkingFountainsClosedStatus',
      });

      assert.equal(captured.bodyChildren.length, 4);
      assert.equal(captured.bodyChildren[0].startDateId, 'drinkingFountainsClosedStartDate');
      assert.equal(captured.bodyChildren[0].endHelpText, Strings.help.continueUntilReopened('drinking fountains'));
      assert.equal(captured.bodyChildren[1].label, Strings.labels.closedMessage);
      assert.equal(captured.bodyChildren[1].inputId, 'drinkingFountainsClosedMessage');
      assert.equal(
         captured.bodyChildren[1].placeholder,
         Strings.textareas.drinkingFountainsClosedMessage
      );
      assert.equal(captured.bodyChildren[2].submitId, 'submitDrinkingFountainsClosed');
      assert.equal(captured.bodyChildren[3].statusId, 'drinkingFountainsClosedStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
