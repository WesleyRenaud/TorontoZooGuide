import assert from 'node:assert/strict';
import test from 'node:test';

import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';
import { TransportationRouteControlsBuilder } from '../../../scripts/map/transportationRouteControlsBuilder.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_RadioGroupName_TestTransportation_ExpectNormalized', () => {
   const name = 'Zoomobile';

   const groupName = TransportationRouteControlsBuilder.radioGroupName(name);

   assert.equal(groupName, `transportationRoute-${AssetKeyNormalizer.normalize(name)}`);
});


test('Test_CreateRouteOption_TestChecked_ExpectRadioLabel', () => {
   const groupName = 'transportationRoute-zoomobile';
   const value = 'current';
   const label = 'Current Route';

   const option = TransportationRouteControlsBuilder.createRouteOption({
      groupName,
      value,
      label,
      checked: true,
   });
   const radio = option.children.at(Position.FIRST);
   const labelEl = option.children.at(Position.SECOND);

   assert.equal(option.className, 'transportation-route-option');
   assert.equal(radio.type, 'radio');
   assert.equal(radio.checked, true);
   assert.equal(labelEl.textContent, label);
});


test('Test_CreateTransportationRouteSection_TestRoutes_ExpectOptions', () => {
   const name = 'Zoomobile';
   const routes = ['red', 'blue'];

   const section = TransportationRouteControlsBuilder.createTransportationRouteSection({
      name,
      routes,
   });

   assert.equal(section.className, 'transportation-route');
   assert.equal(section.dataset.transportation, name);
   assert.match(section.textContent, new RegExp(Strings.map.transportationRoute.title(name)));
   assert.match(section.textContent, new RegExp(Strings.map.transportationRoute.none));
   assert.match(section.textContent, /Red Route/);
   assert.match(section.textContent, /Blue Route/);
});
