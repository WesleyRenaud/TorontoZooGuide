function applyDataset(element, dataset = {}) {
   Object.entries(dataset).forEach(([key, value]) => {
      if (value == null) {
         return;
      }

      element.dataset[key] = String(value);
   });
}

function createTooltipCardShell(index) {
   const card = document.createElement('div');
   card.className = 'tooltip-card';
   card.dataset.index = String(index);
   card.style.display = index === 0 ? 'flex' : 'none';

   return card;
}

function createTooltipImageFrame({
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

function createTextElement(tagName, text, {
   className = '',
   dataset = {},
} = {}) {
   const element = document.createElement(tagName);
   element.textContent = text;

   if (className) {
      element.className = className;
   }

   applyDataset(element, dataset);

   return element;
}

function createTooltipLinkLine({
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

export class CardFactory {
   static createTooltipCard({
      index,
      image = null,
      title,
      details = [],
      links = [],
   } = {}) {
      const card = createTooltipCardShell(index);

      if (image?.src) {
         card.appendChild(createTooltipImageFrame(image));
      }

      if (title?.element) {
         card.appendChild(title.element);
      }
      else if (title?.text) {
         card.appendChild(
            createTextElement(title.tagName || 'strong', title.text, {
               className: title.className,
               dataset: title.dataset,
            })
         );
      }

      details.filter(Boolean).forEach((detail) => {
         card.appendChild(createTextElement('span', detail));
      });

      links
         .filter((link) => link?.href && link?.text)
         .forEach((link) => {
            card.appendChild(createTooltipLinkLine(link));
         });

      return card;
   }
}
