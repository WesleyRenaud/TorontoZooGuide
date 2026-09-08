import { WarningIconHelper } from './warningIconHelper.js';

export class WarningBuilder {
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

      const svg = WarningIconHelper.createSvgNode('svg', attributes);

      svg.append(
         WarningIconHelper.createSvgNode('path', {
            d: 'M12 2L1 21h22L12 2z',
         }),
         WarningIconHelper.createSvgNode('rect', {
            x: '11',
            y: '9',
            width: '2',
            height: '6',
            fill: 'black',
         }),
         WarningIconHelper.createSvgNode('circle', {
            cx: '12',
            cy: '18',
            r: '1.6',
            fill: 'black',
         })
      );

      return svg;
   }
}
