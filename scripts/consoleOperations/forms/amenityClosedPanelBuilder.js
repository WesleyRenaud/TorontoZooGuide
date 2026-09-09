import { ConsoleActionsBuilder } from '../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../templates/consoleTextareaFieldBuilder.js';

export class AmenityClosedPanelBuilder {
   static createPanel({
      panelId,
      title,
      entityLabel,
      emptyOptionLabel,
      idPrefix,
      entityFieldName,
      startHelpText,
      endHelpText,
      messageLabel,
      messagePlaceholder,
      submitId,
      statusId,
   } = {}) {
      const dateRangeOptions = {
         startDateId: `${idPrefix}StartDate`,
         endDateId: `${idPrefix}EndDate`,
         endHelpText,
      };

      if (startHelpText !== undefined) {
         dateRangeOptions.startHelpText = startHelpText;
      }

      return ConsolePanelShellBuilder.createPanelShell({
         panelId,
         title,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: entityLabel,
               inputId: `${idPrefix}${entityFieldName}`,
               emptyOptionLabel,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields(dateRangeOptions),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: messageLabel,
               inputId: `${idPrefix}Message`,
               placeholder: messagePlaceholder,
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
}
