import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateField,
   createPanelShell,
   createScheduleTimesCheckboxField,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createEndGuardiansTalkSchedulePanel() {
   return createPanelShell({
      panelId: 'endGuardiansTalkSchedulePanel',
      title: APP_STRINGS.panelTitles.endGuardiansTalkSchedule,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.labels.location,
            inputId: 'endGuardiansTalkScheduleLocation',
            emptyOptionLabel: APP_STRINGS.placeholders.location,
         }),
         createSelectField({
            label: APP_STRINGS.labels.talkName,
            inputId: 'endGuardiansTalkScheduleTalkName',
            emptyOptionLabel: APP_STRINGS.placeholders.talk,
         }),
         createScheduleTimesCheckboxField({
            label: APP_STRINGS.labels.talkTimes,
            inputId: 'endGuardiansTalkScheduleTimes',
            helpText: APP_STRINGS.help.endScheduleTimes,
         }),
         createDateField({
            label: APP_STRINGS.labels.endDate,
            inputId: 'endGuardiansTalkScheduleEndDate',
            placeholder: APP_STRINGS.placeholders.scheduleEndDate,
            helpText: APP_STRINGS.help.endScheduleToday,
         }),
         createActions({
            submitId: 'submitEndGuardiansTalkSchedule',
         }),
         createStatus({
            statusId: 'endGuardiansTalkScheduleStatus',
         }),
      ],
   });
}
