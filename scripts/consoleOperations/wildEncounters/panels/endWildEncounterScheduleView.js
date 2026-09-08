import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../templates/consoleDateFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class EndWildEncounterScheduleView {
   static createEndWildEncounterSchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'endWildEncounterSchedulePanel',
         title: Strings.panelTitles.endWildEncounterSchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.wildEncounter,
               inputId: 'endWildEncounterScheduleName',
               emptyOptionLabel: Strings.placeholders.wildEncounter,
            }),
            ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
               label: Strings.labels.encounterTimes,
               inputId: 'endWildEncounterScheduleTimes',
               helpText: Strings.help.endScheduleTimes,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.endDate,
               inputId: 'endWildEncounterScheduleDate',
               placeholder: Strings.placeholders.scheduleEndDate,
               helpText: Strings.help.endScheduleToday,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitEndWildEncounterSchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'endWildEncounterScheduleStatus',
            }),
         ],
      });
   }
}
