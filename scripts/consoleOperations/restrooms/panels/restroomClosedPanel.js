import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRestroomClosedPanel() {
   return createPanelShell({
      panelId: 'restroomClosedPanel',
      title: APP_STRINGS.panelTitles.restroomClosed,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.restroom,
            inputId: 'restroomClosedRestroom',
            emptyOptionLabel: APP_STRINGS.placeholders.restroom,
         }),
         createDateRangeFields({
            startDateId: 'restroomClosedStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'restroomClosedEndDate',
            endHelpText: APP_STRINGS.help.continueUntilReopened('restroom'),
         }),
         createTextareaField({
            label: APP_STRINGS.labels.closedMessage,
            inputId: 'restroomClosedMessage',
            placeholder: APP_STRINGS.textareas.closedMessage('restroom'),
         }),
         createActions({
            submitId: 'submitRestroomClosed',
         }),
         createStatus({
            statusId: 'restroomClosedStatus',
         }),
      ],
   });
}
