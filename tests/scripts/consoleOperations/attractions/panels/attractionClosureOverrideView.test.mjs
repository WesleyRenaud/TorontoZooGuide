import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionClosureOverrideView } from '../../../../../scripts/consoleOperations/attractions/panels/attractionClosureOverrideView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateAttractionClosureOverridePanel_TestWiring_ExpectShellOptions', () => {
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
      const result = AttractionClosureOverrideView.createAttractionClosureOverridePanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'attractionClosureOverridePanel');
      assert.equal(captured.title, Strings.panelTitles.attractionClosureOverride);
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'attractionClosureOverrideAttraction');
      assert.equal(captured.bodyChildren[0].label, Strings.entityLabels.attraction);
      assert.equal(captured.bodyChildren[0].emptyOptionLabel, Strings.placeholders.attraction);
      assert.equal(captured.bodyChildren[1].startDateId, 'attractionClosureOverrideStartDate');
      assert.equal(captured.bodyChildren[1].startHelpText, Strings.help.startImmediately);
      assert.equal(captured.bodyChildren[1].endDateId, 'attractionClosureOverrideEndDate');
      assert.equal(
         captured.bodyChildren[1].endHelpText,
         Strings.help.keepClosedUntilManuallyReopened('attraction')
      );
      assert.equal(captured.bodyChildren[2].inputId, 'attractionClosureOverrideMessage');
      assert.equal(captured.bodyChildren[2].label, Strings.labels.closureMessage);
      assert.equal(captured.bodyChildren[2].placeholder, Strings.textareas.closureMessage);
      assert.equal(captured.bodyChildren[3].submitId, 'submitAttractionClosureOverride');
      assert.equal(captured.bodyChildren[4].statusId, 'attractionClosureOverrideStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
