import {
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SLOT_HEIGHT_PX,
} from '../../../scripts/shared/constants.js';
import {
   nodeMatchesSelector,
   queryNode,
   queryNodes,
} from './domSelectorMock.mjs';

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
         remove(value) {
            classes.delete(value);
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
         const existingHandler = listeners[eventName];

         if (!existingHandler) {
            listeners[eventName] = handler;
            return;
         }

         listeners[eventName] = (event) => {
            existingHandler(event);
            handler(event);
         };
      },
      click() {
         const event = {
            preventDefault() {},
            stopPropagation() {},
         };

         listeners.click?.(event);
      },
      remove() {
         const parent = node.parentElement ?? node.parent;

         parent?.removeChild?.(node);
      },
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
      blur() {},
   };

   return node;
}
