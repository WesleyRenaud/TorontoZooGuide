import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class DrinkingFountainsOpenPanel {
   static createDrinkingFountainsOpenPanel() {
      return Fragments.createPanelShell({
         panelId: 'drinkingFountainsOpenPanel',
         title: Strings.panelTitles.drinkingFountainsOpen,
         bodyChildren: [
            Fragments.createDateRangeFields({
               startDateId: 'drinkingFountainsOpenStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'drinkingFountainsOpenEndDate',
               endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('drinking fountains', 'they are'),
            }),
            Fragments.createActions({
               submitId: 'submitDrinkingFountainsOpen',
            }),
            Fragments.createStatus({
               statusId: 'drinkingFountainsOpenStatus',
            }),
         ],
      });
   }
}
