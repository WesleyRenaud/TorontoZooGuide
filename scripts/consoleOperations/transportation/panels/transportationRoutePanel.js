import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createRadioGroupField,
   createStatus,
} from '../../templates/fragments.js';

export class TransportationRoutePanel {
   static createTransportationRoutePanel() {
      return createPanelShell({
         panelId: 'transportationRoutePanel',
         title: APP_STRINGS.panelTitles.transportationRoute,
         bodyChildren: [
            createRadioGroupField({
               label: APP_STRINGS.labels.route,
               name: 'transportationRoute',
               options: [
                  { id: 'transportationRouteSummer', value: 'summer', label: APP_STRINGS.schedule.routeLabels.summer },
                  { id: 'transportationRouteWinter', value: 'winter', label: APP_STRINGS.schedule.routeLabels.winter },
               ],
            }),
            createDateRangeFields({
               startDateId: 'transportationRouteStartDate',
               startHelpText: APP_STRINGS.help.startImmediately,
               endDateId: 'transportationRouteEndDate',
               endHelpText: APP_STRINGS.help.keepRouteUntilChanged,
            }),
            createActions({
               submitId: 'submitTransportationRoute',
            }),
            createStatus({
               statusId: 'transportationRouteStatus',
            }),
         ],
      });
   }
}
