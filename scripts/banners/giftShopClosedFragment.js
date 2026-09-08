import { MessageFragment } from './messageFragment.js';

export class GiftShopClosedFragment {
   static createGiftShopClosedBanner() {
      return MessageFragment.createSingleMessageBanner(
         giftShop => giftShop?.closed_message
      );
   }
}
