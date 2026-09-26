import assert from 'node:assert/strict';
import test from 'node:test';

import { WarningIconHelper } from '../../../scripts/assets/warningIconHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_CreateSvgNode_TestAttributes_ExpectNamespacedNode', () => {
   const created = [];
   const tagName = 'path';
   const pathData = 'M0 0';
   const fill = 'red';
   globalThis.document = {
      createElementNS(ns, createdTagName) {
         const attrs = {};
         const node = {
            tagName: createdTagName,
            ns,
            attrs,
            setAttribute(key, value) { attrs[key] = value; },
         };
         created.push(node);
         return node;
      },
   };

   const node = WarningIconHelper.createSvgNode(tagName, { d: pathData, fill });

   assert.equal(node.ns, WarningIconHelper.SVG_NS);
   assert.equal(node.tagName, tagName);
   assert.equal(node.attrs.d, pathData);
   assert.equal(node.attrs.fill, fill);
   assert.equal(created.at(Position.FIRST), node);
});
