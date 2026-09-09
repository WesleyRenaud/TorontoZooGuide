import { SvgConstants } from '../shared/svgConstants.js';

export class WarningIconHelper {
   static SVG_NS = SvgConstants.SVG_NS;

   static createSvgNode(tagName, attributes = {}) {
      const node = document.createElementNS(WarningIconHelper.SVG_NS, tagName);

      Object.entries(attributes).forEach(([key, value]) => {
         node.setAttribute(key, String(value));
      });

      return node;
   }
}
