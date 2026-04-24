import { createSingleMessageBanner } from './messageBanner.js';

export function createGiftShopClosedBanner() {
   return createSingleMessageBanner(
      giftShop => giftShop?.closed_message
   );
}
