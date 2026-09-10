import { ManualTestRunner } from './manualTestRunner.js';

const runner = new ManualTestRunner({
   suiteListEl: document.getElementById( 'manualTestSuiteList' ),
   suiteViewEl: document.getElementById( 'manualTestSuiteView' ),
   statusEl: document.getElementById( 'manualTestStatus' ),
});

runner.start();
