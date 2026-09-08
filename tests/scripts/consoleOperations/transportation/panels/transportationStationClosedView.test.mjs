import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationStationClosedView } from '../../../../../scripts/consoleOperations/transportation/panels/transportationStationClosedView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateTransportationStationClosedPanel_TestWiring_ExpectShellOptions', () => {
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
      const result = TransportationStationClosedView.createTransportationStationClosedPanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'transportationStationClosedPanel');
      assert.equal(captured.title, Strings.panelTitles.transportationStationClosed);
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'transportationStationClosedTransportationStation');
      assert.equal(captured.bodyChildren[0].label, Strings.entityLabels.transportationStation);
      assert.equal(captured.bodyChildren[1].startDateId, 'transportationStationClosedStartDate');
      assert.equal(captured.bodyChildren[1].endDateId, 'transportationStationClosedEndDate');
      assert.equal(
         captured.bodyChildren[1].endHelpText,
         Strings.help.keepClosedUntilManuallyReopened('transportation station')
      );
      assert.equal(captured.bodyChildren[2].inputId, 'transportationStationClosedMessage');
      assert.equal(captured.bodyChildren[2].label, Strings.labels.closureMessage);
      assert.equal(captured.bodyChildren[3].submitId, 'submitTransportationStationClosed');
      assert.equal(captured.bodyChildren[4].statusId, 'transportationStationClosedStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
