import {
   createActions,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createCancelGuardiansTalkOccurrencePanel() {
   return createPanelShell({
      panelId: 'cancelGuardiansTalkOccurrencePanel',
      title: 'Cancel Meet the Guardians talk occurrence',
      bodyChildren: [
         createSelectField({
            label: 'Location',
            inputId: 'cancelGuardiansTalkOccurrenceLocation',
            emptyOptionLabel: 'Select a location',
         }),
         createSelectField({
            label: 'Talk name',
            inputId: 'cancelGuardiansTalkOccurrenceTalkName',
            emptyOptionLabel: 'Select a talk',
         }),
         createSelectField({
            label: 'Date',
            inputId: 'cancelGuardiansTalkOccurrenceDate',
            emptyOptionLabel: 'Select a date',
         }),
         createSelectField({
            label: 'Time',
            inputId: 'cancelGuardiansTalkOccurrenceTime',
            emptyOptionLabel: 'Select a time',
         }),
         createActions({
            submitId: 'submitCancelGuardiansTalkOccurrence',
         }),
         createStatus({
            statusId: 'cancelGuardiansTalkOccurrenceStatus',
         }),
      ],
   });
}
