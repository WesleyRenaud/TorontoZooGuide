import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class AttractionClosedPanel {
   static createAttractionClosedPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'attractionClosedPanel',
         title: Strings.panelTitles.attractionClosed,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.attraction,
               inputId: 'attractionClosedAttraction',
               emptyOptionLabel: Strings.placeholders.attraction,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'attractionClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'attractionClosedEndDate',
               endHelpText: Strings.help.keepClosedUntilManuallyReopened('attraction'),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closureMessage,
               inputId: 'attractionClosedMessage',
               placeholder: Strings.textareas.closureMessage,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitAttractionClosed',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'attractionClosedStatus',
            }),
         ],
      });
   }
}
