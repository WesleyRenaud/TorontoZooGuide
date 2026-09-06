import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class VisibilitySchedulePanel {
   static createVisibilitySchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'visibilitySchedulePanel',
         title: Strings.panelTitles.visibilitySchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'visibilityScheduleExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            Fragments.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'visibilityScheduleSpecies',
               resultsId: 'visibilityScheduleSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'visibilityScheduleStartDate',
               startLabel: Strings.labels.scheduleStartDate,
               startHelpText: Strings.help.startImmediately,
               endDateId: 'visibilityScheduleEndDate',
               endLabel: Strings.labels.scheduleEndDate,
               endHelpText: Strings.help.keepVisibilityScheduleUntilChanged,
            }),
            Fragments.createDateField({
               label: Strings.labels.dailyViewingStartTime,
               inputId: 'visibilityScheduleDailyStartTime',
               placeholder: Strings.placeholders.dailyStartTime,
            }),
            Fragments.createDateField({
               label: Strings.labels.dailyViewingEndTime,
               inputId: 'visibilityScheduleDailyEndTime',
               placeholder: Strings.placeholders.dailyEndTime,
            }),
            Fragments.createTextareaField({
               label: Strings.labels.message,
               inputId: 'visibilityScheduleMessage',
               placeholder: Strings.textareas.viewingMessage,
            }),
            Fragments.createActions({
               submitId: 'submitVisibilitySchedule',
            }),
            Fragments.createStatus({
               statusId: 'visibilityScheduleStatus',
            }),
         ],
      });
   }
}
