import { Strings } from '../../strings.js';
import { ConsoleActionsBuilder } from '../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../templates/consolePanelShellBuilder.js';
import { ConsoleStatusBuilder } from '../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../templates/consoleTextareaFieldBuilder.js';

export class GlobalAmenityStatusPanelBuilder {
   static createPanel({
      panelId,
      title,
      idPrefix,
      endHelpText,
      includeMessage = false,
      messageLabel,
      messagePlaceholder,
      submitId,
      statusId,
   } = {}) {
      const bodyChildren = [
         ConsoleDateRangeFieldsBuilder.createDateRangeFields({
            startDateId: `${idPrefix}StartDate`,
            startHelpText: Strings.help.startImmediately,
            endDateId: `${idPrefix}EndDate`,
            endHelpText,
         }),
      ];

      if (includeMessage) {
         bodyChildren.push(
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: messageLabel,
               inputId: `${idPrefix}Message`,
               placeholder: messagePlaceholder,
            }),
         );
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
