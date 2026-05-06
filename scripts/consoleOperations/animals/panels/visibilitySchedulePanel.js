import {
   createActions,
   createAutocompleteField,
   createDateRangeFields,
   createDateField,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createVisibilitySchedulePanel() {
   return createPanelShell({
      panelId: 'visibilitySchedulePanel',
      title: APP_STRINGS.panelTitles.visibilitySchedule,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.exhibit,
            inputId: 'visibilityScheduleExhibit',
            emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
         }),
         createAutocompleteField({
            label: APP_STRINGS.labels.species,
            inputId: 'visibilityScheduleSpecies',
            resultsId: 'visibilityScheduleSpeciesResults',
            placeholder: APP_STRINGS.placeholders.speciesSearch,
         }),
         createDateRangeFields({
            startDateId: 'visibilityScheduleStartDate',
            startLabel: APP_STRINGS.labels.scheduleStartDate,
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'visibilityScheduleEndDate',
            endLabel: APP_STRINGS.labels.scheduleEndDate,
            endHelpText: APP_STRINGS.help.keepVisibilityScheduleUntilChanged,
         }),
         createDateField({
            label: APP_STRINGS.labels.dailyViewingStartTime,
            inputId: 'visibilityScheduleDailyStartTime',
            placeholder: APP_STRINGS.placeholders.dailyStartTime,
         }),
         createDateField({
            label: APP_STRINGS.labels.dailyViewingEndTime,
            inputId: 'visibilityScheduleDailyEndTime',
            placeholder: APP_STRINGS.placeholders.dailyEndTime,
         }),
         createTextareaField({
            label: APP_STRINGS.labels.message,
            inputId: 'visibilityScheduleMessage',
            placeholder: APP_STRINGS.textareas.viewingMessage,
         }),
         createActions({
            submitId: 'submitVisibilitySchedule',
         }),
         createStatus({
            statusId: 'visibilityScheduleStatus',
         }),
      ],
   });
}
