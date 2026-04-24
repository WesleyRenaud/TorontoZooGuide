import {
   createActions,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createCancelWildEncounterOccurrencePanel() {
   return createPanelShell({
      panelId: 'cancelWildEncounterOccurrencePanel',
      title: 'Cancel Wild Encounter occurrence',
      bodyChildren: [
         createSelectField({
            label: 'Wild Encounter',
            inputId: 'cancelWildEncounterOccurrenceName',
            emptyOptionLabel: 'Select a Wild Encounter',
         }),
         createSelectField({
            label: 'Date',
            inputId: 'cancelWildEncounterOccurrenceDate',
            emptyOptionLabel: 'Select a date',
         }),
         createSelectField({
            label: 'Time',
            inputId: 'cancelWildEncounterOccurrenceTime',
            emptyOptionLabel: 'Select a time',
         }),
         createActions({
            submitId: 'submitCancelWildEncounterOccurrence',
         }),
         createStatus({
            statusId: 'cancelWildEncounterOccurrenceStatus',
         }),
      ],
   });
}
