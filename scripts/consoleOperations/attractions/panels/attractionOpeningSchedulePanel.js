import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class AttractionOpeningSchedulePanel {
   static createAttractionOpeningSchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'attractionOpeningSchedulePanel',
         title: Strings.panelTitles.attractionOpeningSchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.attraction,
               inputId: 'attractionOpeningScheduleAttraction',
               emptyOptionLabel: Strings.placeholders.attraction,
            }),
            Fragments.createSchedulePresetField({
               inputId: 'attractionOpeningSchedulePreset',
            }),
            Fragments.createDateRangeFields({
               startDateId: 'attractionOpeningScheduleStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'attractionOpeningScheduleEndDate',
               endHelpText: Strings.help.keepScheduleUntilChanged,
            }),
            Fragments.createWeeklyScheduleCheckboxes({
               dayIds: {
                  monday: 'attractionOpeningScheduleMonday',
                  tuesday: 'attractionOpeningScheduleTuesday',
                  wednesday: 'attractionOpeningScheduleWednesday',
                  thursday: 'attractionOpeningScheduleThursday',
                  friday: 'attractionOpeningScheduleFriday',
                  saturday: 'attractionOpeningScheduleSaturday',
                  sunday: 'attractionOpeningScheduleSunday',
                  holidays: 'attractionOpeningScheduleHolidaysOnly',
               },
            }),
            Fragments.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'attractionOpeningScheduleMessage',
               placeholder: Strings.textareas.scheduledClosedMessage('attraction'),
            }),
            Fragments.createActions({
               submitId: 'submitAttractionOpeningSchedule',
            }),
            Fragments.createStatus({
               statusId: 'attractionOpeningScheduleStatus',
            }),
         ],
      });
   }
}
