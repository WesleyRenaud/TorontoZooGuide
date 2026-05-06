import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createExhibitClosedPanel() {
   return createPanelShell({
      panelId: 'exhibitClosedPanel',
      title: APP_STRINGS.panelTitles.exhibitClosed,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.exhibit,
            inputId: 'exhibitClosedExhibit',
            emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
         }),
         createDateRangeFields({
            startDateId: 'exhibitClosedStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'exhibitClosedEndDate',
            endHelpText: APP_STRINGS.help.keepClosedUntilManuallyReopened('exhibit'),
         }),
         createTextareaField({
            label: APP_STRINGS.labels.closureMessage,
            inputId: 'exhibitClosedMessage',
            placeholder: APP_STRINGS.textareas.closureMessage,
         }),
         createActions({
            submitId: 'submitExhibitClosed',
         }),
         createStatus({
            statusId: 'exhibitClosedStatus',
         }),
      ],
   });
}
