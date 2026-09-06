import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class RestaurantOpeningSchedulePanel {
   static createRestaurantOpeningSchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'restaurantOpeningSchedulePanel',
         title: Strings.panelTitles.restaurantOpeningSchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.restaurant,
               inputId: 'restaurantOpeningScheduleRestaurant',
               emptyOptionLabel: Strings.placeholders.restaurant,
            }),
            Fragments.createSchedulePresetField({
               inputId: 'restaurantOpeningSchedulePreset',
            }),
            Fragments.createDateRangeFields({
               startDateId: 'restaurantOpeningScheduleStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restaurantOpeningScheduleEndDate',
               endHelpText: Strings.help.keepScheduleUntilChanged,
            }),
            Fragments.createWeeklyScheduleCheckboxes({
               dayIds: {
                  monday: 'restaurantOpeningScheduleMonday',
                  tuesday: 'restaurantOpeningScheduleTuesday',
                  wednesday: 'restaurantOpeningScheduleWednesday',
                  thursday: 'restaurantOpeningScheduleThursday',
                  friday: 'restaurantOpeningScheduleFriday',
                  saturday: 'restaurantOpeningScheduleSaturday',
                  sunday: 'restaurantOpeningScheduleSunday',
                  holidays: 'restaurantOpeningScheduleHolidaysOnly',
               },
            }),
            Fragments.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'restaurantOpeningScheduleMessage',
               placeholder: Strings.textareas.scheduledClosedMessage('restaurant'),
            }),
            Fragments.createActions({
               submitId: 'submitRestaurantOpeningSchedule',
            }),
            Fragments.createStatus({
               statusId: 'restaurantOpeningScheduleStatus',
            }),
         ],
      });
   }
}
