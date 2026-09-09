import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityOpenPanelBuilder } from '../../../../scripts/consoleOperations/forms/amenityOpenPanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_CreatePanel_TestExhibitConfig_ExpectShellOptionsWithDateRange', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createDateRangeFields: ConsoleDateRangeFieldsBuilder.createDateRangeFields,
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
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = AmenityOpenPanelBuilder.createPanel({
         panelId: 'exhibitOpenPanel',
         title: Strings.panelTitles.exhibitOpen,
         entityLabel: Strings.entityLabels.exhibit,
         emptyOptionLabel: Strings.placeholders.exhibit,
         idPrefix: 'exhibitOpen',
         entityFieldName: 'Exhibit',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('exhibit'),
         submitId: 'submitExhibitOpen',
         statusId: 'exhibitOpenStatus',
      });

      assert.deepEqual(result, { panel: true });
      assert.equal(captured.panelId, 'exhibitOpenPanel');
      assert.equal(captured.bodyChildren.length, 4);
      assert.equal(captured.bodyChildren[0].inputId, 'exhibitOpenExhibit');
      assert.equal(captured.bodyChildren[1].startDateId, 'exhibitOpenStartDate');
      assert.equal(captured.bodyChildren[1].startHelpText, Strings.help.startImmediately);
      assert.equal(
         captured.bodyChildren[1].endHelpText,
         Strings.help.keepExplicitlyOpenUntilChanged('exhibit')
      );
      assert.equal(captured.bodyChildren[2].submitId, 'submitExhibitOpen');
      assert.equal(captured.bodyChildren[3].statusId, 'exhibitOpenStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});

test('Test_CreatePanel_TestTransportationConfig_ExpectNoDateRange', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createDateRangeFields: ConsoleDateRangeFieldsBuilder.createDateRangeFields,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };

   let captured;
   let dateRangeCalled = false;
   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return { panel: true };
   };
   ConsoleSelectFieldBuilder.createSelectField = (options) => ({ kind: 'createSelectField', ...options });
   ConsoleDateRangeFieldsBuilder.createDateRangeFields = (options) => {
      dateRangeCalled = true;
      return { kind: 'createDateRangeFields', ...options };
   };
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      AmenityOpenPanelBuilder.createPanel({
         panelId: 'transportationStationOpenPanel',
         title: Strings.panelTitles.transportationStationOpen,
         entityLabel: Strings.entityLabels.transportationStation,
         emptyOptionLabel: Strings.placeholders.transportationStation,
         idPrefix: 'transportationStationOpen',
         entityFieldName: 'TransportationStation',
         includeDateRange: false,
         submitId: 'submitTransportationStationOpen',
         statusId: 'transportationStationOpenStatus',
      });

      assert.equal(dateRangeCalled, false);
      assert.equal(captured.bodyChildren.length, 3);
      assert.equal(captured.bodyChildren[0].inputId, 'transportationStationOpenTransportationStation');
      assert.equal(captured.bodyChildren[1].submitId, 'submitTransportationStationOpen');
      assert.equal(captured.bodyChildren[2].statusId, 'transportationStationOpenStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
