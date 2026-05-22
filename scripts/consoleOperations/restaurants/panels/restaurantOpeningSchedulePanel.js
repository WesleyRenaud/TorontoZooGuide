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

export function createRestaurantOpeningSchedulePanel() {
   return createPanelShell({
      panelId: 'restaurantOpeningSchedulePanel',
      title: APP_STRINGS.panelTitles.restaurantOpeningSchedule,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.restaurant,
            inputId: 'restaurantOpeningScheduleRestaurant',
            emptyOptionLabel: APP_STRINGS.placeholders.restaurant,
         }),
         createSchedulePresetField({
            inputId: 'restaurantOpeningSchedulePreset',
         }),
         createDateRangeFields({
            startDateId: 'restaurantOpeningScheduleStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'restaurantOpeningScheduleEndDate',
            endHelpText: APP_STRINGS.help.keepScheduleUntilChanged,
         }),
         createWeeklyScheduleCheckboxes({
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
         createTextareaField({
            label: APP_STRINGS.labels.scheduleMessage,
            inputId: 'restaurantOpeningScheduleMessage',
            placeholder: APP_STRINGS.textareas.scheduledClosedMessage('restaurant'),
         }),
         createActions({
            submitId: 'submitRestaurantOpeningSchedule',
         }),
         createStatus({
            statusId: 'restaurantOpeningScheduleStatus',
         }),
      ],
   });
}
