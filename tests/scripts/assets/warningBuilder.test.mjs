import assert from 'node:assert/strict';
import test from 'node:test';

import { WarningBuilder } from '../../../scripts/assets/warningBuilder.js';
import { WarningIconHelper } from '../../../scripts/assets/warningIconHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';


function _createDocument() {
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

   return created;
}


test('Test_CreateWarningIcon_TestDefaults_ExpectSvgChildren', () => {
   const created = _createDocument();
   const className = 'itin-warning-icon';
   const viewBox = '0 0 24 24';

   try {
      const svg = WarningBuilder.createWarningIcon();

      assert.equal(svg.tagName, 'svg');
      assert.equal(svg.attrs.class, className);
      assert.equal(svg.attrs.viewBox, viewBox);
      assert.equal(svg.attrs['aria-hidden'], undefined);
      assert.equal(svg.children.length, Position.FOURTH);
      assert.equal(created.at(Position.FIRST).ns, WarningIconHelper.SVG_NS);
   } finally {
      delete globalThis.document;
   }
});


test('Test_CreateWarningIcon_TestAriaAndFocusable_ExpectAttributes', () => {
   _createDocument();
   const className = 'custom-warning';
   const focusable = 'false';

   try {
      const svg = WarningBuilder.createWarningIcon({
         className,
         ariaHidden: true,
         focusable,
      });

      assert.equal(svg.attrs.class, className);
      assert.equal(svg.attrs['aria-hidden'], String(true));
      assert.equal(svg.attrs.focusable, focusable);
   } finally {
      delete globalThis.document;
   }
});
