import assert from 'node:assert/strict';
import test from 'node:test';

import { OffDisplayFragment } from '../../../scripts/banners/offDisplayFragment.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_CreateOffDisplayBanner_TestMessages_ExpectCombined', () => {
   const banner = OffDisplayFragment.createOffDisplayBanner();
   banner.sync({
      off_display_message: 'Off display',
      limited_viewing_message: 'Limited viewing',
      viewing_alert_messages: ['Alert one', 'Alert two'],
   });
   const text = document.body.children.at(-1).textContent;
   assert.match(text, /Off display/);
   assert.match(text, /Limited viewing/);
   assert.match(text, /Alert one/);
});

test('Test_CreateOffDisplayBanner_TestTransportationAnimal_ExpectPlannedViaMessage', () => {
   const banner = OffDisplayFragment.createOffDisplayBanner();
   banner.sync({
      added_by_transportation: true,
      transportation: 'Zoomobile',
   });
   const bannerEl = document.body.children.at(-1);
   assert.equal(bannerEl.style.display, 'flex');
   assert.equal(
      bannerEl.querySelector('.off-display-closed-message')?.textContent,
      Strings.itinerary.map.plannedViaTransportation('Zoomobile')
   );

   banner.sync({ species: 'African Lion' });
   assert.equal(bannerEl.style.display, 'none');
});

test('Test_CreateOffDisplayBanner_TestZoomobileOnlyAnimal_ExpectVisibleViaMessage', () => {
   const banner = OffDisplayFragment.createOffDisplayBanner();
   banner.sync({
      is_zoomobile_only: true,
   });
   const bannerEl = document.body.children.at(-1);
   assert.equal(bannerEl.style.display, 'flex');
   assert.equal(
      bannerEl.querySelector('.off-display-closed-message')?.textContent,
      Strings.map.visibleViaTransportation('Zoomobile')
   );

   banner.sync({
      added_by_transportation: true,
      is_zoomobile_only: true,
      transportation: 'Zoomobile',
   });
   assert.equal(
      bannerEl.querySelector('.off-display-closed-message')?.textContent,
      Strings.itinerary.map.plannedViaTransportation('Zoomobile')
   );
   assert.equal(bannerEl.querySelectorAll('.off-display-closed-message').length, 1);
});
