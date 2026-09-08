import assert from 'node:assert/strict';
import test from 'node:test';

import { BuildOnlyBuilder } from '../../../../../scripts/itinerary/panel/components/buildOnlyBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_RenderBuildOnly_TestBody_ExpectBuildButton', () => {
   const events = [];
   window.dispatchEvent = (event) => { events.push(event.type); return true; };

   const body = document.createElement('div');
   BuildOnlyBuilder.renderBuildOnly(body);

   const button = body.children[0].children[0];
   assert.equal(button.className, 'itin-panel-build-btn');
   assert.equal(button.textContent, Strings.itinerary.actions.build);
   button.click();
   assert.deepEqual(events, ['tzg:editItinerary']);
});
