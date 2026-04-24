export function createMessageBanner({
   getMessages = () => [],
} = {}) {
   let element = null;
   let textElement = null;

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

   function ensure() {
      if (element) {
         return element;
      }

      element = document.createElement('div');
      element.className = 'off-display-closed-banner';
      element.style.display = 'none';

      const iconElement = document.createElement('div');
      iconElement.className = 'off-display-closed-icon';
      iconElement.textContent = '⚠';

      textElement = document.createElement('div');
      textElement.className = 'off-display-closed-text';

      const closeButton = document.createElement('button');
      closeButton.className = 'off-display-closed-close';
      closeButton.type = 'button';
      closeButton.setAttribute('aria-label', 'Close');
      closeButton.textContent = '×';

      element.addEventListener('click', event => event.stopPropagation());
      closeButton.addEventListener('click', event => {
         event.stopPropagation();
         hide();
      });

      element.append(iconElement, textElement, closeButton);
      document.body.appendChild(element);

      return element;
   }

   function hide() {
      if (!element) return;
      element.style.display = 'none';
   }

   function sync(item) {
      const messages = getMessages(item);

      if (!messages.length) {
         hide();
         return;
      }

      const banner = ensure();
      renderMessages(messages);
      banner.style.display = 'flex';
   }

   return { sync, hide };
}

export function createSingleMessageBanner(getMessage) {
   return createMessageBanner({
      getMessages: item => {
         const message = getMessage(item);
         return message ? [message] : [];
      },
   });
}
