import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class EndGuardiansTalkSchedulePanel {
   static createEndGuardiansTalkSchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'endGuardiansTalkSchedulePanel',
         title: Strings.panelTitles.endGuardiansTalkSchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.labels.location,
               inputId: 'endGuardiansTalkScheduleLocation',
               emptyOptionLabel: Strings.placeholders.location,
            }),
            Fragments.createSelectField({
               label: Strings.labels.talkName,
               inputId: 'endGuardiansTalkScheduleTalkName',
               emptyOptionLabel: Strings.placeholders.talk,
            }),
            Fragments.createScheduleTimesCheckboxField({
               label: Strings.labels.talkTimes,
               inputId: 'endGuardiansTalkScheduleTimes',
               helpText: Strings.help.endScheduleTimes,
            }),
            Fragments.createDateField({
               label: Strings.labels.endDate,
               inputId: 'endGuardiansTalkScheduleEndDate',
               placeholder: Strings.placeholders.scheduleEndDate,
               helpText: Strings.help.endScheduleToday,
            }),
            Fragments.createActions({
               submitId: 'submitEndGuardiansTalkSchedule',
            }),
            Fragments.createStatus({
               statusId: 'endGuardiansTalkScheduleStatus',
            }),
         ],
      });
   }
}
