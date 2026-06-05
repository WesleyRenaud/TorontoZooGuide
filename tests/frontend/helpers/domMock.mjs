/** Minimal DOM stubs for itinerary panel component tests. */

import {
   TIMELINE_PILL_STRIP_TOP_OFFSET_PX,
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SLOT_HEIGHT_PX,
} from '../../../scripts/shared/constants.js';

export function createDomNode(tagName = 'div', className = '', textContent = '') {
   const children = [];
   const listeners = {};
   const classes = new Set(className ? className.split(/\s+/).filter(Boolean) : []);
   const attributes = {};

   const node = {
      tagName,
      get className() {
         return [...classes].join(' ');
      },
      set className(value) {
         classes.clear();

         for (const token of String(value).split(/\s+/)) {
            if (token) {
               classes.add(token);
            }
         }
      },
      textContent,
      children,
      listeners,
      dataset: {},
      hidden: false,
      type: '',
      tabIndex: 0,
      classList: {
         contains(value) {
            return classes.has(value);
         },
         add(value) {
            classes.add(value);
         },
         toggle(value, shouldAdd) {
            if (shouldAdd) {
               classes.add(value);
            }
            else {
               classes.delete(value);
            }
         },
      },
      appendChild(child) {
         child.parentElement = node;
         child.parent = node;
         children.push(child);
         return child;
      },
      removeChild(child) {
         const childIndex = children.indexOf(child);

         if (childIndex >= 0) {
            children.splice(childIndex, 1);
         }

         child.parentElement = null;
         child.parent = null;

         return child;
      },
      closest(selector) {
         let current = node;

         while (current) {
            if (nodeMatchesSelector(current, selector)) {
               return current;
            }

            current = current.parentElement ?? current.parent;
         }

         return null;
      },
      contains(other) {
         if (!other) {
            return false;
         }

         let current = other;

         while (current) {
            if (current === node) {
               return true;
            }

            current = current.parentElement ?? current.parent;
         }

         return false;
      },
      get offsetHeight() {
         if (classes.has('itinerary-day-open-pill')) {
            return TIMELINE_POINT_PILL_HEIGHT_PX;
         }

         if (classes.has('itinerary-day-grid-line')) {
            return TIMELINE_SLOT_HEIGHT_PX;
         }

         return 0;
      },
      getBoundingClientRect() {
         const height = classes.has('itinerary-day-open-pill')
            ? TIMELINE_POINT_PILL_HEIGHT_PX
            : 0;

         return {
            height,
            width: 0,
            top: 0,
            left: 0,
            right: 0,
            bottom: height,
         };
      },
      style: {
         setProperty(name, value) {
            this[name] = value;
         },
      },
      append(...items) {
         for (const item of items) {
            if (item && typeof item === 'object') {
               item.parentElement = node;
               item.parent = node;
            }

            children.push(item);
         }
      },
      replaceChildren(...items) {
         for (const child of children) {
            child.parentElement = null;
            child.parent = null;
         }

         children.length = 0;

         for (const item of items) {
            if (item.tagName === '#fragment') {
               for (const child of item.children) {
                  child.parentElement = node;
                  child.parent = node;
                  children.push(child);
               }
            }
            else {
               item.parentElement = node;
               item.parent = node;
               children.push(item);
            }
         }
      },
      addEventListener(eventName, handler) {
         listeners[eventName] = handler;
      },
      click() {
         listeners.click?.();
      },
      remove() {},
      setAttribute(name, value) {
         attributes[name] = value;
         node[name] = value;
      },
      getAttribute(name) {
         return attributes[name] ?? node[name] ?? null;
      },
      querySelector(selector) {
         return queryNode(node, selector);
      },
      querySelectorAll(selector) {
         return queryNodes(node, selector);
      },
      focus() {},
   };

   return node;
}

function queryNode(root, selector) {
   if (!selector.startsWith('.')) {
      return null;
   }

   const classNameToFind = selector.slice(1);
   const stack = [root];

   while (stack.length > 0) {
      const current = stack.shift();

      if (
         current !== root
         && current.className?.split(/\s+/).includes(classNameToFind)
      ) {
         return current;
      }

      stack.push(...current.children);
   }

   return null;
}

