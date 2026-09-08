import assert from 'node:assert/strict';
import test from 'node:test';

import { WarningIconHelper } from '../../../scripts/assets/warningIconHelper.js';

test('Test_CreateSvgNode_TestAttributes_ExpectNamespacedNode', () => {
   const created = [];
   globalThis.document = {
      createElementNS(ns, tagName) {
         const attrs = {};
         const node = {
            tagName,
            ns,
            attrs,
            setAttribute(key, value) { attrs[key] = value; },
         };
         created.push(node);
         return node;
      },
   };

   const node = WarningIconHelper.createSvgNode('path', { d: 'M0 0', fill: 'red' });
   assert.equal(node.ns, WarningIconHelper.SVG_NS);
   assert.equal(node.tagName, 'path');
   assert.equal(node.attrs.d, 'M0 0');
   assert.equal(node.attrs.fill, 'red');
   assert.equal(created.length, 1);
});
