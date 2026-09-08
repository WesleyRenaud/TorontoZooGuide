import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopClosureOverrideView } from '../../../../../scripts/consoleOperations/giftShops/panels/giftShopClosureOverrideView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateGiftShopClosureOverridePanel_TestWiring_ExpectShellOptions', () => {
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
      const result = GiftShopClosureOverrideView.createGiftShopClosureOverridePanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'giftShopClosureOverridePanel');
      assert.equal(captured.title, Strings.panelTitles.giftShopClosureOverride);
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'giftShopClosureOverrideGiftShop');
      assert.equal(captured.bodyChildren[0].label, Strings.entityLabels.giftShop);
      assert.equal(captured.bodyChildren[0].emptyOptionLabel, Strings.placeholders.giftShop);
      assert.equal(captured.bodyChildren[1].startDateId, 'giftShopClosureOverrideStartDate');
      assert.equal(captured.bodyChildren[1].endDateId, 'giftShopClosureOverrideEndDate');
      assert.equal(
         captured.bodyChildren[1].endHelpText,
         Strings.help.continueUntilReopened('gift shop')
      );
      assert.equal(captured.bodyChildren[2].inputId, 'giftShopClosureOverrideMessage');
      assert.equal(captured.bodyChildren[2].label, Strings.labels.closedMessage);
      assert.equal(captured.bodyChildren[2].placeholder, Strings.textareas.closedMessage('gift shop'));
      assert.equal(captured.bodyChildren[3].submitId, 'submitGiftShopClosureOverride');
      assert.equal(captured.bodyChildren[4].statusId, 'giftShopClosureOverrideStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
