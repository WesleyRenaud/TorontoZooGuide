import { Strings } from '../../strings.js';
import { ConsoleActionsBuilder } from '../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../templates/consolePanelShellBuilder.js';
import { ConsoleSchedulePresetFieldBuilder } from '../templates/consoleSchedulePresetFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../templates/consoleTextareaFieldBuilder.js';
import { ConsoleWeeklyScheduleCheckboxesBuilder } from '../templates/consoleWeeklyScheduleCheckboxesBuilder.js';

export class AmenityOpeningSchedulePanelBuilder {
   static createPanel({
      panelId,
      title,
      entityLabel,
      emptyOptionLabel,
      idPrefix,
      entityFieldName,
      scheduleMessagePlaceholder,
      submitId,
      statusId,
   } = {}) {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId,
         title,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: entityLabel,
               inputId: `${idPrefix}${entityFieldName}`,
               emptyOptionLabel,
            }),
            ConsoleSchedulePresetFieldBuilder.createSchedulePresetField({
               inputId: `${idPrefix}Preset`,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: `${idPrefix}StartDate`,
               startHelpText: Strings.help.startImmediately,
               endDateId: `${idPrefix}EndDate`,
               endHelpText: Strings.help.keepScheduleUntilChanged,
            }),
            ConsoleWeeklyScheduleCheckboxesBuilder.createWeeklyScheduleCheckboxes({
               dayIds: AmenityOpeningSchedulePanelBuilder._createDayIds(idPrefix),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: `${idPrefix}Message`,
               placeholder: scheduleMessagePlaceholder,
            }),
            ConsoleActionsBuilder.createActions({
               submitId,
            }),
            ConsoleStatusBuilder.createStatus({
               statusId,
            }),
         ],
      });
   }

   static _createDayIds(idPrefix) {
      return {
         monday: `${idPrefix}Monday`,
         tuesday: `${idPrefix}Tuesday`,
         wednesday: `${idPrefix}Wednesday`,
         thursday: `${idPrefix}Thursday`,
         friday: `${idPrefix}Friday`,
         saturday: `${idPrefix}Saturday`,
         sunday: `${idPrefix}Sunday`,
         holidays: `${idPrefix}HolidaysOnly`,
      };
   }
}
