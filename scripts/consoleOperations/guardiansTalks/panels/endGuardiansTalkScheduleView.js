import { EndRecurringSchedulePanelBuilder } from '../../forms/endRecurringSchedulePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class EndGuardiansTalkScheduleView {
   static createEndGuardiansTalkSchedulePanel() {
      return EndRecurringSchedulePanelBuilder.createPanel({
         panelId: 'endGuardiansTalkSchedulePanel',
         title: Strings.panelTitles.endGuardiansTalkSchedule,
         locationLabel: Strings.labels.location,
         locationInputId: 'endGuardiansTalkScheduleLocation',
         locationEmptyOptionLabel: Strings.placeholders.location,
         talkLabel: Strings.labels.talkName,
         talkInputId: 'endGuardiansTalkScheduleTalkName',
         talkEmptyOptionLabel: Strings.placeholders.talk,
         timesLabel: Strings.labels.talkTimes,
         timesInputId: 'endGuardiansTalkScheduleTimes',
         timesHelpText: Strings.help.endScheduleTimes,
         endDateLabel: Strings.labels.endDate,
         endDateInputId: 'endGuardiansTalkScheduleEndDate',
         endDatePlaceholder: Strings.placeholders.scheduleEndDate,
         endDateHelpText: Strings.help.endScheduleToday,
         submitId: 'submitEndGuardiansTalkSchedule',
         statusId: 'endGuardiansTalkScheduleStatus',
      });
   }
}
