import { MessageBanner } from './messageBanner.js';

export class RestaurantClosedBanner {
   static createRestaurantClosedBanner() {
      return MessageBanner.createSingleMessageBanner(
         restaurant => restaurant?.closed_message
      );
   }
}
