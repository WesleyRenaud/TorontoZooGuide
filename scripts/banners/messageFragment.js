import { MessageBannerLayoutAdjuster } from './messageBannerLayoutAdjuster.js';
import { Strings } from '../strings.js';

export class MessageFragment {
   static createMessageBanner({
      getMessages = () => [],
      isOffDisplayForSeason = () => false,
   } = {}) {
      let element = null;
      let iconElement = null;
      let textElement = null;
      let closeButtonElement = null;
      let onDismiss = null;

      function createMessageElement(message) {
         const messageElement = document.createElement('p');
         messageElement.className = 'off-display-closed-message';
         messageElement.textContent = message;
         return messageElement;
      }

      function renderMessages(messages) {
         textElement.replaceChildren(
            ...messages.map(createMessageElement)
         );
      }

      function renderSeason(banner, isSeason) {
         banner.classList.toggle('off-display-closed-banner--season', isSeason);
         iconElement.replaceChildren(
            isSeason
               ? MessageBannerLayoutAdjuster.createSnowflakeIcon()
               : MessageBannerLayoutAdjuster.createWarningIcon()
         );
      }

      function handleCloseClick(event) {
         event.stopPropagation();
         hide();

         if (!onDismiss) {
            return;
         }

         onDismiss();
      }

      function ensure() {
         if (element) {
            return element;
         }

         element = document.createElement('div');
         element.className = 'off-display-closed-banner';
         element.style.display = 'none';

         iconElement = document.createElement('div');
         iconElement.className = 'off-display-closed-icon';

         textElement = document.createElement('div');
         textElement.className = 'off-display-closed-text';

         closeButtonElement = document.createElement('button');
         closeButtonElement.className = 'off-display-closed-close';
         closeButtonElement.type = 'button';
         closeButtonElement.setAttribute('aria-label', Strings.common.close);
         closeButtonElement.textContent = Strings.common.closeSymbol;

         element.addEventListener('click', event => event.stopPropagation());
         closeButtonElement.addEventListener('click', handleCloseClick);

         element.append(iconElement, textElement, closeButtonElement);
         document.body.appendChild(element);

         return element;
      }

      function hide() {
         if (!element) return;
         element.style.display = 'none';
      }

      function getFocusableElements() {
         if (!element || element.style.display === 'none') {
            return [];
         }

         return [closeButtonElement];
      }

      function setOnDismiss(handler) {
         onDismiss = handler;
      }

      function sync(item) {
         const messages = getMessages(item);

         if (!messages.length) {
            hide();
            return;
         }

         const banner = ensure();
         renderSeason(banner, isOffDisplayForSeason(item));
         renderMessages(messages);
         banner.style.display = 'flex';
      }

      return { sync, hide, getFocusableElements, setOnDismiss };
   }

   static createSingleMessageBanner(getMessage, isOffDisplayForSeason = () => false) {
      return MessageFragment.createMessageBanner({
         getMessages: item => {
            const message = getMessage(item);
            return message ? [message] : [];
         },
         isOffDisplayForSeason,
      });
   }
}
