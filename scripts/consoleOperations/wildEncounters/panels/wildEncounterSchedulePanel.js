import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class WildEncounterSchedulePanel {
   static createWildEncounterSchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'wildEncounterSchedulePanel',
         title: Strings.panelTitles.wildEncounterSchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.wildEncounter,
               inputId: 'wildEncounterScheduleName',
               emptyOptionLabel: Strings.placeholders.wildEncounter,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'wildEncounterScheduleStartDate',
               endDateId: 'wildEncounterScheduleEndDate',
               endHelpText: Strings.help.continueUntilScheduleEnded,
            }),
            Fragments.createWildEncounterScheduleRowsField({
               rowsId: 'wildEncounterScheduleScheduleRows',
               addRowButtonId: 'wildEncounterScheduleAddScheduleRow',
            }),
            Fragments.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'wildEncounterScheduleMessage',
               placeholder: Strings.textareas.optionalScheduleMessage(
                  Strings.entityLabels.wildEncounter
               ),
            }),
            Fragments.createActions({
               submitId: 'submitWildEncounterSchedule',
            }),
            Fragments.createStatus({
               statusId: 'wildEncounterScheduleStatus',
            }),
         ],
      });
   }
}
