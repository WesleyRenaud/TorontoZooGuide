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

export function createAttractionOpenPanel() {
   return createPanelShell({
      panelId: 'attractionOpenPanel',
      title: APP_STRINGS.panelTitles.attractionOpen,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.attraction,
            inputId: 'attractionOpenAttraction',
            emptyOptionLabel: APP_STRINGS.placeholders.attraction,
         }),
         createSchedulePresetField({
            inputId: 'attractionOpenPreset',
         }),
         createDateRangeFields({
            startDateId: 'attractionOpenStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'attractionOpenEndDate',
            endHelpText: APP_STRINGS.help.keepScheduleUntilChanged,
         }),
         createWeeklyScheduleCheckboxes({
            dayIds: {
               monday: 'attractionOpenMonday',
               tuesday: 'attractionOpenTuesday',
               wednesday: 'attractionOpenWednesday',
               thursday: 'attractionOpenThursday',
               friday: 'attractionOpenFriday',
               saturday: 'attractionOpenSaturday',
               sunday: 'attractionOpenSunday',
               holidays: 'attractionOpenHolidaysOnly',
            },
         }),
         createTextareaField({
            label: APP_STRINGS.labels.scheduleMessage,
            inputId: 'attractionOpenMessage',
            placeholder: APP_STRINGS.textareas.scheduledClosedMessage('attraction'),
         }),
         createActions({
            submitId: 'submitAttractionOpen',
         }),
         createStatus({
            statusId: 'attractionOpenStatus',
         }),
      ],
   });
}
