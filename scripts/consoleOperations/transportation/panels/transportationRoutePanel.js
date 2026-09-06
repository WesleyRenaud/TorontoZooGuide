import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class TransportationRoutePanel {
   static createTransportationRoutePanel() {
      return Fragments.createPanelShell({
         panelId: 'transportationRoutePanel',
         title: Strings.panelTitles.transportationRoute,
         bodyChildren: [
            Fragments.createRadioGroupField({
               label: Strings.labels.route,
               name: 'transportationRoute',
               options: [
                  { id: 'transportationRouteSummer', value: 'summer', label: Strings.schedule.routeLabels.summer },
                  { id: 'transportationRouteWinter', value: 'winter', label: Strings.schedule.routeLabels.winter },
               ],
            }),
            Fragments.createDateRangeFields({
               startDateId: 'transportationRouteStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'transportationRouteEndDate',
               endHelpText: Strings.help.keepRouteUntilChanged,
            }),
            Fragments.createActions({
               submitId: 'submitTransportationRoute',
            }),
            Fragments.createStatus({
               statusId: 'transportationRouteStatus',
            }),
         ],
      });
   }
}
