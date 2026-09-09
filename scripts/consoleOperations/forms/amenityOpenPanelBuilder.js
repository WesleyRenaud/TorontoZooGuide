import { ConsoleActionsBuilder } from '../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../templates/consoleStatusBuilder.js';

export class AmenityOpenPanelBuilder {
   static createPanel({
      panelId,
      title,
      entityLabel,
      emptyOptionLabel,
      idPrefix,
      entityFieldName,
      includeDateRange = true,
      startHelpText,
      endHelpText,
      submitId,
      statusId,
   } = {}) {
      const bodyChildren = [
         ConsoleSelectFieldBuilder.createSelectField({
            label: entityLabel,
            inputId: `${idPrefix}${entityFieldName}`,
            emptyOptionLabel,
         }),
      ];

      if (includeDateRange) {
         const dateRangeOptions = {
            startDateId: `${idPrefix}StartDate`,
            endDateId: `${idPrefix}EndDate`,
            endHelpText,
         };

         if (startHelpText !== undefined) {
            dateRangeOptions.startHelpText = startHelpText;
         }

         bodyChildren.push(ConsoleDateRangeFieldsBuilder.createDateRangeFields(dateRangeOptions));
      }

      bodyChildren.push(
         ConsoleActionsBuilder.createActions({
            submitId,
         }),
         ConsoleStatusBuilder.createStatus({
            statusId,
         }),
      );

      return ConsolePanelShellBuilder.createPanelShell({
         panelId,
         title,
         bodyChildren,
      });
   }
}
