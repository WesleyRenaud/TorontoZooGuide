import { MessageBanner } from './messageBanner.js';

export class OffDisplayBanner {
   static createOffDisplayBanner() {
      return MessageBanner.createMessageBanner({
         getMessages: animal => {
            const messages = [];

            if (animal?.off_display_message) {
               messages.push(animal.off_display_message);
            }

            if (animal?.limited_viewing_message) {
               messages.push(animal.limited_viewing_message);
            }

            if (animal?.viewing_alert_messages?.length) {
               messages.push(animal.viewing_alert_messages.join('\n\n'));
            }

            return [...new Set(messages)];
         },
      });
   }
}
