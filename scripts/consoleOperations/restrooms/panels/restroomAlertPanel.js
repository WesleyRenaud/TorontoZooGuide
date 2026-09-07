import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class RestroomAlertPanel {
   static createRestroomAlertPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'restroomAlertPanel',
         title: Strings.panelTitles.restroomAlert,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.restroom,
               inputId: 'restroomAlertRestroom',
               emptyOptionLabel: Strings.placeholders.restroom,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'restroomAlertStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restroomAlertEndDate',
               endHelpText: Strings.help.keepAlertActiveUntilRemoved,
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.alertMessage,
               inputId: 'restroomAlertMessage',
               placeholder: Strings.placeholders.restroomAlertExample,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitRestroomAlert',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'restroomAlertStatus',
            }),
         ],
      });
   }
}
