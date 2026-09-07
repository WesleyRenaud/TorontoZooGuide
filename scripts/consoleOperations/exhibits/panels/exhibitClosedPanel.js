import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class ExhibitClosedPanel {
   static createExhibitClosedPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'exhibitClosedPanel',
         title: Strings.panelTitles.exhibitClosed,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'exhibitClosedExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'exhibitClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'exhibitClosedEndDate',
               endHelpText: Strings.help.keepClosedUntilManuallyReopened('exhibit'),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closureMessage,
               inputId: 'exhibitClosedMessage',
               placeholder: Strings.textareas.closureMessage,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitExhibitClosed',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'exhibitClosedStatus',
            }),
         ],
      });
   }
}