function queryNodes(root, selector) {
   if (!selector.startsWith('.')) {
      return [];
   }

   const classNameToFind = selector.slice(1);
   const matches = [];
   const stack = [root];

   while (stack.length > 0) {
      const current = stack.shift();

      if (
         current !== root
         && current.className?.split(/\s+/).includes(classNameToFind)
      ) {
         matches.push(current);
      }

      stack.push(...current.children);
   }

   return matches;
}

function nodeMatchesSelector(node, selector) {
   if (!node || !selector) {
      return false;
   }

   if (selector[0] === '.') {
      const className = selector.slice(1);
      return node.classList?.contains(className) ?? false;
   }

   const dataAttributeMatch = selector.match(/^\[data-([^\]=]+)(?:="([^"]*)")?\]$/);

   if (dataAttributeMatch) {
      const datasetKey = dataAttributeMatch[1].replace(
         /-([a-z])/g,
         (_, character) => character.toUpperCase()
      );
      const expectedValue = dataAttributeMatch[2];
      const actualValue = node.dataset?.[datasetKey];

      if (expectedValue === undefined) {
         return actualValue != null && actualValue !== '';
      }

      return String(actualValue) === expectedValue;
   }

   return false;
}

function querySelectorInNode(node, selector) {
   if (!node) {
      return null;
   }

   if (nodeMatchesSelector(node, selector)) {
      return node;
   }

   for (const child of node.children ?? []) {
      const match = querySelectorInNode(child, selector);

      if (match) {
         return match;
      }
   }

   return null;
}

export function installDocument() {
   const itineraryPanel = createDomNode('div', 'itinerary-panel');
   const itineraryFlow = createDomNode('div', 'itinerary-flow');
   itineraryFlow.id = 'itineraryFlow';
   const body = createDomNode('body');

   body.appendChild = (child) => {
      body.children.push(child);
      return child;
   };
   body.appendChild(itineraryPanel);
   body.appendChild(itineraryFlow);

   globalThis.document = {
      body,
      getElementById: (id) => {
         if (id === 'itineraryFlow') {
            return itineraryFlow;
         }

         return null;
      },
      addEventListener: () => {},
      removeEventListener: () => {},
      createElement: (tagName) => {
         if (tagName === 'button') {
            return createDomNode('button');
         }

         return createDomNode(tagName);
      },
      createDocumentFragment: () => {
         const fragment = createDomNode('#fragment');
         fragment.appendChild = (child) => {
            fragment.children.push(child);
            return child;
         };
         return fragment;
      },
      createTextNode: (textContent) => createDomNode('#text', '', textContent),
      querySelector: (selector) => (
         querySelectorInNode(body, selector)
         ?? querySelectorInNode(itineraryPanel, selector)
      ),
   };
}

export function teardownDocument() {
   delete globalThis.document;
   delete globalThis.requestAnimationFrame;
}

export function installTestWindow() {
   globalThis.requestAnimationFrame = (callback) => {
      callback();
      return 0;
   };

   const getComputedStyle = (element) => ({
      gap: '0',
      paddingBottom: '0',
      paddingTop: '0',
      rowGap: '0',
      getPropertyValue(property) {
         if (
            property === '--itinerary-half-hour-slot-height'
            && element?.classList?.contains('itinerary-day-timeline')
         ) {
            return `${TIMELINE_SLOT_HEIGHT_PX}px`;
         }

         if (
            property === '--itinerary-pill-strip-top-offset'
            && element?.classList?.contains('itinerary-day-timeline')
         ) {
            return `${TIMELINE_PILL_STRIP_TOP_OFFSET_PX}px`;
         }

         return '';
      },
   });

   globalThis.getComputedStyle = getComputedStyle;

   globalThis.window = {
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => true,
      getComputedStyle,
      open: () => {},
   };
}
