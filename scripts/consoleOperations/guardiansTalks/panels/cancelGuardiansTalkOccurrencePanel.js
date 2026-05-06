import {
   createActions,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createCancelGuardiansTalkOccurrencePanel() {
   return createPanelShell({
      panelId: 'cancelGuardiansTalkOccurrencePanel',
      title: APP_STRINGS.panelTitles.cancelGuardiansTalkOccurrence,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.labels.location,
            inputId: 'cancelGuardiansTalkOccurrenceLocation',
            emptyOptionLabel: APP_STRINGS.placeholders.location,
         }),
         createSelectField({
            label: APP_STRINGS.labels.talkName,
            inputId: 'cancelGuardiansTalkOccurrenceTalkName',
            emptyOptionLabel: APP_STRINGS.placeholders.talk,
         }),
         createSelectField({
            label: APP_STRINGS.labels.date,
            inputId: 'cancelGuardiansTalkOccurrenceDate',
            emptyOptionLabel: APP_STRINGS.placeholders.date,
         }),
         createSelectField({
            label: APP_STRINGS.labels.time,
            inputId: 'cancelGuardiansTalkOccurrenceTime',
            emptyOptionLabel: APP_STRINGS.placeholders.time,
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
