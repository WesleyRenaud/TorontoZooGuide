const SVG_NS = 'http://www.w3.org/2000/svg';

const ALERT_WIDTH_TO_HEIGHT_RATIO = 2;

const ALERT_MIN_WIDTH = 560;

const ALERT_MAX_WIDTH = 1600;

const ALERT_VIEWPORT_GUTTER = 48;

const ALERT_MOBILE_MEDIA_QUERY = '(max-width: 720px)';

const ALERT_WIDTH_SEARCH_STEPS = 8;

export class MessageBannerLayoutAdjuster {
   static createSvgNode(tagName, attributes = {}) {
      const node = document.createElementNS(SVG_NS, tagName);

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

   static isMobileAlertLayout() {
      return typeof window !== 'undefined'
         && typeof window.matchMedia === 'function'
         && window.matchMedia(ALERT_MOBILE_MEDIA_QUERY).matches;
   }

   static getDesktopWidthRange() {
      const viewportWidth = typeof window !== 'undefined' && window.innerWidth
         ? window.innerWidth
         : ALERT_MAX_WIDTH + ALERT_VIEWPORT_GUTTER;
      const maxWidth = Math.min(ALERT_MAX_WIDTH, viewportWidth - ALERT_VIEWPORT_GUTTER);
      const clampedMaxWidth = Math.max(0, maxWidth);

      return {
         min: Math.min(ALERT_MIN_WIDTH, clampedMaxWidth),
         max: clampedMaxWidth,
      };
   }

   static setBannerWidth(element, width) {
      element.style.setProperty('--alert-banner-width', `${Math.round(width)}px`);
   }

   static getMeasuredHeight(element) {
      const rect = element.getBoundingClientRect();
      return rect.height || element.offsetHeight || 0;
   }

   static getWidthToHeightRatio(element, width) {
      MessageBannerLayoutAdjuster.setBannerWidth(element, width);

      const height = MessageBannerLayoutAdjuster.getMeasuredHeight(element);
      return height > 0 ? width / height : null;
   }

   static adjustBannerWidth(element) {
      if (MessageBannerLayoutAdjuster.isMobileAlertLayout()) {
         element.style.removeProperty('--alert-banner-width');
         return;
      }

      const { min, max } = MessageBannerLayoutAdjuster.getDesktopWidthRange();

      if (max <= 0) {
         element.style.removeProperty('--alert-banner-width');
         return;
      }

      if (min >= max) {
         MessageBannerLayoutAdjuster.setBannerWidth(element, max);
         return;
      }

      const minRatio = MessageBannerLayoutAdjuster.getWidthToHeightRatio(element, min);

      if (minRatio == null) {
         return;
      }

      if (minRatio >= ALERT_WIDTH_TO_HEIGHT_RATIO) {
         MessageBannerLayoutAdjuster.setBannerWidth(element, min);
         return;
      }

      const maxRatio = MessageBannerLayoutAdjuster.getWidthToHeightRatio(element, max);

      if (maxRatio == null || maxRatio <= ALERT_WIDTH_TO_HEIGHT_RATIO) {
         MessageBannerLayoutAdjuster.setBannerWidth(element, max);
         return;
      }

      let low = min;
      let high = max;

      for (let i = 0; i < ALERT_WIDTH_SEARCH_STEPS; i += 1) {
         const midpoint = (low + high) / 2;
         const ratio = MessageBannerLayoutAdjuster.getWidthToHeightRatio(element, midpoint);

         if (ratio == null) {
            return;
         }

         if (ratio < ALERT_WIDTH_TO_HEIGHT_RATIO) {
            low = midpoint;
         } else {
            high = midpoint;
         }
      }

      MessageBannerLayoutAdjuster.setBannerWidth(element, high);
   }
}
