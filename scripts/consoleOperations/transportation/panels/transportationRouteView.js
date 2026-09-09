import { TransportationRouteId } from '../../../shared/enums/transportationRouteId.js';
import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleRadioGroupFieldBuilder } from '../../templates/consoleRadioGroupFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class TransportationRouteView {
   static createTransportationRoutePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'transportationRoutePanel',
         title: Strings.panelTitles.transportationRoute,
         bodyChildren: [
            ConsoleRadioGroupFieldBuilder.createRadioGroupField({
               label: Strings.labels.route,
               name: 'transportationRoute',
               options: [
                  {
                     id: 'transportationRouteSummer',
                     value: TransportationRouteId.SUMMER,
                     label: Strings.schedule.routeLabels.summer,
                  },
                  {
                     id: 'transportationRouteWinter',
                     value: TransportationRouteId.WINTER,
                     label: Strings.schedule.routeLabels.winter,
                  },
               ],
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'transportationRouteStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'transportationRouteEndDate',
               endHelpText: Strings.help.keepRouteUntilChanged,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitTransportationRoute',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'transportationRouteStatus',
            }),
         ],
      });
   }
}
