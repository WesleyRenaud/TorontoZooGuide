import { Strings } from '../../strings.js';
import { ConsoleActionsBuilder } from '../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../templates/consoleTextareaFieldBuilder.js';

export class AmenityClosureOverridePanelBuilder {
   static createPanel({
      panelId,
      title,
      entityLabel,
      emptyOptionLabel,
      idPrefix,
      entityFieldName,
      endHelpText,
      messageLabel,
      messagePlaceholder,
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
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: `${idPrefix}StartDate`,
               startHelpText: Strings.help.startImmediately,
               endDateId: `${idPrefix}EndDate`,
               endHelpText,
            }),
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
