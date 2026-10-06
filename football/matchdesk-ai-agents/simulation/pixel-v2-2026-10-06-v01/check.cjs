'use strict';
const assert=require('node:assert/strict');const sim=require('./pixel-simulation.js');let checks=0;
function test(name,fn){fn();checks++;console.log('PASS '+name);}
const p={model:'deterministic-test-fixture',status:'ready',probabilities:[.5,.25,.25]};
test('home interval',()=>assert.deepEqual(sim.sample(p,()=>.49).score,[1,0]));
test('draw lower boundary',()=>assert.equal(sim.sample(p,()=>.5).outcome,1));
test('away lower boundary',()=>assert.equal(sim.sample(p,()=>.75).outcome,2));
test('near one',()=>assert.equal(sim.sample(p,()=>.99999).outcome,2));
test('invalid probability sum',()=>assert.throws(()=>sim.validate({...p,probabilities:[.5,.5,.5]})));
test('negative value',()=>assert.throws(()=>sim.validate({...p,probabilities:[-.1,.6,.5]})));
test('missing model',()=>assert.throws(()=>sim.validate({...p,model:null})));
test('pending blocked',()=>assert.throws(()=>sim.validate({...p,status:'pending'})));
test('random out of range',()=>assert.throws(()=>sim.sample(p,()=>1)));
test('optional score distribution sampling',()=>{let i=0;const values=[.2,.95];assert.deepEqual(sim.sample({...p,scoreDistribution:[{home:1,away:0,probability:.2},{home:2,away:0,probability:.3},{home:1,away:1,probability:.25},{home:0,away:1,probability:.25}]},()=>values[i++]).score,[2,0]);});
test('score distribution mismatches rejected',()=>assert.throws(()=>sim.validate({...p,scoreDistribution:[{home:1,away:0,probability:1}]})));
test('uniform grid frequencies match probabilities',()=>{const counts=[0,0,0];for(let i=0;i<1000;i++)counts[sim.sample(p,()=>(i+.5)/1000).outcome]++;assert.deepEqual(counts,[500,250,250]);});
test('no non-home zero mass sampled',()=>assert.equal(sim.sample({...p,probabilities:[1,0,0]},()=>.999).outcome,0));
console.log(JSON.stringify({checks,passed:checks,browserVerified:false,realModel:false}));
