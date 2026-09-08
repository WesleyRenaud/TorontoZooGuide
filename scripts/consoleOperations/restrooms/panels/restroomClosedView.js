import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class RestroomClosedView {
   static createRestroomClosedPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'restroomClosedPanel',
         title: Strings.panelTitles.restroomClosed,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.restroom,
               inputId: 'restroomClosedRestroom',
               emptyOptionLabel: Strings.placeholders.restroom,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'restroomClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restroomClosedEndDate',
               endHelpText: Strings.help.continueUntilReopened('restroom'),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'restroomClosedMessage',
               placeholder: Strings.textareas.closedMessage('restroom'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitRestroomClosed',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'restroomClosedStatus',
            }),
         ],
      });
   }
}
