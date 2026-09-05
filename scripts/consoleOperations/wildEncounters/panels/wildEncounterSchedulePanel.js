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

export class WildEncounterSchedulePanel {
   static createWildEncounterSchedulePanel() {
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
            createWildEncounterScheduleRowsField({
               rowsId: 'wildEncounterScheduleScheduleRows',
               addRowButtonId: 'wildEncounterScheduleAddScheduleRow',
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
}
