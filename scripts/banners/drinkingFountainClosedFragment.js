import { MessageFragment } from './messageFragment.js';

export class DrinkingFountainClosedFragment {
   static createDrinkingFountainClosedBanner() {
      return MessageFragment.createSingleMessageBanner(
         drinkingFountain => drinkingFountain?.closed_message
      );
   }
}
