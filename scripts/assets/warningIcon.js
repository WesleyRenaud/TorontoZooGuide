import { WarningIconHelpers } from './warningIconHelpers.js';

export class WarningIcon {
   static createWarningIcon({
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

      const svg = WarningIconHelpers.createSvgNode('svg', attributes);

      svg.append(
         WarningIconHelpers.createSvgNode('path', {
            d: 'M12 2L1 21h22L12 2z',
         }),
         WarningIconHelpers.createSvgNode('rect', {
            x: '11',
            y: '9',
            width: '2',
            height: '6',
            fill: 'black',
         }),
         WarningIconHelpers.createSvgNode('circle', {
            cx: '12',
            cy: '18',
            r: '1.6',
            fill: 'black',
         })
      );

      return svg;
   }
}
