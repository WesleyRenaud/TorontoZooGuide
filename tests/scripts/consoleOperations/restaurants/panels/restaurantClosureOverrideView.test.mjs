import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantClosureOverrideView } from '../../../../../scripts/consoleOperations/restaurants/panels/restaurantClosureOverrideView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateRestaurantClosureOverridePanel_TestWiring_ExpectShellOptions', () => {
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
      const result = RestaurantClosureOverrideView.createRestaurantClosureOverridePanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'restaurantClosureOverridePanel');
      assert.equal(captured.title, Strings.panelTitles.restaurantClosureOverride);
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'restaurantClosureOverrideRestaurant');
      assert.equal(captured.bodyChildren[0].label, Strings.entityLabels.restaurant);
      assert.equal(captured.bodyChildren[1].startDateId, 'restaurantClosureOverrideStartDate');
      assert.equal(captured.bodyChildren[1].endDateId, 'restaurantClosureOverrideEndDate');
      assert.equal(
         captured.bodyChildren[1].endHelpText,
         Strings.help.continueUntilReopened('restaurant')
      );
      assert.equal(captured.bodyChildren[2].inputId, 'restaurantClosureOverrideMessage');
      assert.equal(captured.bodyChildren[2].placeholder, Strings.textareas.closedMessage('restaurant'));
      assert.equal(captured.bodyChildren[3].submitId, 'submitRestaurantClosureOverride');
      assert.equal(captured.bodyChildren[4].statusId, 'restaurantClosureOverrideStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
