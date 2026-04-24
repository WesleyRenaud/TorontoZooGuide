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
      title: 'Set attraction as closed',
      bodyChildren: [
         createSelectField({
            label: 'Attraction',
            inputId: 'attractionClosedAttraction',
            emptyOptionLabel: 'Select an attraction',
         }),
         createDateRangeFields({
            startDateId: 'attractionClosedStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'attractionClosedEndDate',
            endHelpText: 'Leave blank to keep the attraction closed until it is manually reopened.',
         }),
         createTextareaField({
            label: 'Closure message',
            inputId: 'attractionClosedMessage',
            placeholder: 'Enter the closure message shown to guests',
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
