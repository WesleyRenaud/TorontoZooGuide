import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createCancelWildEncounterOccurrencePanel() {
   return createPanelShell({
      panelId: 'cancelWildEncounterOccurrencePanel',
      title: APP_STRINGS.panelTitles.cancelWildEncounterOccurrence,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.wildEncounter,
            inputId: 'cancelWildEncounterOccurrenceName',
            emptyOptionLabel: APP_STRINGS.placeholders.wildEncounter,
         }),
         createSelectField({
            label: APP_STRINGS.labels.date,
            inputId: 'cancelWildEncounterOccurrenceDate',
            emptyOptionLabel: APP_STRINGS.placeholders.date,
         }),
         createSelectField({
            label: APP_STRINGS.labels.time,
            inputId: 'cancelWildEncounterOccurrenceTime',
            emptyOptionLabel: APP_STRINGS.placeholders.time,
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
