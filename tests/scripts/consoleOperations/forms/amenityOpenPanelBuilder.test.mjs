import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityOpenPanelBuilder } from '../../../../scripts/consoleOperations/forms/amenityOpenPanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';

function _installBuilderMocks() {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createDateRangeFields: ConsoleDateRangeFieldsBuilder.createDateRangeFields,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };
   const panel = { panel: true };
   let captured;
   let dateRangeCalled = false;

   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return panel;
   };
   ConsoleSelectFieldBuilder.createSelectField = (options) => ({ kind: 'createSelectField', ...options });
   ConsoleDateRangeFieldsBuilder.createDateRangeFields = (options) => {
      dateRangeCalled = true;
      return { kind: 'createDateRangeFields', ...options };
   };
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   return {
      panel,
      getCaptured: () => captured,
      wasDateRangeCalled: () => dateRangeCalled,
      restore() {
         ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
         ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
         ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
         ConsoleActionsBuilder.createActions = originals.createActions;
         ConsoleStatusBuilder.createStatus = originals.createStatus;
      },
   };
}


test('Test_CreatePanel_TestExhibitConfig_ExpectShellOptionsWithDateRange', () => {
   const mocks = _installBuilderMocks();
   const panelId = 'exhibitOpenPanel';
   const idPrefix = 'exhibitOpen';
   const entityFieldName = 'Exhibit';
   const startHelpText = Strings.help.startImmediately;
   const endHelpText = Strings.help.keepExplicitlyOpenUntilChanged('exhibit');
   const submitId = 'submitExhibitOpen';
   const statusId = 'exhibitOpenStatus';

   try {
      const result = AmenityOpenPanelBuilder.createPanel({
         panelId,
         title: Strings.panelTitles.exhibitOpen,
         entityLabel: Strings.entityLabels.exhibit,
         emptyOptionLabel: Strings.placeholders.exhibit,
         idPrefix,
         entityFieldName,
         startHelpText,
         endHelpText,
         submitId,
         statusId,
      });

      const captured = mocks.getCaptured();
      const exhibitField = captured.bodyChildren[Position.FIRST];
      const dateRange = captured.bodyChildren[Position.SECOND];
      const actions = captured.bodyChildren[Position.THIRD];
      const status = captured.bodyChildren[Position.FOURTH];
      assert.equal(result, mocks.panel);
      assert.equal(captured.panelId, panelId);
      assert.equal(exhibitField.inputId, `${idPrefix}${entityFieldName}`);
      assert.equal(dateRange.startDateId, `${idPrefix}StartDate`);
      assert.equal(dateRange.startHelpText, startHelpText);
      assert.equal(dateRange.endHelpText, endHelpText);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      mocks.restore();
   }
});


test('Test_CreatePanel_TestTransportationConfig_ExpectNoDateRange', () => {
   const mocks = _installBuilderMocks();
   const idPrefix = 'transportationStationOpen';
   const entityFieldName = 'TransportationStation';
   const submitId = 'submitTransportationStationOpen';
   const statusId = 'transportationStationOpenStatus';

   try {
      AmenityOpenPanelBuilder.createPanel({
         panelId: 'transportationStationOpenPanel',
         title: Strings.panelTitles.transportationStationOpen,
         entityLabel: Strings.entityLabels.transportationStation,
         emptyOptionLabel: Strings.placeholders.transportationStation,
         idPrefix,
         entityFieldName,
         includeDateRange: false,
         submitId,
         statusId,
      });

      const captured = mocks.getCaptured();
      const stationField = captured.bodyChildren[Position.FIRST];
      const actions = captured.bodyChildren[Position.SECOND];
      const status = captured.bodyChildren[Position.THIRD];
      assert.equal(mocks.wasDateRangeCalled(), false);
      assert.equal(stationField.inputId, `${idPrefix}${entityFieldName}`);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      mocks.restore();
   }
});
