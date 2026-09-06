import { Strings } from '../strings.js';

const SVG_NS = 'http://www.w3.org/2000/svg';
const ALERT_WIDTH_TO_HEIGHT_RATIO = 2;
const ALERT_MIN_WIDTH = 560;
const ALERT_MAX_WIDTH = 1600;
const ALERT_VIEWPORT_GUTTER = 48;
const ALERT_MOBILE_MEDIA_QUERY = '(max-width: 720px)';
const ALERT_WIDTH_SEARCH_STEPS = 8;

function createSvgNode(tagName, attributes = {}) {
   const node = document.createElementNS(SVG_NS, tagName);

   Object.entries(attributes).forEach(([key, value]) => {
      node.setAttribute(key, String(value));
   });

   return node;
}

function createWarningIcon() {
   const svg = createSvgNode('svg', {
      class: 'off-display-warning-icon',
      viewBox: '0 0 24 24',
      'aria-hidden': 'true',
      focusable: 'false',
   });

   svg.append(
      createSvgNode('path', {
         d: 'M12 2L1 21h22L12 2z',
      }),
      createSvgNode('rect', {
         x: '11',
         y: '8',
         width: '2',
         height: '7',
      }),
      createSvgNode('circle', {
         cx: '12',
         cy: '18',
         r: '1.5',
      })
   );

   return svg;
}

function isMobileAlertLayout() {
   return typeof window !== 'undefined'
      && typeof window.matchMedia === 'function'
      && window.matchMedia(ALERT_MOBILE_MEDIA_QUERY).matches;
}

function getDesktopWidthRange() {
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

function setBannerWidth(element, width) {
   element.style.setProperty('--alert-banner-width', `${Math.round(width)}px`);
}

function getMeasuredHeight(element) {
   const rect = element.getBoundingClientRect();
   return rect.height || element.offsetHeight || 0;
}

function getWidthToHeightRatio(element, width) {
   setBannerWidth(element, width);

   const height = getMeasuredHeight(element);
   return height > 0 ? width / height : null;
}

function adjustBannerWidth(element) {
   if (isMobileAlertLayout()) {
      element.style.removeProperty('--alert-banner-width');
      return;
   }

   const { min, max } = getDesktopWidthRange();

   if (max <= 0) {
      element.style.removeProperty('--alert-banner-width');
      return;
   }

   if (min >= max) {
      setBannerWidth(element, max);
      return;
   }

   const minRatio = getWidthToHeightRatio(element, min);

   if (minRatio == null) {
      return;
   }

   if (minRatio >= ALERT_WIDTH_TO_HEIGHT_RATIO) {
      setBannerWidth(element, min);
      return;
   }

   const maxRatio = getWidthToHeightRatio(element, max);

   if (maxRatio == null || maxRatio <= ALERT_WIDTH_TO_HEIGHT_RATIO) {
      setBannerWidth(element, max);
      return;
   }

   let low = min;
   let high = max;

   for (let i = 0; i < ALERT_WIDTH_SEARCH_STEPS; i += 1) {
      const midpoint = (low + high) / 2;
      const ratio = getWidthToHeightRatio(element, midpoint);

      if (ratio == null) {
         return;
      }

      if (ratio < ALERT_WIDTH_TO_HEIGHT_RATIO) {
         low = midpoint;
      } else {
         high = midpoint;
      }
   }

   setBannerWidth(element, high);
}

export class MessageBanner {
   static createMessageBanner({
      getMessages = () => [],
   } = {}) {
      let element = null;
      let textElement = null;

      function createMessageElement(message) {
         const messageElement = document.createElement('p');
         messageElement.className = 'off-display-closed-message';
         messageElement.textContent = message;
         return messageElement;
      }

      function renderMessages(messages) {
         textElement.replaceChildren(
            ...messages.map(createMessageElement)
         );
      }

      function ensure() {
         if (element) {
            return element;
         }

         element = document.createElement('div');
         element.className = 'off-display-closed-banner';
         element.style.display = 'none';

         const iconElement = document.createElement('div');
         iconElement.className = 'off-display-closed-icon';
         iconElement.appendChild(createWarningIcon());

         textElement = document.createElement('div');
         textElement.className = 'off-display-closed-text';

         const closeButton = document.createElement('button');
         closeButton.className = 'off-display-closed-close';
         closeButton.type = 'button';
         closeButton.setAttribute('aria-label', Strings.common.close);
         closeButton.textContent = Strings.common.closeSymbol;

         element.addEventListener('click', event => event.stopPropagation());
         closeButton.addEventListener('click', event => {
            event.stopPropagation();
            hide();
         });

         element.append(iconElement, textElement, closeButton);
         document.body.appendChild(element);

         return element;
      }

      function hide() {
         if (!element) return;
         element.style.display = 'none';
      }

      function sync(item) {
         const messages = getMessages(item);

         if (!messages.length) {
            hide();
            return;
         }

         const banner = ensure();
         renderMessages(messages);
         banner.style.display = 'flex';
         adjustBannerWidth(banner);
      }

      return { sync, hide };
   }

   static createSingleMessageBanner(getMessage) {
      return MessageBanner.createMessageBanner({
         getMessages: item => {
            const message = getMessage(item);
            return message ? [message] : [];
         },
      });
   }
}
