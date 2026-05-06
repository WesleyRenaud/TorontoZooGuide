import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createRadioGroupField,
   createStatus,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createZoomobileRoutePanel() {
   return createPanelShell({
      panelId: 'zoomobileRoutePanel',
      title: APP_STRINGS.panelTitles.zoomobileRoute,
      bodyChildren: [
         createRadioGroupField({
            label: APP_STRINGS.labels.route,
            name: 'zoomobileRoute',
            options: [
               { id: 'zoomobileRouteSummer', value: 'summer', label: APP_STRINGS.schedule.routeLabels.summer },
               { id: 'zoomobileRouteWinter', value: 'winter', label: APP_STRINGS.schedule.routeLabels.winter },
            ],
         }),
         createDateRangeFields({
            startDateId: 'zoomobileRouteStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'zoomobileRouteEndDate',
            endHelpText: APP_STRINGS.help.keepRouteUntilChanged,
         }),
         createActions({
            submitId: 'submitZoomobileRoute',
         }),
         createStatus({
            statusId: 'zoomobileRouteStatus',
         }),
      ],
   });
}
