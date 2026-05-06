import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createZoomobileStationClosedPanel() {
   return createPanelShell({
      panelId: 'zoomobileStationClosedPanel',
      title: APP_STRINGS.panelTitles.zoomobileStationClosed,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.zoomobileStation,
            inputId: 'zoomobileStationClosedZoomobileStation',
            emptyOptionLabel: APP_STRINGS.placeholders.zoomobileStation,
         }),
         createDateRangeFields({
            startDateId: 'zoomobileStationClosedStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'zoomobileStationClosedEndDate',
            endHelpText: APP_STRINGS.help.keepClosedUntilManuallyReopened('zoomobile station'),
         }),
         createTextareaField({
            label: APP_STRINGS.labels.closureMessage,
            inputId: 'zoomobileStationClosedMessage',
            placeholder: APP_STRINGS.textareas.closureMessage,
         }),
         createActions({
            submitId: 'submitZoomobileStationClosed',
         }),
         createStatus({
            statusId: 'zoomobileStationClosedStatus',
         }),
      ],
   });
}
