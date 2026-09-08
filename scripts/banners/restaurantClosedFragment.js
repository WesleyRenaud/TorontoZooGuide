import { MessageFragment } from './messageFragment.js';

export class RestaurantClosedFragment {
   static createRestaurantClosedBanner() {
      return MessageFragment.createSingleMessageBanner(
         restaurant => restaurant?.closed_message
      );
   }
}
