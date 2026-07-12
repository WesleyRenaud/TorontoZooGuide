import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createPanelShell,
   createScheduleTimesCheckboxField,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

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
         createScheduleTimesCheckboxField({
            label: APP_STRINGS.labels.talkTimes,
            inputId: 'cancelGuardiansTalkOccurrenceTimes',
            helpText: APP_STRINGS.help.cancelOccurrenceTimes,
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
