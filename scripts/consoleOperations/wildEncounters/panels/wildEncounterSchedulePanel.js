import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createCheckboxGridField,
   createDateRangeFields,
   createMultiTimeField,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createWildEncounterSchedulePanel() {
   return createPanelShell({
      panelId: 'wildEncounterSchedulePanel',
      title: APP_STRINGS.panelTitles.wildEncounterSchedule,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.wildEncounter,
            inputId: 'wildEncounterScheduleName',
            emptyOptionLabel: APP_STRINGS.placeholders.wildEncounter,
         }),
         createDateRangeFields({
            startDateId: 'wildEncounterScheduleStartDate',
            endDateId: 'wildEncounterScheduleEndDate',
            endHelpText: APP_STRINGS.help.continueUntilScheduleEnded,
         }),
         createCheckboxGridField({
            label: APP_STRINGS.labels.occursOnTheseDays,
            options: [
               { id: 'wildEncounterScheduleMonday', label: APP_STRINGS.schedule.dayLabels.monday },
               { id: 'wildEncounterScheduleTuesday', label: APP_STRINGS.schedule.dayLabels.tuesday },
               { id: 'wildEncounterScheduleWednesday', label: APP_STRINGS.schedule.dayLabels.wednesday },
               { id: 'wildEncounterScheduleThursday', label: APP_STRINGS.schedule.dayLabels.thursday },
               { id: 'wildEncounterScheduleFriday', label: APP_STRINGS.schedule.dayLabels.friday },
               { id: 'wildEncounterScheduleSaturday', label: APP_STRINGS.schedule.dayLabels.saturday },
               { id: 'wildEncounterScheduleSunday', label: APP_STRINGS.schedule.dayLabels.sunday },
            ],
         }),
         createMultiTimeField({
            label: APP_STRINGS.labels.encounterTimes,
            listId: 'wildEncounterScheduleTimes',
            inputId: 'wildEncounterScheduleTime',
            placeholder: APP_STRINGS.placeholders.scheduledTime('an encounter'),
            helpText: APP_STRINGS.help.encounterTimesAddOneAtATime,
         }),
         createTextareaField({
            label: APP_STRINGS.labels.scheduleMessage,
            inputId: 'wildEncounterScheduleMessage',
            placeholder: APP_STRINGS.textareas.optionalScheduleMessage(
               APP_STRINGS.entityLabels.wildEncounter
            ),
         }),
         createActions({
            submitId: 'submitWildEncounterSchedule',
         }),
         createStatus({
            statusId: 'wildEncounterScheduleStatus',
         }),
      ],
   });
}
