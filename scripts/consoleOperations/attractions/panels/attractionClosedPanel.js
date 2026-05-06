import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createAttractionClosedPanel() {
   return createPanelShell({
      panelId: 'attractionClosedPanel',
      title: APP_STRINGS.panelTitles.attractionClosed,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.attraction,
            inputId: 'attractionClosedAttraction',
            emptyOptionLabel: APP_STRINGS.placeholders.attraction,
         }),
         createDateRangeFields({
            startDateId: 'attractionClosedStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'attractionClosedEndDate',
            endHelpText: APP_STRINGS.help.keepClosedUntilManuallyReopened('attraction'),
         }),
         createTextareaField({
            label: APP_STRINGS.labels.closureMessage,
            inputId: 'attractionClosedMessage',
            placeholder: APP_STRINGS.textareas.closureMessage,
         }),
         createActions({
            submitId: 'submitAttractionClosed',
         }),
         createStatus({
            statusId: 'attractionClosedStatus',
         }),
      ],
   });
}
