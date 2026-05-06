import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createDrinkingFountainsClosedPanel() {
   return createPanelShell({
      panelId: 'drinkingFountainsClosedPanel',
      title: APP_STRINGS.panelTitles.drinkingFountainsClosed,
      bodyChildren: [
         createDateRangeFields({
            startDateId: 'drinkingFountainsClosedStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'drinkingFountainsClosedEndDate',
            endHelpText: APP_STRINGS.help.continueUntilReopened(
               'drinking fountains'
            ),
         }),
         createTextareaField({
            label: APP_STRINGS.labels.closedMessage,
            inputId: 'drinkingFountainsClosedMessage',
            placeholder: APP_STRINGS.textareas.drinkingFountainsClosedMessage,
         }),
         createActions({
            submitId: 'submitDrinkingFountainsClosed',
         }),
         createStatus({
            statusId: 'drinkingFountainsClosedStatus',
         }),
      ],
   });
}
