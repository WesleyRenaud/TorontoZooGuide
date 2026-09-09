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

   let captured;
   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return { panel: true };
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
         panelId: 'giftShopOpeningSchedulePanel',
         title: Strings.panelTitles.giftShopOpeningSchedule,
         entityLabel: Strings.entityLabels.giftShop,
         emptyOptionLabel: Strings.placeholders.giftShop,
         idPrefix: 'giftShopOpeningSchedule',
         entityFieldName: 'GiftShop',
         scheduleMessagePlaceholder: Strings.textareas.scheduledClosedMessage('gift shop'),
         submitId: 'submitGiftShopOpeningSchedule',
         statusId: 'giftShopOpeningScheduleStatus',
      });

      assert.deepEqual(result, { panel: true });
      assert.equal(captured.panelId, 'giftShopOpeningSchedulePanel');
      assert.equal(captured.title, Strings.panelTitles.giftShopOpeningSchedule);
      assert.equal(captured.bodyChildren.length, 7);
      assert.equal(captured.bodyChildren[0].inputId, 'giftShopOpeningScheduleGiftShop');
      assert.equal(captured.bodyChildren[1].inputId, 'giftShopOpeningSchedulePreset');
      assert.equal(captured.bodyChildren[2].startDateId, 'giftShopOpeningScheduleStartDate');
      assert.equal(captured.bodyChildren[2].startHelpText, Strings.help.startImmediately);
      assert.equal(captured.bodyChildren[2].endDateId, 'giftShopOpeningScheduleEndDate');
      assert.equal(captured.bodyChildren[2].endHelpText, Strings.help.keepScheduleUntilChanged);
      assert.equal(captured.bodyChildren[3].dayIds.monday, 'giftShopOpeningScheduleMonday');
      assert.equal(captured.bodyChildren[3].dayIds.holidays, 'giftShopOpeningScheduleHolidaysOnly');
      assert.equal(captured.bodyChildren[4].inputId, 'giftShopOpeningScheduleMessage');
      assert.equal(captured.bodyChildren[4].placeholder, Strings.textareas.scheduledClosedMessage('gift shop'));
      assert.equal(captured.bodyChildren[5].submitId, 'submitGiftShopOpeningSchedule');
      assert.equal(captured.bodyChildren[6].statusId, 'giftShopOpeningScheduleStatus');
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
