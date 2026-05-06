import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createStatus,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createDrinkingFountainsOpenPanel() {
   return createPanelShell({
      panelId: 'drinkingFountainsOpenPanel',
      title: APP_STRINGS.panelTitles.drinkingFountainsOpen,
      bodyChildren: [
         createDateRangeFields({
            startDateId: 'drinkingFountainsOpenStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'drinkingFountainsOpenEndDate',
            endHelpText: APP_STRINGS.help.keepExplicitlyOpenUntilChanged('drinking fountains', 'they are'),
         }),
         createActions({
            submitId: 'submitDrinkingFountainsOpen',
         }),
         createStatus({
            statusId: 'drinkingFountainsOpenStatus',
         }),
      ],
   });
}
