(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const canvas = $('gameCanvas'), ctx = canvas.getContext('2d');
  const W = 1240, H = 850, TW = 47, TH = 25, OX = 619, OY = 159;
  const TAU = Math.PI * 2;
  const types = {
    arrow: { name: 'Arrow tower', cost: 60, color: '#76985d', description: 'Rapid arrows target the enemy closest to the base within range.', damage: [14, 25, 42], range: [2.65, 3.05, 3.5], interval: [.60, .52, .43], upgrades: [55, 85] },
    magic: { name: 'Starlight tower', cost: 90, color: '#a497c5', description: 'Starlight damages its target and nearby enemies.', damage: [23, 40, 65], range: [2.4, 2.85, 3.2], interval: [1.15, 1.03, .92], upgrades: [75, 115] }
  };
  const route = [{x:-.8,y:7},{x:3,y:7},{x:3,y:3},{x:7,y:3},{x:7,y:6},{x:10,y:6},{x:10,y:2},{x:11,y:2}];
  let routeLength = 0;
  const segments = route.slice(1).map((p,i) => {
    const a=route[i], length=Math.hypot(p.x-a.x,p.y-a.y), start=routeLength;
    routeLength+=length; return {a,b:p,length,start};
  });
  const road = new Set();
  segments.forEach(({a,b}) => {
    const count=Math.ceil(Math.hypot(b.x-a.x,b.y-a.y));
    for(let i=0;i<=count;i++){const t=i/count,x=Math.round(a.x+(b.x-a.x)*t),y=Math.round(a.y+(b.y-a.y)*t);if(x>=0&&x<12)road.add(`${x},${y}`);}
  });
  const padPositions = [[1,6],[2,8],[4,5],[5,2],[6,5],[8,4],[8,7],[9,1],[11,4],[10,8]];
  const missing = new Set(['0,0','0,1','1,0','11,9','11,8','10,9','0,9']);
  const cells=[];
  for(let x=0;x<12;x++)for(let y=0;y<10;y++)if(!missing.has(`${x},${y}`))cells.push({x,y});
  cells.sort((a,b)=>(a.x+a.y)-(b.x+b.y));
  const cellSet = new Set(cells.map(p=>`${p.x},${p.y}`));
  const decorations=[];
  const treePositions=[[2,0,1.1],[3,0,.85],[0,2,1],[1,1,.8],[0,3,.9],[0,4,.7],[1,3,.75],[1,4,.8],[2,2,.72],[4,0,.9],[5,0,.85],[6,0,1.03],[7,0,.7],[7,1,.75],[8,0,.85],[11,0,.8],[11,1,.65],[0,8,.75],[1,9,1],[3,9,.8],[4,8,.8],[4,9,1.1],[5,8,.9],[5,9,.65],[6,9,.8],[7,8,.8],[7,9,1],[9,9,.85],[11,6,.85],[11,7,1],[9,7,.55]];
  treePositions.forEach(([x,y,size],i)=>decorations.push({kind:i%4===0?'pine':'tree',x:x+(rand(i,2)-.5)*.2,y:y+(rand(i,9)-.5)*.2,size,seed:i}));
  [[2,5],[2,9],[4,2],[6,2],[8,2],[9,4],[9,8],[11,5],[4,7],[6,7],[0,5],[10,0],[8,9],[5,1]].forEach(([x,y],i)=>decorations.push({kind:i%3===0?'rock':'bush',x,y,size:.8,seed:i+80}));
  decorations.push({kind:'pond',x:1.2,y:2.1,size:1,seed:23},{kind:'ruin',x:9.4,y:.1,size:1,seed:50});
  let state, view={scale:1,x:0,y:0}, hover=null, lastTime=0, visualTime=0, toastTimer, sound=false, audioCtx;
  const waves=[
    Array.from({length:8},(_,i)=>({kind:i%3===2?'goblin':'slime',hp:i%3===2?48:38,speed:i%3===2?1.12:.97,reward:10,damage:1})),
    Array.from({length:12},(_,i)=>({kind:i===5||i===11?'troll':i%3?'goblin':'slime',hp:i===5||i===11?135:68,speed:i===5||i===11?.82:1.08,reward:i===5||i===11?20:12,damage:i===5||i===11?2:1})),
    Array.from({length:16},(_,i)=>({kind:i===15?'boss':i%5===4?'troll':i%4?'goblin':'slime',hp:i===15?380:i%5===4?185:94,speed:i===15?.73:i%5===4?.87:1.17,reward:i===15?40:i%5===4?22:14,damage:i===15?4:i%5===4?2:1}))
  ];
  function rand(a,b=0){const n=Math.sin(a*127.1+b*311.7)*43758.5453;return n-Math.floor(n);}
  function project(x,y){return {x:OX+(x-y)*TW,y:OY+(x+y)*TH};}
  function routePosition(progress){for(const s of segments){if(progress<=s.start+s.length){const t=Math.max(0,(progress-s.start)/s.length);return {x:s.a.x+(s.b.x-s.a.x)*t,y:s.a.y+(s.b.y-s.a.y)*t};}}return {...route[route.length-1]};}
  function distance(a,b){return Math.hypot(a.x-b.x,a.y-b.y);}
  function reset(){
    state={health:20,gold:180,wave:0,completed:0,phase:'ready',paused:false,speed:1,selectedType:'arrow',selectedTower:null,pads:padPositions.map(([x,y],id)=>({x,y,id,tower:null})),enemies:[],projectiles:[],particles:[],spawnIndex:0,spawnTimer:0,kills:0,nextId:0};
    hover=null; $('endOverlay').hidden=true; $('toast').classList.remove('visible'); clearTimeout(toastTimer); updateUI();
  }
  function toast(message){$('toast').textContent=message;$('toast').classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').classList.remove('visible'),2500);}
  function flash(id){const el=$(id);el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');}
  function selectType(type){if(!types[type])return;state.selectedType=type;state.selectedTower=null;updateUI();}
  function build(pad){
    if(state.phase==='won'||state.phase==='lost')return;
    if(pad.tower){state.selectedTower=pad.tower;updateUI();return;}
    const config=types[state.selectedType];
    if(state.gold<config.cost){toast(`Not enough gold. Building ${config.name} needs  ${config.cost} gold`);flash('goldValue');return;}
    state.gold-=config.cost;pad.tower={type:state.selectedType,level:1,x:pad.x,y:pad.y,padId:pad.id,cooldown:0,kick:0};
    burst(pad.x,pad.y,config.color,12);playSound('build');toast(`${config.name} ready · Click the tower to upgrade`);updateUI();
  }
  function upgrade(){
    const t=state.selectedTower;if(!t||t.level>=3||state.phase==='won'||state.phase==='lost')return;
    const config=types[t.type], cost=config.upgrades[t.level-1];
    if(state.gold<cost){toast(`Upgrade costs  ${cost}  gold. Defeat enemies to earn more.`);flash('goldValue');return;}
    state.gold-=cost;t.level++;burst(t.x,t.y,'#e8d99f',18);playSound('upgrade');toast(`${config.name} upgraded to level  ${t.level} !`);updateUI();
  }
  function startWave(){
    if(state.phase!=='ready')return;
    if(!state.pads.some(p=>p.tower))toast('Enemies incoming! Build on the green sites.');
    state.wave++;state.phase='battle';state.spawnIndex=0;state.spawnTimer=.5;state.paused=false;playSound('start');updateUI();
  }
  function burst(x,y,color,count){const p=project(x,y);for(let i=0;i<count;i++){const a=rand(i,visualTime)*TAU,s=20+rand(i,visualTime+3)*45;state.particles.push({x:p.x,y:p.y-15,vx:Math.cos(a)*s,vy:Math.sin(a)*s-30,life:.65,maxLife:.65,color,size:2+rand(i,visualTime)*3});}}
  function floatingText(x,y,text,color){const p=project(x,y);state.particles.push({x:p.x,y:p.y-33,vx:0,vy:-27,life:1.15,maxLife:1.15,color,text});}
  function hurt(enemy,damage){
    if(enemy.dead)return;enemy.hp-=damage;enemy.hit=.14;
    if(enemy.hp<=0){enemy.dead=true;state.gold+=enemy.reward;state.kills++;burst(enemy.x,enemy.y,enemy.kind==='slime'?'#9fb47c':'#c4ad75',6);floatingText(enemy.x,enemy.y,`+${enemy.reward}`,'#a07e35');playSound('coin');}
  }
  function finish(won){state.phase=won?'won':'lost';state.paused=false;state.projectiles=[];state.selectedTower=null;updateUI();
    $('endOverlay').hidden=false;$('endEmblem').textContent=won?'✦':'♡';$('endEyebrow').textContent=won?'FOREST PROTECTED':'A NEW DAWN AWAITS';$('endTitle').textContent=won?'The forest still shines':'The forest awaits your return';$('endDescription').innerHTML=won?`Three waves defeated. The forest heart is safe.<br>Health left: ${state.health} / 20 · Defeated: ${state.kills}  enemies`:`The base has fallen.<br>Build at bends, upgrade early, and try again.`;playSound(won?'win':'lose');
  }
  function update(dt){
    if(state.paused)return;
    state.particles.forEach(p=>{p.life-=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.text?0:35*dt;});state.particles=state.particles.filter(p=>p.life>0);
    if(state.phase!=='battle')return;
    let uiDirty=false;
    state.spawnTimer-=dt;
    if(state.spawnIndex<waves[state.wave-1].length&&state.spawnTimer<=0){const spec=waves[state.wave-1][state.spawnIndex++];state.enemies.push({...spec,id:state.nextId++,maxHp:spec.hp,progress:0,...routePosition(0),dead:false,hit:0,walk:rand(state.nextId)*6});state.spawnTimer=state.wave===1?1.12:state.wave===2?.95:.84;uiDirty=true;}
    for(const e of state.enemies){if(e.dead)continue;e.hit=Math.max(0,e.hit-dt);e.progress+=e.speed*dt;e.walk+=dt*8;Object.assign(e,routePosition(e.progress));if(e.progress>=routeLength){e.dead=true;state.health=Math.max(0,state.health-e.damage);burst(11,2,'#c18c72',12);floatingText(11,2,`−${e.damage} ♥`,'#bf7965');flash('healthValue');playSound('hurt');uiDirty=true;if(state.health<=0){finish(false);return;}}}
    for(const pad of state.pads){const t=pad.tower;if(!t)continue;t.kick=Math.max(0,t.kick-dt*4);t.cooldown-=dt;if(t.cooldown>0)continue;const config=types[t.type],lvl=t.level-1;let target=null;for(const e of state.enemies)if(!e.dead&&distance(t,e)<=config.range[lvl]&&(!target||e.progress>target.progress))target=e;
      if(target){const p=project(t.x,t.y);state.projectiles.push({type:t.type,target,damage:config.damage[lvl],from:{x:p.x,y:p.y-66},elapsed:0,duration:t.type==='arrow'?.17:.29,x:p.x,y:p.y-66,level:t.level});t.cooldown=config.interval[lvl];t.kick=1;playSound(t.type==='arrow'?'arrow':'magic');}
    }
    for(const p of state.projectiles){p.elapsed+=dt;if(p.target.dead){p.done=true;continue;}const targetPoint=project(p.target.x,p.target.y),a=Math.min(1,p.elapsed/p.duration);p.x=p.from.x+(targetPoint.x-p.from.x)*a;p.y=p.from.y+(targetPoint.y-17-p.from.y)*a-(p.type==='arrow'?Math.sin(a*Math.PI)*14:0);
      if(a>=1){p.done=true;if(p.type==='magic'){const location={x:p.target.x,y:p.target.y};for(const e of state.enemies)if(!e.dead&&distance(e,location)<1.1)hurt(e,p.damage);burst(location.x,location.y,'#b2a0d4',8);}else hurt(p.target,p.damage);uiDirty=true;}
    }
    state.projectiles=state.projectiles.filter(p=>!p.done);state.enemies=state.enemies.filter(e=>!e.dead);
    if(state.spawnIndex===waves[state.wave-1].length&&state.enemies.length===0){state.completed=state.wave;if(state.wave===3){finish(true);return;}state.phase='ready';state.gold+=30;state.projectiles=[];state.selectedTower=null;toast(`Wave ${state.wave}  cleared! +30 gold. Prepare for the next wave.`);playSound('clear');uiDirty=true;}
    if(uiDirty)updateUI();
  }
  function updateUI(){
    $('healthValue').textContent=state.health;$('goldValue').textContent=state.gold;$('waveValue').textContent=state.wave;
    const active=state.phase==='battle',done=state.phase==='won'||state.phase==='lost',next=Math.min(3,state.wave+1);
    $('phaseBadge').innerHTML=`<i></i> ${done?(state.phase==='won'?'Victory':'Base lost'):active?(state.paused?'Paused':'Enemies incoming'):'Prepare defenses'}`;$('phaseBadge').classList.toggle('battle',active);
    $('pauseButton').disabled=!active;$('pauseButton').innerHTML=`<svg class="icon"><use href="#i-${state.paused?'play':'pause'}"/></svg>`;$('pauseButton').title=state.paused?'Resume':'Pause';$('pauseButton').setAttribute('aria-label',$('pauseButton').title);
    $('speedButton').textContent=`${state.speed}×`;
    $('startWave').disabled=active||done;$('startWave').querySelector('span').textContent=done?(state.phase==='won'?'All waves cleared':'Base lost'):active?'Defending…':`Start wave  ${next} `;
    $('waveStatus').textContent=active?`Wave ${state.wave}  in progress`:state.completed?`Cleared: ${state.completed} `:'3 waves';
    document.querySelectorAll('.wave-step').forEach((el,i)=>{el.classList.toggle('current',i===(active?state.wave-1:state.completed)&&!done);el.classList.toggle('complete',i<state.completed);el.querySelector('span').textContent=i<state.completed?'✓':i+1;});
    const index=active?state.wave-1:Math.min(state.wave,2);$('waveInfo').textContent=`Wave ${index+1}  · ${waves[index].length}  enemies`;$('enemyCount').textContent=active?`Remaining: ${state.enemies.length+waves[index].length-state.spawnIndex}`:done?'Finished':'Ready';
    $('mapTipTitle').textContent=active?(state.paused?'Take a breath. Plan your next move.':'Your towers defend the forest'):state.completed?'Take a breath. Strengthen the line.':'Your forest. Your watch.';$('mapTipText').textContent=active?'Defeat enemies for gold. Build and upgrade during battle.':state.completed?'+30 gold after each wave. Start when ready.':'Choose a tower, then click a + on the map.';
    document.querySelectorAll('.tower-card').forEach(el=>{const selected=el.dataset.tower===state.selectedType;el.classList.toggle('selected',selected);el.classList.toggle('unaffordable',state.gold<types[el.dataset.tower].cost);el.setAttribute('aria-pressed',String(selected));});
    const config=types[state.selectedType];$('selectedTypeName').textContent=config.name;$('selectionHint').textContent=state.gold<config.cost?`Need  ${config.cost-state.gold}  more gold · Defeat enemies to earn it`:`Click a build site. Cost: ${config.cost} gold`;
    const t=state.selectedTower;$('buildPanel').hidden=!!t;$('upgradePanel').hidden=!t;
    if(t){const c=types[t.type],i=t.level-1;$('selectedLevel').textContent=`Level ${t.level} / 3`;$('upgradeName').textContent=c.name;$('upgradeDescription').textContent=c.description;$('attackValue').textContent=c.damage[i];$('rangeValue').textContent=`${c.range[i].toFixed(1)} tiles`;$('rateValue').textContent=`${c.interval[i].toFixed(2)} s`;
      const max=t.level>=3;$('upgradeButton').hidden=max;$('maxLevelMessage').hidden=!max;$('upgradePreview').textContent=max?'Fully upgraded and ready for the last stand.':`Next: damage  ${c.damage[i]} → ${c.damage[i+1]}, range  ${c.range[i].toFixed(1)} → ${c.range[i+1].toFixed(1)} tiles`;
      if(!max){$('upgradeCost').textContent=`${c.upgrades[i]} gold`;$('upgradeButton').disabled=state.gold<c.upgrades[i]||done;}
    }
  }
  function playSound(kind){
    if(!sound)return;try{audioCtx ||= new (window.AudioContext||window.webkitAudioContext)();if(audioCtx.state==='suspended')audioCtx.resume();const osc=audioCtx.createOscillator(),gain=audioCtx.createGain();const notes={arrow:[520,.045,.015],magic:[680,.1,.025],coin:[950,.07,.025],build:[330,.15,.035],upgrade:[660,.22,.035],start:[260,.18,.035],hurt:[150,.18,.045],win:[780,.45,.045],lose:[170,.4,.035],clear:[600,.28,.035]};const [f,d,v]=notes[kind]||notes.build;osc.type=kind==='hurt'?'triangle':'sine';osc.frequency.setValueAtTime(f,audioCtx.currentTime);osc.frequency.exponentialRampToValueAtTime(f*(kind==='lose'?.6:1.4),audioCtx.currentTime+d);gain.gain.setValueAtTime(v,audioCtx.currentTime);gain.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+d);osc.connect(gain);gain.connect(audioCtx.destination);osc.start();osc.stop(audioCtx.currentTime+d);}catch{sound=false;}
  }

  // The forest is drawn locally, from small geometric shapes and a seeded palette.
  function poly(points,fill,stroke,width=1){ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke();}}
  function ellipse(x,y,rx,ry,fill,stroke,width=1){ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,TAU);if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke();}}
  function line(x1,y1,x2,y2,color,width=1){ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke();}
  function roundRect(x,y,w,h,r,fill,stroke,width=1){ctx.beginPath();ctx.roundRect(x,y,w,h,r);if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke();}}
  function diamond(x,y,w,h,color,stroke){poly([[x,y-h],[x+w,y],[x,y+h],[x-w,y]],color,stroke);}
  function text(label,x,y,size,color,align='center',font='"Moss Sans",sans-serif'){ctx.font=`${size}px ${font}`;ctx.textAlign=align;ctx.fillStyle=color;ctx.fillText(label,x,y);}
  function leaf(x,y,size,color,angle=0){ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.beginPath();ctx.moveTo(-size,0);ctx.quadraticCurveTo(0,-size,size,0);ctx.quadraticCurveTo(0,size,-size,0);ctx.fillStyle=color;ctx.fill();ctx.restore();}
  function drawBackground(){
    ctx.fillStyle='#e8edde';ctx.fillRect(0,0,W,H);
    const grad=ctx.createRadialGradient(570,370,40,580,400,640);grad.addColorStop(0,'#f3f4e9');grad.addColorStop(1,'#e5ebdc');ctx.fillStyle=grad;ctx.fillRect(0,0,W,H);
    for(let i=0;i<145;i++){const x=rand(i,8)*W,y=rand(i,15)*H;ellipse(x,y,.6+rand(i)*1.1,.6,'#ced8bf77');}
    ctx.save();ctx.filter='blur(23px)';ellipse(639,656,425,93,'#869e6c26');ctx.restore();
    [[194,180,1],[1104,281,.65],[172,624,.8],[1006,696,.7],[443,718,.5]].forEach(([x,y,s],i)=>{ctx.save();ctx.translate(x,y);ctx.scale(s,s);diamond(0,0,17,9,'#c6d4b5');poly([[-17,0],[0,9],[17,0],[12,15],[-4,25],[-14,11]],'#afbe9d');diamond(0,-2,17,9,'#d6dfc7');leaf(4,-8,10,'#a6bb89',-.7);ctx.restore();});
  }
  function drawGround(){
    const grass=['#acc68a','#b1ca91','#b6ce94','#b1c98d','#b8ce97','#aac38a'];
    for(const c of cells){const p=project(c.x,c.y),depth=37+rand(c.x,c.y)*14;
      if(!cellSet.has(`${c.x+1},${c.y}`)){poly([[p.x,p.y+TH],[p.x+TW,p.y],[p.x+TW,p.y+depth],[p.x,p.y+TH+depth]],'#8fa878');line(p.x+2,p.y+TH+7,p.x+TW-2,p.y+9,'#a6b889',3);poly([[p.x+8,p.y+TH+15],[p.x+29,p.y+TH+5],[p.x+28,p.y+TH+24],[p.x+13,p.y+TH+30]],'#819b6b');line(p.x+36,p.y+21,p.x+36,p.y+34,'#799364',2);}
      if(!cellSet.has(`${c.x},${c.y+1}`)){poly([[p.x-TW,p.y],[p.x,p.y+TH],[p.x,p.y+TH+depth],[p.x-TW,p.y+depth]],'#789969');line(p.x-TW+3,p.y+8,p.x-2,p.y+TH+8,'#90a879',3);poly([[p.x-34,p.y+17],[p.x-16,p.y+25],[p.x-18,p.y+46],[p.x-32,p.y+37]],'#6e8e61');}
    }
    for(const c of cells){const p=project(c.x,c.y);diamond(p.x,p.y,TW+.2,TH+.2,grass[Math.floor(rand(c.x,c.y)*grass.length)]);
      if(!road.has(`${c.x},${c.y}`)){
        for(let i=0;i<4;i++){const u=(rand(c.x+i,c.y+11)-.5)*.78,v=(rand(c.x+7,c.y+i)-.5)*.78,q=project(c.x+u,c.y+v);line(q.x,q.y,q.x-2,q.y-4,'#84a86855',1.3);line(q.x,q.y,q.x+2,q.y-3,'#84a86855',1.3);}
        if(rand(c.x+31,c.y)>.69){const q=project(c.x+.2,c.y+.15);ellipse(q.x,q.y,2,1.5,'#e4e6b8');ellipse(q.x+6,q.y-3,1.6,1.3,'#f2edca');}
      }
    }
    for(const key of road){const [x,y]=key.split(',').map(Number),p=project(x,y);diamond(p.x,p.y,TW,TH,'#c5b487');diamond(p.x,p.y,TW-2,TH-1,'#decc9e');
      const shades=['#d4bf91','#e7d5aa','#cdbb8f','#e8d7af'];
      [[-.22,-.18],[.24,-.12],[-.15,.27],[.3,.26]].forEach(([a,b],i)=>{const q=project(x+a,y+b);diamond(q.x,q.y,8+rand(x+i,y)*5,4+rand(x,y+i)*2,shades[Math.floor(rand(x+i,y+2)*4)]);});
      if(rand(x,y)>.65){const q=project(x-.31,y+.22);line(q.x,q.y,q.x+4,q.y+2,'#b69e7566',1.2);}
    }
    // Quiet stepping stones make the path direction easy to read.
    [2.2,7.5,12.8,18].forEach(n=>{const a=routePosition(n),b=routePosition(n+.2),p=project(a.x,a.y),q=project(b.x,b.y),ang=Math.atan2(q.y-p.y,q.x-p.x);ctx.save();ctx.translate(p.x,p.y);ctx.rotate(ang);poly([[-4,-4],[3,0],[-4,4]],null,'#b29c70',1.5);ctx.restore();});
  }
  function drawPad(pad){const p=project(pad.x,pad.y),selected=hover===pad,canAfford=state.gold>=types[state.selectedType].cost;
    ellipse(p.x,p.y+5,31,16,'#7c9c6250');diamond(p.x,p.y,31,16,'#d1dcba','#8ca770');diamond(p.x,p.y-3,28,14,selected?'#e7edce':'#dce5c4',selected?'#648a4d':'#acc393');
    ctx.save();ctx.setLineDash([3,4]);ellipse(p.x,p.y-3,21,10,null,selected?'#719455':'#a1b884',1.2);ctx.restore();
    const bob=selected?Math.sin(visualTime*4)*1.5:0;line(p.x-6,p.y-5+bob,p.x+6,p.y-5+bob,canAfford?'#789b58':'#9ba986',2.7);line(p.x,p.y-11+bob,p.x,p.y+1+bob,canAfford?'#789b58':'#9ba986',2.7);
    if(selected){const label=`${types[state.selectedType].name} · ${types[state.selectedType].cost} gold`;roundRect(p.x-62,p.y-54,124,24,6,'#f5f7e9ed','#d3dfbf');text(label,p.x,p.y-38,11,'#60784d');}
  }
  function drawRange(tower){const c=types[tower.type],r=c.range[tower.level-1],points=[];for(let i=0;i<=64;i++){const a=i/64*TAU,q=project(tower.x+Math.cos(a)*r,tower.y+Math.sin(a)*r);points.push([q.x,q.y]);}ctx.save();ctx.setLineDash([5,5]);poly(points,tower.type==='arrow'?'#6a93571a':'#9681b01a',tower.type==='arrow'?'#72955190':'#9c88b890',1.4);ctx.restore();}
  function drawTree(d){const p=project(d.x,d.y);ctx.save();ctx.translate(p.x,p.y);ctx.scale(d.size,d.size);ellipse(3,1,31,15,'#688f5955');
    poly([[-5,-35],[6,-37],[8,1],[0,5],[-6,0]],'#8a8057');poly([[1,-35],[6,-37],[8,1],[0,5]],'#6c7148');line(0,-17,13,-32,'#7f794f',5);
    if(d.kind==='pine'){
      poly([[-27,-28],[0,-87],[28,-28],[0,-15]],'#597f5b');poly([[0,-87],[28,-28],[0,-15]],'#446d4d');poly([[-22,-48],[0,-101],[23,-48],[0,-36]],'#6e9565');poly([[0,-101],[23,-48],[0,-36]],'#507e53');poly([[-15,-70],[0,-112],[16,-70],[0,-62]],'#84a674');poly([[0,-112],[16,-70],[0,-62]],'#638b5a');
    }else{
      const colors=d.seed%3===0?['#7d9f69','#638954','#96b276']:d.seed%3===1?['#7b9d67','#527e53','#99b57b']:['#91ad70','#63864f','#adbf83'];
      ctx.beginPath();ctx.moveTo(-31,-34);ctx.bezierCurveTo(-45,-46,-38,-63,-26,-66);ctx.bezierCurveTo(-28,-86,-9,-98,8,-90);ctx.bezierCurveTo(22,-100,40,-80,34,-65);ctx.bezierCurveTo(53,-51,37,-29,21,-27);ctx.bezierCurveTo(6,-15,-17,-19,-31,-34);ctx.closePath();ctx.fillStyle=colors[0];ctx.fill();
      ctx.beginPath();ctx.moveTo(12,-90);ctx.bezierCurveTo(37,-88,35,-76,34,-65);ctx.bezierCurveTo(53,-51,37,-29,21,-27);ctx.bezierCurveTo(1,-13,-15,-25,-17,-28);ctx.bezierCurveTo(13,-25,29,-43,18,-59);ctx.bezierCurveTo(29,-75,18,-87,12,-90);ctx.fillStyle=colors[1];ctx.fill();
      ellipse(-12,-69,19,14,colors[2]);ellipse(-20,-54,12,8,colors[2]);ellipse(5,-80,12,9,colors[2]);leaf(-22,-49,5,'#c3cf9370',-.5);leaf(7,-70,4,'#d0d69c70',.5);
    }
    if(d.seed%4===1){ellipse(-15,4,5,2,'#78975a');line(-15,3,-15,-4,'#ddd5aa',2);ellipse(-15,-5,5,3,'#c79061');ellipse(-15,-6,1,1,'#f5e3b9');}ctx.restore();}
  function drawBush(d){const p=project(d.x,d.y);ctx.save();ctx.translate(p.x,p.y);ellipse(0,1,24,11,'#7d9d5e50');ellipse(-12,-7,12,10,'#88a667');ellipse(8,-10,15,13,'#7b9b5b');ellipse(2,-15,13,10,'#a0b77b');ellipse(14,-4,10,8,'#709052');leaf(-5,-16,5,'#becb8d');if(d.seed%2){[[1,-13],[8,-9],[-9,-8]].forEach(([x,y])=>ellipse(x,y,2.6,2.4,'#d5a277'));}ctx.restore();}
  function drawRock(d){const p=project(d.x,d.y);ctx.save();ctx.translate(p.x,p.y);ellipse(0,2,20,10,'#708e6250');poly([[-20,0],[-12,-17],[5,-23],[21,-6],[12,7],[-3,9]],'#a0ac90');poly([[-12,-17],[5,-23],[21,-6],[1,-5]],'#c1c7ad');poly([[1,-5],[21,-6],[12,7],[-3,9]],'#8a9a7e');poly([[-19,0],[-13,-7],[-7,-3],[-5,5]],'#88a064');ctx.restore();}
  function drawPond(d){const p=project(d.x,d.y);ctx.save();ctx.translate(p.x,p.y);ellipse(0,0,68,29,'#90ae81');ellipse(0,-3,61,25,'#83b9a9');ellipse(-4,-5,52,21,'#a2cebb');ctx.save();ctx.beginPath();ctx.ellipse(0,-3,60,24,0,0,TAU);ctx.clip();ctx.strokeStyle='#c7e0ca';ctx.lineWidth=2;for(let i=0;i<4;i++){ctx.beginPath();ctx.ellipse(-8+i*9,-8,12+i*14,4+i*4,0,.2,2.7);ctx.stroke();}ctx.restore();[[40,-10],[49,2],[-44,2]].forEach(([x,y])=>{ellipse(x,y,7,4,'#b9c1a0');ellipse(x-1,y-2,6,3,'#d6d7b8');});ellipse(-12,-3,11,5,'#789c62');poly([[-12,-3],[-2,-6],[-4,-1]],'#a2cebb');ellipse(-12,-7,3,2,'#e8d9ae');line(-47,-6,-47,-27,'#7f985d',2);line(-42,-5,-43,-21,'#7f985d',2);ellipse(-47,-25,2,5,'#a9925f');ctx.restore();}
  function drawRuin(d){const p=project(d.x,d.y);ctx.save();ctx.translate(p.x,p.y);diamond(0,0,27,14,'#91a578');poly([[-19,-3],[-19,-24],[-6,-32],[7,-25],[7,11]],'#b6b997');poly([[7,-25],[20,-31],[20,4],[7,11]],'#8f9f7f');poly([[-19,-24],[-6,-32],[20,-31],[7,-25]],'#cdd0ac');line(-15,-12,2,-3,'#92a17b',2);leaf(10,-9,11,'#7c9b5d',1);leaf(17,-20,8,'#8ea76a',-.5);ctx.restore();}
  function drawTower(t){const p=project(t.x,t.y),c=types[t.type],selected=state.selectedTower===t||hover?.tower===t;ctx.save();ctx.translate(p.x,p.y);if(selected)ellipse(0,2,36,19,'#e5edc680','#91ac6c',1.5);ellipse(0,5,29,14,'#728a5955');
    const magic=t.type==='magic';const base=magic?'#c4bad1':'#d7cba7',dark=magic?'#90849d':'#a69c76',light=magic?'#dfd7e6':'#eee2bf';
    poly([[-26,-4],[0,10],[27,-4],[27,7],[0,21],[-26,7]],dark);diamond(0,-4,27,14,light);poly([[-16,-45],[1,-35],[19,-45],[19,-3],[1,8],[-16,-3]],base);poly([[1,-35],[19,-45],[19,-3],[1,8]],dark);line(-12,-22,0,-15,magic?'#a398b5':'#b9ac83',1.4);line(5,-20,16,-26,magic?'#7e7390':'#968c69',1.4);
    ctx.save();ctx.translate(0,-t.kick*2);
    poly([[-23,-50],[0,-38],[24,-50],[24,-39],[0,-26],[-23,-39]],base);poly([[0,-38],[24,-50],[24,-39],[0,-26]],dark);diamond(0,-50,24,13,light);
    if(magic){const bob=Math.sin(visualTime*2+t.padId)*2;ctx.save();ctx.translate(0,bob);ctx.save();ctx.shadowColor='#c6b5e5';ctx.shadowBlur=12;poly([[0,-95],[-13,-72],[0,-49],[14,-72]],'#b2a0d8');ctx.restore();poly([[0,-95],[14,-72],[0,-49]],'#806aa7');poly([[0,-95],[-13,-72],[0,-72]],'#e3d5f2');line(0,-90,0,-55,'#c8b7e4',1.5);ctx.save();ctx.translate(0,-59);ctx.rotate(-.2);ellipse(0,0,23,7,null,'#c2a065',3);ctx.restore();ctx.restore();if(t.level>1){ellipse(-18,-79,2.5,2.5,'#cfbedf');ellipse(20,-72,2.5,2.5,'#dfc6ec');}}else{
      poly([[-26,-58],[0,-87],[27,-58],[0,-43]],'#648975');poly([[0,-87],[27,-58],[0,-43]],'#3c6e55');poly([[-26,-58],[-26,-52],[0,-37],[0,-43]],'#4f7b5b');poly([[0,-43],[27,-58],[27,-52],[0,-37]],'#305d49');line(0,-87,0,-96,'#987846',2);ellipse(0,-96,3,3,'#d5b065');line(-16,-58,-16,-65,'#436f54',4);line(17,-58,17,-65,'#315f48',4);
      ctx.beginPath();ctx.moveTo(-8,-62);ctx.quadraticCurveTo(9,-77,10,-59);ctx.strokeStyle='#ae8650';ctx.lineWidth=3;ctx.stroke();line(-8,-62,10,-59,'#e3d3a7',1.3);line(-4,-58,17,-71,'#755938',2);poly([[17,-71],[11,-70],[15,-66]],'#795b38');}
    ctx.restore();line(-2,-16,-2,-7,magic?'#e0d0ed':'#6e7754',4);
    for(let i=0;i<t.level;i++){ellipse(-((t.level-1)*5)+i*10,14,2.5,1.6,'#e7ce81');}
    ctx.restore();}
  function drawPortal(){const p=project(-.35,7);ctx.save();ctx.translate(p.x,p.y);ellipse(0,1,32,15,'#7c8b6544');diamond(0,-1,31,16,'#b2b095');
    ctx.beginPath();ctx.moveTo(-22,0);ctx.lineTo(-22,-35);ctx.bezierCurveTo(-22,-67,22,-67,22,-35);ctx.lineTo(22,0);ctx.fillStyle='#7c8d71';ctx.fill();
    ctx.beginPath();ctx.moveTo(-14,0);ctx.lineTo(-14,-33);ctx.bezierCurveTo(-14,-55,14,-55,14,-33);ctx.lineTo(14,0);ctx.fillStyle='#8d837f';ctx.fill();ellipse(0,-20,10,20,'#b6a394');line(-20,-34,-14,-32,'#b3b795',3);line(15,-22,21,-24,'#b3b795',3);leaf(-22,-49,9,'#75945e',-.4);leaf(23,-32,10,'#8d9f6b',.8);ctx.restore();label('Enemy entrance',p.x-28,p.y+41,'#7e8d70');}
  function drawCastle(){const p=project(11,2);ctx.save();ctx.translate(p.x,p.y);ellipse(0,6,52,24,'#7790624d');diamond(0,1,48,26,'#c5c9a4');poly([[-40,0],[0,21],[40,0],[40,12],[0,34],[-40,12]],'#a3ad8c');diamond(0,0,40,21,'#e4ddba');
    poly([[-24,-62],[3,-47],[28,-62],[28,0],[3,14],[-24,0]],'#e8ddba');poly([[3,-47],[28,-62],[28,0],[3,14]],'#b6b18c');line(-19,-18,0,-8,'#c9c19b',2);line(8,-16,25,-25,'#9ba381',2);line(-17,-36,0,-26,'#c9c19b',2);
    for(const [x,y,s] of [[-30,-13,.8],[31,-17,.8],[0,-64,1]]){ctx.save();ctx.translate(x,y);ctx.scale(s,s);poly([[-15,-16],[0,-8],[16,-16],[16,22],[0,31],[-15,22]],'#ddd6b2');poly([[0,-8],[16,-16],[16,22],[0,31]],'#aaa989');poly([[-21,-19],[0,-53],[22,-19],[0,-7]],'#658b73');poly([[0,-53],[22,-19],[0,-7]],'#3c6b55');line(0,-53,0,-62,'#ac935b',2);ellipse(0,-63,3,3,'#dbc282');line(-3,8,-3,16,'#798465',4);ctx.restore();}
    ctx.beginPath();ctx.moveTo(-14,6);ctx.lineTo(-14,-14);ctx.quadraticCurveTo(-7,-27,0,-11);ctx.lineTo(0,14);ctx.fillStyle='#687e61';ctx.fill();line(-9,-11,-9,9,'#adbc8f',1);ellipse(6,-50,7,10,'#ddcd86');poly([[6,-61],[0,-51],[6,-41],[12,-51]],'#efdf9c');poly([[6,-61],[12,-51],[6,-41]],'#c6b571');
    line(1,-126,1,-98,'#7a825b',2);ctx.beginPath();ctx.moveTo(2,-125);ctx.quadraticCurveTo(18,-134,28,-123);ctx.lineTo(28,-110);ctx.quadraticCurveTo(17,-121,2,-112);ctx.closePath();ctx.fillStyle='#d4bb76';ctx.fill();line(7,-117,12,-118,'#f4e4b0',2);ctx.restore();
    label('Forest heart',p.x,p.y+54,'#6d8360');roundRect(p.x-27,p.y+62,54,5,3,'#bdcba5');roundRect(p.x-27,p.y+62,54*(state.health/20),5,3,state.health>7?'#789c61':'#bc8a6c');}
  function label(str,x,y,color){ctx.font='11px "Moss Sans",sans-serif';const w=ctx.measureText(str).width+19;roundRect(x-w/2,y-15,w,23,6,'#eff3e5d9');text(str,x,y,11,color);}
  function drawEnemy(e){const p=project(e.x,e.y),s=e.kind==='boss'?1.55:e.kind==='troll'?1.25:1,bob=Math.sin(e.walk)*1.2;ctx.save();ctx.translate(p.x,p.y);ctx.scale(s,s);ellipse(0,2,14,7,'#59704640');ctx.translate(0,bob);if(e.hit>0){ctx.shadowColor='#fff3cb';ctx.shadowBlur=8;}
    if(e.kind==='slime'){
      ctx.beginPath();ctx.moveTo(-15,0);ctx.bezierCurveTo(-19,-8,-12,-26,0,-27);ctx.bezierCurveTo(14,-26,21,-5,14,0);ctx.quadraticCurveTo(0,10,-15,0);ctx.fillStyle=e.hit>0?'#d3d8a2':'#a3b46a';ctx.fill();ellipse(-4,-19,7,4,'#c4cf8a');ellipse(-5,-10,2,3,'#4c6240');ellipse(6,-10,2,3,'#4c6240');line(-1,-5,2,-5,'#778851',1.3);leaf(2,-28,8,'#778d57',-.7);
    }else{
      const big=e.kind==='troll'||e.kind==='boss';line(-7,-2,-8,5,'#625d41',5);line(6,-2,8,4,'#625d41',5);poly([[-10,-21],[8,-21],[12,-3],[-11,-3]],big?'#8c7460':'#a78b62');line(-10,-15,-16,-6,'#8ba06b',6);line(10,-14,15,-6,'#8ba06b',6);ellipse(0,-28,big?16:13,big?15:12,e.hit>0?'#c7ce96':big?'#91a273':'#9caf74');poly([[-12,-30],[-23,-33],[-13,-22]],'#889e65');poly([[12,-30],[22,-33],[13,-22]],'#7e9560');ellipse(-5,-27,2,2.5,'#415338');ellipse(5,-27,2,2.5,'#415338');line(-3,-21,4,-21,'#5f7149',2);if(big){poly([[-13,-36],[-15,-48],[-6,-39]],'#e1d4ae');poly([[8,-40],[16,-48],[13,-34]],'#e1d4ae');line(-1,-21,-1,-17,'#ede2bf',2);line(5,-21,5,-17,'#ede2bf',2);}else{poly([[-14,-34],[0,-46],[14,-34],[2,-32]],'#b29163');poly([[0,-46],[14,-34],[2,-32]],'#8d7754');}
      line(17,-3,18,-24,'#6e7357',2);poly([[18,-31],[14,-23],[18,-11],[21,-24]],'#d4d8bb');if(e.kind==='boss'){roundRect(-12,-8,24,4,1,'#b59a61');ellipse(0,-7,3,3,'#dfc87e');}
    }
    ctx.restore();if(e.hp<e.maxHp||hover?.enemy===e){const w=27*s;roundRect(p.x-w/2,p.y-44*s,w,4,2,'#63805a66');roundRect(p.x-w/2,p.y-44*s,w*(e.hp/e.maxHp),4,2,e.hp/e.maxHp>.4?'#8caa64':'#c9946b');}}
  function drawProjectiles(){for(const p of state.projectiles){if(p.type==='magic'){ctx.save();ctx.shadowColor='#bdabe0';ctx.shadowBlur=13;ellipse(p.x,p.y,5,5,'#ddcef6');ctx.restore();ellipse(p.x-3,p.y+3,2,2,'#a692c7');}else{const target=project(p.target.x,p.target.y),ang=Math.atan2(target.y-17-p.y,target.x-p.x);ctx.save();ctx.translate(p.x,p.y);ctx.rotate(ang);line(-10,0,4,0,'#815f3d',2);poly([[7,0],[1,-3],[1,3]],'#e8dfb9');line(-9,0,-13,-3,'#d4c596',2);line(-9,0,-13,3,'#d4c596',2);ctx.restore();}}}
  function render(){
    ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,canvas.width,canvas.height);ctx.setTransform(view.scale,0,0,view.scale,view.x,view.y);drawBackground();drawGround();
    const selected=state.selectedTower||hover?.tower;if(selected)drawRange(selected);else if(hover&&!hover.tower&&hover.id!==undefined)drawRange({...hover,type:state.selectedType,level:1});
    state.pads.filter(p=>!p.tower).forEach(drawPad);
    const objects=[...decorations.map(d=>({depth:d.x+d.y,kind:d.kind,data:d})),...state.pads.filter(p=>p.tower).map(p=>({depth:p.x+p.y,kind:'tower',data:p.tower})),...state.enemies.map(e=>({depth:e.x+e.y+.08,kind:'enemy',data:e})),{depth:6.7,kind:'portal'},{depth:13,kind:'castle'}];
    objects.sort((a,b)=>a.depth-b.depth);for(const o of objects){switch(o.kind){case'tree':case'pine':drawTree(o.data);break;case'bush':drawBush(o.data);break;case'rock':drawRock(o.data);break;case'pond':drawPond(o.data);break;case'ruin':drawRuin(o.data);break;case'tower':drawTower(o.data);break;case'enemy':drawEnemy(o.data);break;case'portal':drawPortal();break;case'castle':drawCastle();}}
    drawProjectiles();for(const p of state.particles){ctx.globalAlpha=Math.min(1,p.life/p.maxLife*2);if(p.text)text(p.text,p.x,p.y,14,p.color);else diamond(p.x,p.y,p.size,p.size,p.color);}ctx.globalAlpha=1;
    // Tiny fireflies give the still forest a little life.
    for(let i=0;i<7;i++){const x=300+rand(i,4)*660+Math.sin(visualTime*.5+i)*13,y=205+rand(i,6)*350+Math.cos(visualTime*.7+i)*8;ctx.globalAlpha=.3+Math.sin(visualTime*1.6+i)*.2;ellipse(x,y,2,2,'#f7f1c7');}ctx.globalAlpha=1;
  }
  function resize(){const rect=canvas.getBoundingClientRect(),dpr=Math.min(window.devicePixelRatio||1,2);canvas.width=Math.round(rect.width*dpr);canvas.height=Math.round(rect.height*dpr);const scale=Math.min(rect.width/W,rect.height/H);view={scale:scale*dpr,x:(rect.width-W*scale)/2*dpr,y:(rect.height-H*scale)/2*dpr,dpr,cssScale:scale};render();}
  function pointerPosition(event){const rect=canvas.getBoundingClientRect();return {x:((event.clientX-rect.left)*view.dpr-view.x)/view.scale,y:((event.clientY-rect.top)*view.dpr-view.y)/view.scale};}
  function hitPad(point){let hit=null,best=Infinity;for(const pad of state.pads){const p=project(pad.x,pad.y),dx=(point.x-p.x)/34,dy=(point.y-p.y)/20;const d=dx*dx+dy*dy;if(d<=1.2&&d<best){hit=pad;best=d;}else if(pad.tower&&Math.abs(point.x-p.x)<25&&point.y<p.y&&point.y>p.y-97){if(2<best){hit=pad;best=2;}}}return hit;}
  canvas.addEventListener('pointermove',event=>{hover=hitPad(pointerPosition(event));canvas.style.cursor=hover?'pointer':'default';});canvas.addEventListener('pointerleave',()=>{hover=null;canvas.style.cursor='default';});
  canvas.addEventListener('click',event=>{if(state.phase==='won'||state.phase==='lost')return;const pad=hitPad(pointerPosition(event));if(pad)build(pad);else if(state.selectedTower){state.selectedTower=null;updateUI();}});
  document.querySelectorAll('[data-tower]').forEach(button=>button.addEventListener('click',()=>selectType(button.dataset.tower)));
  $('startWave').addEventListener('click',startWave);$('upgradeButton').addEventListener('click',upgrade);
  $('closeUpgrade').addEventListener('click',()=>{state.selectedTower=null;updateUI();});$('backBuild').addEventListener('click',()=>{state.selectedTower=null;updateUI();});
  $('pauseButton').addEventListener('click',()=>{if(state.phase==='battle'){state.paused=!state.paused;updateUI();}});
  $('speedButton').addEventListener('click',()=>{state.speed=state.speed===1?2:1;updateUI();});
  $('soundButton').addEventListener('click',()=>{sound=!sound;$('soundButton').innerHTML=`<svg class="icon"><use href="#i-${sound?'sound':'mute'}"/></svg>`;$('soundButton').title=sound?'Mute sound':'Enable sound';$('soundButton').setAttribute('aria-label',$('soundButton').title);if(sound)playSound('build');});
  $('restartButton').addEventListener('click',()=>{reset();toast('A new dawn · Initial state restored');});$('endRestart').addEventListener('click',reset);
  $('helpButton').addEventListener('click',()=>{if(state.phase==='battle'&&!state.paused){state.paused=true;updateUI();}$('helpDialog').showModal();});$('closeHelp').addEventListener('click',()=>$('helpDialog').close());$('helpDone').addEventListener('click',()=>$('helpDialog').close());$('helpDialog').addEventListener('click',event=>{if(event.target===$('helpDialog')){const r=$('helpDialog').getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)$('helpDialog').close();}});
  new ResizeObserver(resize).observe(canvas);reset();resize();
  function frame(time){const dt=Math.min((time-lastTime)/1000||0,.06);lastTime=time;visualTime+=dt;update(dt*state.speed);render();requestAnimationFrame(frame);}requestAnimationFrame(frame);
  // An opt-in inspection interface for local browser checks; absent in ordinary play.
  if(new URLSearchParams(location.search).has('test'))window.__mosswatch={get state(){return state;},types,routeLength,reset,startWave,selectType,build:id=>build(state.pads[id]),upgrade,step:seconds=>{for(let i=0;i<Math.ceil(seconds*60);i++)update(1/60);render();},point:id=>{const p=project(state.pads[id].x,state.pads[id].y),r=canvas.getBoundingClientRect();return {x:r.left+(p.x*view.scale+view.x)/view.dpr,y:r.top+(p.y*view.scale+view.y)/view.dpr};}};
})();
