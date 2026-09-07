import { TooltipCardElementBuilder } from './tooltipCardElementBuilder.js';
export class CardFactory {
   static createTooltipCard({
      index,
      image = null,
      title,
      details = [],
      links = [],
   } = {}) {
      const card = TooltipCardElementBuilder.createTooltipCardShell(index);

      if (image?.src) {
         card.appendChild(TooltipCardElementBuilder.createTooltipImageFrame(image));
      }

      if (title?.element) {
         card.appendChild(title.element);
      }
      else if (title?.text) {
         card.appendChild(
            TooltipCardElementBuilder.createTextElement(title.tagName || 'strong', title.text, {
               className: title.className,
               dataset: title.dataset,
            })
         );
      }

      details.filter(Boolean).forEach((detail) => {
         card.appendChild(TooltipCardElementBuilder.createTextElement('span', detail));
      });

      links
         .filter((link) => link?.href && link?.text)
         .forEach((link) => {
            card.appendChild(TooltipCardElementBuilder.createTooltipLinkLine(link));
         });

      return card;
   }
}
