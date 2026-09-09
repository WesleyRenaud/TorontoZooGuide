import { GlobalAmenityStatusPanelBuilder } from '../../forms/globalAmenityStatusPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class DrinkingFountainsOpenView {
   static createDrinkingFountainsOpenPanel() {
      return GlobalAmenityStatusPanelBuilder.createPanel({
         panelId: 'drinkingFountainsOpenPanel',
         title: Strings.panelTitles.drinkingFountainsOpen,
         idPrefix: 'drinkingFountainsOpen',
         endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('drinking fountains', 'they are'),
         submitId: 'submitDrinkingFountainsOpen',
         statusId: 'drinkingFountainsOpenStatus',
      });
   }
}
