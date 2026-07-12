import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
   createWildEncounterScheduleRowsField,
} from '../../templates/fragments.js';

export function createGuardiansTalkSchedulePanel() {
   return createPanelShell({
      panelId: 'guardiansTalkSchedulePanel',
      title: APP_STRINGS.panelTitles.guardiansTalkSchedule,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.labels.location,
            inputId: 'guardiansTalkScheduleLocation',
            emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
         }),
         createSelectField({
            label: APP_STRINGS.labels.talkName,
            inputId: 'guardiansTalkScheduleTalkName',
            emptyOptionLabel: APP_STRINGS.placeholders.talk,
         }),
         createDateRangeFields({
            startDateId: 'guardiansTalkScheduleStartDate',
            endDateId: 'guardiansTalkScheduleEndDate',
            endHelpText: APP_STRINGS.help.continueUntilScheduleEnded,
         }),
         createWildEncounterScheduleRowsField({
            label: APP_STRINGS.labels.talkTimes,
            rowsId: 'guardiansTalkScheduleScheduleRows',
            addRowButtonId: 'guardiansTalkScheduleAddScheduleRow',
            helpText: APP_STRINGS.help.talkScheduleRows,
         }),
         createTextareaField({
            label: APP_STRINGS.labels.scheduleMessage,
            inputId: 'guardiansTalkScheduleMessage',
            placeholder: APP_STRINGS.textareas.optionalScheduleMessage('talk'),
         }),
         createActions({
            submitId: 'submitGuardiansTalkSchedule',
         }),
         createStatus({
            statusId: 'guardiansTalkScheduleStatus',
         }),
      ],
   });
}
