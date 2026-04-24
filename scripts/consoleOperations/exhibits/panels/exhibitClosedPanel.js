import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createExhibitClosedPanel() {
   return createPanelShell({
      panelId: 'exhibitClosedPanel',
      title: 'Set exhibit as closed',
      bodyChildren: [
         createSelectField({
            label: 'Exhibit',
            inputId: 'exhibitClosedExhibit',
            emptyOptionLabel: 'Select an exhibit',
         }),
         createDateRangeFields({
            startDateId: 'exhibitClosedStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'exhibitClosedEndDate',
            endHelpText: 'Leave blank to keep the exhibit closed until it is manually reopened.',
         }),
         createTextareaField({
            label: 'Closure message',
            inputId: 'exhibitClosedMessage',
            placeholder: 'Enter the closure message shown to guests',
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
