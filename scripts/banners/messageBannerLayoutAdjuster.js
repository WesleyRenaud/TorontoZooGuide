import { SvgConstants } from '../shared/svgConstants.js';

export class MessageBannerLayoutAdjuster {
   static SVG_NS = SvgConstants.SVG_NS;

   static SNOWFLAKE_PATH = 'M12 22L12 2M20.66 17L3.34 7M20.66 7L3.34 17'
      + 'M9.88 3.88L12 6L14.12 3.88M3.91 9.78L6.8 9L6.03 6.1M6.03 17.9L6.8 15L3.91 14.22'
      + 'M14.12 20.12L12 18L9.88 20.12M20.09 14.22L17.2 15L17.97 17.9M17.97 6.1L17.2 9L20.09 9.78';

   static createSvgNode(tagName, attributes = {}) {
      const node = document.createElementNS(MessageBannerLayoutAdjuster.SVG_NS, tagName);

      Object.entries(attributes).forEach(([key, value]) => {
         node.setAttribute(key, String(value));
      });

      return node;
   }

   static createWarningIcon() {
      const svg = MessageBannerLayoutAdjuster.createSvgNode('svg', {
         class: 'off-display-warning-icon',
         viewBox: '0 0 24 24',
         'aria-hidden': 'true',
         focusable: 'false',
      });

      svg.append(
         MessageBannerLayoutAdjuster.createSvgNode('path', {
            d: 'M12 2L1 21h22L12 2z',
         }),
         MessageBannerLayoutAdjuster.createSvgNode('rect', {
            x: '11',
            y: '8',
            width: '2',
            height: '7',
         }),
         MessageBannerLayoutAdjuster.createSvgNode('circle', {
            cx: '12',
            cy: '18',
            r: '1.5',
         })
      );

      return svg;
   }

   static createSnowflakeIcon() {
      const svg = MessageBannerLayoutAdjuster.createSvgNode('svg', {
         class: 'off-display-snowflake-icon',
         viewBox: '0 0 24 24',
         'aria-hidden': 'true',
         focusable: 'false',
      });

      svg.append(
         MessageBannerLayoutAdjuster.createSvgNode('path', {
            d: MessageBannerLayoutAdjuster.SNOWFLAKE_PATH,
         })
      );

      return svg;
   }
}
