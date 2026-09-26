import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityOpeningSchedulePanelBuilder } from '../../../../scripts/consoleOperations/forms/amenityOpeningSchedulePanelBuilder.js';
import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSchedulePresetFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSchedulePresetFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { ConsoleWeeklyScheduleCheckboxesBuilder } from '../../../../scripts/consoleOperations/templates/consoleWeeklyScheduleCheckboxesBuilder.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_CreatePanel_TestGiftShopConfig_ExpectShellOptions', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createSchedulePresetField: ConsoleSchedulePresetFieldBuilder.createSchedulePresetField,
      createDateRangeFields: ConsoleDateRangeFieldsBuilder.createDateRangeFields,
      createWeeklyScheduleCheckboxes: ConsoleWeeklyScheduleCheckboxesBuilder.createWeeklyScheduleCheckboxes,
      createTextareaField: ConsoleTextareaFieldBuilder.createTextareaField,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };
   const panel = { panel: true };
   const panelId = 'giftShopOpeningSchedulePanel';
   const title = Strings.panelTitles.giftShopOpeningSchedule;
   const idPrefix = 'giftShopOpeningSchedule';
   const entityFieldName = 'GiftShop';
   const scheduleMessagePlaceholder = Strings.textareas.scheduledClosedMessage('gift shop');
   const submitId = 'submitGiftShopOpeningSchedule';
   const statusId = 'giftShopOpeningScheduleStatus';
   let captured;

   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return panel;
   };
   ConsoleSelectFieldBuilder.createSelectField = (options) => ({ kind: 'createSelectField', ...options });
   ConsoleSchedulePresetFieldBuilder.createSchedulePresetField = (options) => ({
      kind: 'createSchedulePresetField',
      ...options,
   });
   ConsoleDateRangeFieldsBuilder.createDateRangeFields = (options) => ({ kind: 'createDateRangeFields', ...options });
   ConsoleWeeklyScheduleCheckboxesBuilder.createWeeklyScheduleCheckboxes = (options) => ({
      kind: 'createWeeklyScheduleCheckboxes',
      ...options,
   });
   ConsoleTextareaFieldBuilder.createTextareaField = (options) => ({ kind: 'createTextareaField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = AmenityOpeningSchedulePanelBuilder.createPanel({
         panelId,
         title,
         entityLabel: Strings.entityLabels.giftShop,
         emptyOptionLabel: Strings.placeholders.giftShop,
         idPrefix,
         entityFieldName,
         scheduleMessagePlaceholder,
         submitId,
         statusId,
      });

      const [
         entityField,
         presetField,
         dateRange,
         daysField,
         messageField,
         actions,
         status,
      ] = captured.bodyChildren;
      assert.equal(result, panel);
      assert.equal(captured.panelId, panelId);
      assert.equal(captured.title, title);
      assert.equal(entityField.inputId, `${idPrefix}${entityFieldName}`);
      assert.equal(presetField.inputId, `${idPrefix}Preset`);
      assert.equal(dateRange.startDateId, `${idPrefix}StartDate`);
      assert.equal(dateRange.startHelpText, Strings.help.startImmediately);
      assert.equal(dateRange.endDateId, `${idPrefix}EndDate`);
      assert.equal(dateRange.endHelpText, Strings.help.keepScheduleUntilChanged);
      assert.equal(daysField.dayIds.monday, `${idPrefix}Monday`);
      assert.equal(daysField.dayIds.holidays, `${idPrefix}HolidaysOnly`);
      assert.equal(messageField.inputId, `${idPrefix}Message`);
      assert.equal(messageField.placeholder, scheduleMessagePlaceholder);
      assert.equal(actions.submitId, submitId);
      assert.equal(status.statusId, statusId);
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleSchedulePresetFieldBuilder.createSchedulePresetField = originals.createSchedulePresetField;
      ConsoleDateRangeFieldsBuilder.createDateRangeFields = originals.createDateRangeFields;
      ConsoleWeeklyScheduleCheckboxesBuilder.createWeeklyScheduleCheckboxes = originals.createWeeklyScheduleCheckboxes;
      ConsoleTextareaFieldBuilder.createTextareaField = originals.createTextareaField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
