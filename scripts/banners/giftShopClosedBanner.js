import { MessageBanner } from './messageBanner.js';

export class GiftShopClosedBanner {
   static createGiftShopClosedBanner() {
      return MessageBanner.createSingleMessageBanner(
         giftShop => giftShop?.closed_message
      );
   }
}
