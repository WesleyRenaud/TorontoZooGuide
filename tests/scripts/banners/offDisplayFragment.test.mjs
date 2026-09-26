import assert from 'node:assert/strict';
import test from 'node:test';

import { OffDisplayFragment } from '../../../scripts/banners/offDisplayFragment.js';
import { Position } from '../../../scripts/shared/enums/position.js';
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
   const offDisplay = 'Off display';
   const limitedViewing = 'Limited viewing';
   const alertOne = 'Alert one';
   const banner = OffDisplayFragment.createOffDisplayBanner();

   banner.sync({
      off_display_message: offDisplay,
      limited_viewing_message: limitedViewing,
      viewing_alert_messages: [alertOne, 'Alert two'],
   });
   const text = document.body.children.at(Position.LAST).textContent;

   assert.match(text, new RegExp(offDisplay));
   assert.match(text, new RegExp(limitedViewing));
   assert.match(text, new RegExp(alertOne));
});


test('Test_CreateOffDisplayBanner_TestTransportationAnimal_ExpectPlannedViaMessage', () => {
   const transportation = 'Zoomobile';
   const banner = OffDisplayFragment.createOffDisplayBanner();

   banner.sync({
      added_by_transportation: true,
      transportation,
   });
   const bannerEl = document.body.children.at(Position.LAST);

   assert.equal(bannerEl.style.display, 'flex');
   assert.equal(
      bannerEl.querySelector('.off-display-closed-message')?.textContent,
      Strings.itinerary.map.plannedViaTransportation(transportation)
   );
});


test('Test_CreateOffDisplayBanner_TestClearTransportation_ExpectHidden', () => {
   const banner = OffDisplayFragment.createOffDisplayBanner();
   banner.sync({
      added_by_transportation: true,
      transportation: 'Zoomobile',
   });
   const bannerEl = document.body.children.at(Position.LAST);

   banner.sync({ species: 'African Lion' });

   assert.equal(bannerEl.style.display, 'none');
});


test('Test_CreateOffDisplayBanner_TestZoomobileOnlyAnimal_ExpectVisibleViaMessage', () => {
   const transportation = 'Zoomobile';
   const banner = OffDisplayFragment.createOffDisplayBanner();

   banner.sync({
      is_zoomobile_only: true,
   });
   const bannerEl = document.body.children.at(Position.LAST);

   assert.equal(bannerEl.style.display, 'flex');
   assert.equal(
      bannerEl.querySelector('.off-display-closed-message')?.textContent,
      Strings.map.visibleViaTransportation(transportation)
   );
});


test('Test_CreateOffDisplayBanner_TestPlannedOverridesZoomobileOnly_ExpectPlannedMessage', () => {
   const transportation = 'Zoomobile';
   const banner = OffDisplayFragment.createOffDisplayBanner();
   banner.sync({
      is_zoomobile_only: true,
   });
   const bannerEl = document.body.children.at(Position.LAST);

   banner.sync({
      added_by_transportation: true,
      is_zoomobile_only: true,
      transportation,
   });

   assert.equal(
      bannerEl.querySelector('.off-display-closed-message')?.textContent,
      Strings.itinerary.map.plannedViaTransportation(transportation)
   );
   assert.equal(bannerEl.querySelectorAll('.off-display-closed-message').length, Position.SECOND);
});
