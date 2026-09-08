import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';
import { ConsoleWildEncounterScheduleRowsFieldBuilder } from '../../templates/consoleWildEncounterScheduleRowsFieldBuilder.js';

export class WildEncounterScheduleView {
   static createWildEncounterSchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'wildEncounterSchedulePanel',
         title: Strings.panelTitles.wildEncounterSchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.wildEncounter,
               inputId: 'wildEncounterScheduleName',
               emptyOptionLabel: Strings.placeholders.wildEncounter,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'wildEncounterScheduleStartDate',
               endDateId: 'wildEncounterScheduleEndDate',
               endHelpText: Strings.help.continueUntilScheduleEnded,
            }),
            ConsoleWildEncounterScheduleRowsFieldBuilder.createWildEncounterScheduleRowsField({
               rowsId: 'wildEncounterScheduleScheduleRows',
               addRowButtonId: 'wildEncounterScheduleAddScheduleRow',
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'wildEncounterScheduleMessage',
               placeholder: Strings.textareas.optionalScheduleMessage(
                  Strings.entityLabels.wildEncounter
               ),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitWildEncounterSchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'wildEncounterScheduleStatus',
            }),
         ],
      });
   }
}
