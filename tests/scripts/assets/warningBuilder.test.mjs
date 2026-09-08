import assert from 'node:assert/strict';
import test from 'node:test';

import { WarningBuilder } from '../../../scripts/assets/warningBuilder.js';
import { WarningIconHelper } from '../../../scripts/assets/warningIconHelper.js';

test('Test_CreateWarningIcon_TestDefaults_ExpectSvgChildren', () => {
   const created = [];
   globalThis.document = {
      createElementNS(ns, tagName) {
         const attrs = {};
         const node = {
            tagName,
            ns,
            attrs,
            children: [],
            setAttribute(key, value) { attrs[key] = value; },
            append(...nodes) { this.children.push(...nodes); },
         };
         created.push(node);
         return node;
      },
   };

   try {
      const svg = WarningBuilder.createWarningIcon();
      assert.equal(svg.tagName, 'svg');
      assert.equal(svg.attrs.class, 'itin-warning-icon');
      assert.equal(svg.attrs.viewBox, '0 0 24 24');
      assert.equal(svg.attrs['aria-hidden'], undefined);
      assert.equal(svg.children.length, 3);
      assert.equal(created[0].ns, WarningIconHelper.SVG_NS);
   } finally {
      delete globalThis.document;
   }
});

test('Test_CreateWarningIcon_TestAriaAndFocusable_ExpectAttributes', () => {
   globalThis.document = {
      createElementNS(_ns, tagName) {
         const attrs = {};
         const node = {
            tagName,
            attrs,
            children: [],
            setAttribute(key, value) { attrs[key] = value; },
            append(...nodes) { this.children.push(...nodes); },
         };
         return node;
      },
   };

   try {
      const svg = WarningBuilder.createWarningIcon({
         className: 'custom-warning',
         ariaHidden: true,
         focusable: 'false',
      });
      assert.equal(svg.attrs.class, 'custom-warning');
      assert.equal(svg.attrs['aria-hidden'], 'true');
      assert.equal(svg.attrs.focusable, 'false');
   } finally {
      delete globalThis.document;
   }
});
