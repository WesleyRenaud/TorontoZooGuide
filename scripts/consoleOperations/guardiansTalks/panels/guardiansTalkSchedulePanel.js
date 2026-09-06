import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class GuardiansTalkSchedulePanel {
   static createGuardiansTalkSchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'guardiansTalkSchedulePanel',
         title: Strings.panelTitles.guardiansTalkSchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.labels.location,
               inputId: 'guardiansTalkScheduleLocation',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            Fragments.createSelectField({
               label: Strings.labels.talkName,
               inputId: 'guardiansTalkScheduleTalkName',
               emptyOptionLabel: Strings.placeholders.talk,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'guardiansTalkScheduleStartDate',
               endDateId: 'guardiansTalkScheduleEndDate',
               endHelpText: Strings.help.continueUntilScheduleEnded,
            }),
            Fragments.createWildEncounterScheduleRowsField({
               label: Strings.labels.talkTimes,
               rowsId: 'guardiansTalkScheduleScheduleRows',
               addRowButtonId: 'guardiansTalkScheduleAddScheduleRow',
               helpText: Strings.help.talkScheduleRows,
            }),
            Fragments.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'guardiansTalkScheduleMessage',
               placeholder: Strings.textareas.optionalScheduleMessage('talk'),
            }),
            Fragments.createActions({
               submitId: 'submitGuardiansTalkSchedule',
            }),
            Fragments.createStatus({
               statusId: 'guardiansTalkScheduleStatus',
            }),
         ],
      });
   }
}
