const SVG_NS = 'http://www.w3.org/2000/svg';

function createSvgNode(tagName, attributes = {}) {
   const node = document.createElementNS(SVG_NS, tagName);

   Object.entries(attributes).forEach(([key, value]) => {
      node.setAttribute(key, String(value));
   });

   return node;
}

export function createWarningIcon({
   className = 'itin-warning-icon',
   ariaHidden = false,
   focusable = null,
} = {}) {
   const attributes = {
      viewBox: '0 0 24 24',
      class: className,
   };

   if (ariaHidden) {
      attributes['aria-hidden'] = 'true';
   }

   if (focusable != null) {
      attributes.focusable = focusable;
   }

   const svg = createSvgNode('svg', attributes);

   svg.append(
      createSvgNode('path', {
         d: 'M12 2L1 21h22L12 2z',
      }),
      createSvgNode('rect', {
         x: '11',
         y: '9',
         width: '2',
         height: '6',
         fill: 'black',
      }),
      createSvgNode('circle', {
         cx: '12',
         cy: '18',
         r: '1.6',
         fill: 'black',
      })
   );

   return svg;
}
