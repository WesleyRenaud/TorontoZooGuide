import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class CancelWildEncounterOccurrencePanel {
   static createCancelWildEncounterOccurrencePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'cancelWildEncounterOccurrencePanel',
         title: Strings.panelTitles.cancelWildEncounterOccurrence,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.wildEncounter,
               inputId: 'cancelWildEncounterOccurrenceName',
               emptyOptionLabel: Strings.placeholders.wildEncounter,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.date,
               inputId: 'cancelWildEncounterOccurrenceDate',
               emptyOptionLabel: Strings.placeholders.date,
            }),
            ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
               label: Strings.labels.encounterTimes,
               inputId: 'cancelWildEncounterOccurrenceTimes',
               helpText: Strings.help.cancelOccurrenceTimes,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitCancelWildEncounterOccurrence',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'cancelWildEncounterOccurrenceStatus',
            }),
         ],
      });
   }
}
