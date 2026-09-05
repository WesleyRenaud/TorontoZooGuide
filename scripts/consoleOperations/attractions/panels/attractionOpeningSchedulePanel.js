import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSchedulePresetField,
   createSelectField,
   createStatus,
   createTextareaField,
   createWeeklyScheduleCheckboxes,
} from '../../templates/fragments.js';

export class AttractionOpeningSchedulePanel {
   static createAttractionOpeningSchedulePanel() {
      return createPanelShell({
         panelId: 'attractionOpeningSchedulePanel',
         title: APP_STRINGS.panelTitles.attractionOpeningSchedule,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.attraction,
               inputId: 'attractionOpeningScheduleAttraction',
               emptyOptionLabel: APP_STRINGS.placeholders.attraction,
            }),
            createSchedulePresetField({
               inputId: 'attractionOpeningSchedulePreset',
            }),
            createDateRangeFields({
               startDateId: 'attractionOpeningScheduleStartDate',
               startHelpText: APP_STRINGS.help.startImmediately,
               endDateId: 'attractionOpeningScheduleEndDate',
               endHelpText: APP_STRINGS.help.keepScheduleUntilChanged,
            }),
            createWeeklyScheduleCheckboxes({
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
            createTextareaField({
               label: APP_STRINGS.labels.scheduleMessage,
               inputId: 'attractionOpeningScheduleMessage',
               placeholder: APP_STRINGS.textareas.scheduledClosedMessage('attraction'),
            }),
            createActions({
               submitId: 'submitAttractionOpeningSchedule',
            }),
            createStatus({
               statusId: 'attractionOpeningScheduleStatus',
            }),
         ],
      });
   }
}
