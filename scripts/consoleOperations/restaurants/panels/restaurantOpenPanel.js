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

export function createRestaurantOpenPanel() {
   return createPanelShell({
      panelId: 'restaurantOpenPanel',
      title: APP_STRINGS.panelTitles.restaurantOpen,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.restaurant,
            inputId: 'restaurantOpenRestaurant',
            emptyOptionLabel: APP_STRINGS.placeholders.restaurant,
         }),
         createSchedulePresetField({
            inputId: 'restaurantOpenPreset',
         }),
         createDateRangeFields({
            startDateId: 'restaurantOpenStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'restaurantOpenEndDate',
            endHelpText: APP_STRINGS.help.keepScheduleUntilChanged,
         }),
         createWeeklyScheduleCheckboxes({
            dayIds: {
               monday: 'restaurantOpenMonday',
               tuesday: 'restaurantOpenTuesday',
               wednesday: 'restaurantOpenWednesday',
               thursday: 'restaurantOpenThursday',
               friday: 'restaurantOpenFriday',
               saturday: 'restaurantOpenSaturday',
               sunday: 'restaurantOpenSunday',
               holidays: 'restaurantOpenHolidaysOnly',
            },
         }),
         createTextareaField({
            label: APP_STRINGS.labels.scheduleMessage,
            inputId: 'restaurantOpenMessage',
            placeholder: APP_STRINGS.textareas.scheduledClosedMessage('restaurant'),
         }),
         createActions({
            submitId: 'submitRestaurantOpen',
         }),
         createStatus({
            statusId: 'restaurantOpenStatus',
         }),
      ],
   });
}
