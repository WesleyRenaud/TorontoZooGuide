import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createAddGuardiansTalkOccurrencePanel() {
   return createPanelShell({
      panelId: 'addGuardiansTalkOccurrencePanel',
      title: APP_STRINGS.panelTitles.addGuardiansTalkOccurrence,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.labels.location,
            inputId: 'addGuardiansTalkOccurrenceLocation',
            emptyOptionLabel: APP_STRINGS.placeholders.location,
         }),
         createSelectField({
            label: APP_STRINGS.labels.talkName,
            inputId: 'addGuardiansTalkOccurrenceTalkName',
            emptyOptionLabel: APP_STRINGS.placeholders.talk,
         }),
         createDateField({
            label: APP_STRINGS.labels.date,
            inputId: 'addGuardiansTalkOccurrenceDate',
            placeholder: APP_STRINGS.placeholders.startDate,
         }),
         createDateField({
            label: APP_STRINGS.labels.talkTime,
            inputId: 'addGuardiansTalkOccurrenceTime',
            placeholder: APP_STRINGS.placeholders.time,
         }),
         createActions({
            submitId: 'submitAddGuardiansTalkOccurrence',
         }),
         createStatus({
            statusId: 'addGuardiansTalkOccurrenceStatus',
         }),
      ],
   });
}
