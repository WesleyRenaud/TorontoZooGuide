export class WarningIconHelpers {
   static SVG_NS = 'http://www.w3.org/2000/svg';

   static createSvgNode(tagName, attributes = {}) {
      const node = document.createElementNS(WarningIconHelpers.SVG_NS, tagName);

      Object.entries(attributes).forEach(([key, value]) => {
         node.setAttribute(key, String(value));
      });

      return node;
   }
}
