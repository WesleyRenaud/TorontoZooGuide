import { GlobalAmenityStatusPanelBuilder } from '../../forms/globalAmenityStatusPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class DrinkingFountainsOpenView {
   static createDrinkingFountainsOpenPanel() {
      return GlobalAmenityStatusPanelBuilder.createPanel({
         panelId: 'drinkingFountainsOpenPanel',
         title: Strings.panelTitles.drinkingFountainsOpen,
         idPrefix: 'drinkingFountainsOpen',
         includeDateRange: false,
         submitId: 'submitDrinkingFountainsOpen',
         statusId: 'drinkingFountainsOpenStatus',
      });
   }
}
