export class TooltipCardElementBuilder {
   static applyDataset(element, dataset = {}) {
      Object.entries(dataset).forEach(([key, value]) => {
         if (value == null) {
            return;
         }

         element.dataset[key] = String(value);
      });
   }

   static createTooltipCardShell(index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = String(index);
      card.style.display = index === 0 ? 'flex' : 'none';

      return card;
   }

   static createTooltipImageFrame({
      src,
      alt,
      fallbackSrc = null,
   } = {}) {
      const frame = document.createElement('div');
      frame.className = 'tooltip-image-frame';

      const image = document.createElement('img');
      image.src = src;
      image.alt = alt;
      image.className = 'tooltip-image';

      if (fallbackSrc) {
         image.addEventListener('error', function handleError() {
            image.removeEventListener('error', handleError);
            image.src = fallbackSrc;
         });
      }

      frame.appendChild(image);

      return frame;
   }

   static createTextElement(tagName, text, {
      className = '',
      dataset = {},
   } = {}) {
      const element = document.createElement(tagName);
      element.textContent = text;

      if (className) {
         element.className = className;
      }

      TooltipCardElementBuilder.applyDataset(element, dataset);

      return element;
   }

   static createTooltipLinkLine({
      href,
      text,
      className = '',
   } = {}) {
      const line = document.createElement('span');
      const link = document.createElement('a');

      link.href = href;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = text;
      link.className = className ? `tooltip-link ${className}` : 'tooltip-link';

      line.appendChild(link);

      return line;
   }
}
