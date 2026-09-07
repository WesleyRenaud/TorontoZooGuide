import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../templates/consoleAutocompleteFieldBuilder.js';
import { ConsoleDateFieldBuilder } from '../../templates/consoleDateFieldBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class VisibilitySchedulePanel {
   static createVisibilitySchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'visibilitySchedulePanel',
         title: Strings.panelTitles.visibilitySchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'visibilityScheduleExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleAutocompleteFieldBuilder.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'visibilityScheduleSpecies',
               resultsId: 'visibilityScheduleSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'visibilityScheduleStartDate',
               startLabel: Strings.labels.scheduleStartDate,
               startHelpText: Strings.help.startImmediately,
               endDateId: 'visibilityScheduleEndDate',
               endLabel: Strings.labels.scheduleEndDate,
               endHelpText: Strings.help.keepVisibilityScheduleUntilChanged,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.dailyViewingStartTime,
               inputId: 'visibilityScheduleDailyStartTime',
               placeholder: Strings.placeholders.dailyStartTime,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.dailyViewingEndTime,
               inputId: 'visibilityScheduleDailyEndTime',
               placeholder: Strings.placeholders.dailyEndTime,
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.message,
               inputId: 'visibilityScheduleMessage',
               placeholder: Strings.textareas.viewingMessage,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitVisibilitySchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'visibilityScheduleStatus',
            }),
         ],
      });
   }
}
