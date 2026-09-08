import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationRouteControlsBuilder } from '../../../scripts/map/transportationRouteControlsBuilder.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_RadioGroupName_TestTransportation_ExpectNormalized', () => {
   assert.equal(
      TransportationRouteControlsBuilder.radioGroupName('Zoomobile'),
      'transportationRoute-zoomobile'
   );
});

test('Test_CreateRouteOption_TestChecked_ExpectRadioLabel', () => {
   const option = TransportationRouteControlsBuilder.createRouteOption({
      groupName: 'transportationRoute-zoomobile',
      value: 'current',
      label: 'Current Route',
      checked: true,
   });

   assert.equal(option.className, 'transportation-route-option');
   assert.equal(option.children[0].type, 'radio');
   assert.equal(option.children[0].checked, true);
   assert.equal(option.children[1].textContent, 'Current Route');
});

test('Test_CreateTransportationRouteSection_TestRoutes_ExpectOptions', () => {
   const section = TransportationRouteControlsBuilder.createTransportationRouteSection({
      name: 'Zoomobile',
      routes: ['red', 'blue'],
   });

   assert.equal(section.className, 'transportation-route');
   assert.equal(section.dataset.transportation, 'Zoomobile');
   assert.match(section.textContent, new RegExp(Strings.map.transportationRoute.title('Zoomobile')));
   assert.match(section.textContent, new RegExp(Strings.map.transportationRoute.none));
   assert.match(section.textContent, /Red Route/);
   assert.match(section.textContent, /Blue Route/);
});
