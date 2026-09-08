import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class TransportationStationClosedView {
   static createTransportationStationClosedPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'transportationStationClosedPanel',
         title: Strings.panelTitles.transportationStationClosed,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.transportationStation,
               inputId: 'transportationStationClosedTransportationStation',
               emptyOptionLabel: Strings.placeholders.transportationStation,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'transportationStationClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'transportationStationClosedEndDate',
               endHelpText: Strings.help.keepClosedUntilManuallyReopened('transportation station'),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closureMessage,
               inputId: 'transportationStationClosedMessage',
               placeholder: Strings.textareas.closureMessage,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitTransportationStationClosed',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'transportationStationClosedStatus',
            }),
         ],
      });
   }
}
