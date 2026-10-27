"""Public-game-derived deterministic tower-defense strategy experiment.

Research prototype, not yet an accepted Harbor Task. Observations expose visible
battleboard and upcoming-wave summaries, never hidden scenario IDs or RNG state.
"""
from pathlib import Path
import argparse,json,random,re,time,subprocess,selectors,select,os,signal,hashlib,sys,ast
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
WAVES=12; MAX_ACTIONS=72; CASE_SECONDS=30
TYPES={'arrow':{'cost':60,'damage':[14,25,42],'range':[2.65,3.05,3.5],'interval':[.60,.52,.43],'upgrades':[55,85]},'magic':{'cost':90,'damage':[23,40,65],'range':[2.4,2.85,3.2],'interval':[1.15,1.03,.92],'upgrades':[75,115]}}
ROUTES=[
[{'x':-.8,'y':7},{'x':3,'y':7},{'x':3,'y':3},{'x':7,'y':3},{'x':7,'y':6},{'x':10,'y':6},{'x':10,'y':2},{'x':11,'y':2}],
[{'x':-.8,'y':7},{'x':2,'y':7},{'x':2,'y':2},{'x':5,'y':2},{'x':5,'y':8},{'x':8,'y':8},{'x':8,'y':2},{'x':11,'y':2}]]

def scenario(seed, pressure=2.0):
 r=random.Random(seed);route=ROUTES[seed%2];road=set()
 for a,b in zip(route,route[1:]):
  n=int(abs(a['x']-b['x'])+abs(a['y']-b['y']))+2
  for i in range(n+1):road.add((round(a['x']+(b['x']-a['x'])*i/n),round(a['y']+(b['y']-a['y'])*i/n)))
 pads=[(x,y) for x in range(1,11) for y in range(1,9) if (x,y) not in road and any(abs(x-a)+abs(y-b)<=2 for a,b in road)]
 r.shuffle(pads);pads=pads[:16];waves=[]
 for w in range(WAVES):
  wave=[];theme=r.choice(['swarm','armor','ward','mixed'])
  for i in range(9+w):
   armor=(theme=='armor' or (theme=='mixed' and i%3==0));ward=(theme=='ward' or (theme=='mixed' and i%3==1));boss=i==8+w and w%3==2
   hp=(38*(1+.30*w)**1.65)*(2.8 if boss else .85 if theme=='swarm' else 1.0)*pressure*r.uniform(.92,1.08)
   wave.append({'kind':'boss' if boss else 'troll' if armor else 'goblin' if ward else 'slime','hp':round(hp,2),'speed':(.82 if boss else 1.20 if theme=='swarm' else 1.02)*r.uniform(.94,1.06),'reward':12 if boss else 7,'damage':4 if boss else 1,'armor':.62 if armor else .08,'ward':.62 if ward else .08})
  waves.append(wave)
 return {'route':route,'pads':pads,'waves':waves,'gold':150,'health':24,'pressure':pressure,'total_threat':sum(e['damage'] for wave in waves for e in wave)}

def replace_once(s,old,new):
 if s.count(old)!=1:raise ValueError('Public game adaptation anchor mismatch: '+old[:70])
 return s.replace(old,new,1)

HOOK=r'''
const originalUI=updateUI;
let measuredKills=0, measuredThreat=0, stepCount=0;
const originalHurt=hurt;
hurt=function(enemy,amount){const alive=!enemy.dead;originalHurt(enemy,amount);if(alive&&enemy.dead){measuredKills++;measuredThreat+=enemy.damage;}};
document.getElementById('waveTrack').innerHTML=waves.map((w,i)=>`<div class="wave-step"><span>${i+1}</span><small>Wave ${i+1}</small></div>`).join('');
window.__td={
 observe(){
  const o={gold:state.gold,health:state.health,phase:state.phase,completed_waves:state.completed,wave_count:waves.length,
    actions_remaining:72-stepCount,route,pads:state.pads.map(p=>({id:p.id,x:p.x,y:p.y,tower:p.tower?{type:p.tower.type,level:p.tower.level}:null})),
    tower_types:types,upcoming:waves.slice(state.completed,Math.min(waves.length,state.completed+2)).map(w=>({count:w.length,mean_hp:Math.round(w.reduce((s,e)=>s+e.hp,0)/w.length*100)/100,mean_speed:Math.round(w.reduce((s,e)=>s+e.speed,0)/w.length*100)/100,physical_resistance:Math.round(w.reduce((s,e)=>s+e.armor,0)/w.length*100)/100,magic_resistance:Math.round(w.reduce((s,e)=>s+e.ward,0)/w.length*100)/100,total_threat:w.reduce((s,e)=>s+e.damage,0)}))};
  let panel=document.getElementById('campaign-readout');
  if(!panel){panel=document.createElement('section');panel.id='campaign-readout';panel.style.cssText='padding:16px;white-space:pre-wrap;font:12px monospace;background:#f4f6ec';document.body.appendChild(panel);}
  panel.textContent='Campaign planning board — visible information\n'+JSON.stringify(o,null,2);
  return o;
 },
 act(command){
  if(state.phase!=='ready')throw Error('Only between-wave planning is allowed');
  if(!command||Object.keys(command).sort().join(',')!=='actions,start_wave'||!Array.isArray(command.actions)||command.actions.length>8||command.start_wave!==true)throw Error('Emit {actions:[...at most 8],start_wave:true}');
  for(const a of command.actions){
   if(stepCount>=72)throw Error('72 build/upgrade actions exceeded');
   const p=state.pads.find(p=>p.id===a.pad);if(!p)throw Error('Unknown build site');
   if(a.type==='build'){
    if(Object.keys(a).sort().join(',')!=='kind,pad,type'||p.tower||!types[a.kind]||state.gold<types[a.kind].cost)throw Error('Invalid or unaffordable build');
    selectType(a.kind);build(p);
   }else if(a.type==='upgrade'){
    if(Object.keys(a).sort().join(',')!=='pad,type'||!p.tower||p.tower.level>=3||state.gold<types[p.tower.type].upgrades[p.tower.level-1])throw Error('Invalid or unaffordable upgrade');
    state.selectedTower=p.tower;upgrade();
   }else if(a.type==='sell'){
    if(Object.keys(a).sort().join(',')!=='pad,type'||!p.tower)throw Error('Invalid sale');
    const t=p.tower,c=types[t.type];const invested=c.cost+c.upgrades.slice(0,t.level-1).reduce((a,b)=>a+b,0);
    state.gold+=Math.floor(invested*.55);p.tower=null;state.selectedTower=null;originalUI();
   }else throw Error('Unknown command');
   stepCount++;
  }
  startWave();let ticks=0;updateUI=()=>{};
  while(state.phase==='battle'&&ticks++<18000){update(1/30);state.particles=[];}
  updateUI=originalUI;if(state.phase==='battle')throw Error('Wave simulation incomplete');
  originalUI();render();return this.observe();
 },
 result(){return {intercepted_threat:measuredThreat,total_threat:window.__scenario.total_threat,kills:measuredKills,completed_waves:state.completed,health:state.health,phase:state.phase,actions:stepCount};}
};
'''

def document(config):
 s=(ROOT/'assets/game.js').read_text();s=re.sub(r'  const route = .*?;\n','  const route = window.__scenario.route;\n',s,count=1)
 s=re.sub(r'  const padPositions = .*?;\n','  const padPositions = window.__scenario.pads;\n',s,count=1)
 a=s.index('  const waves=[');b=s.index('  function rand',a);s=s[:a]+'  const waves=window.__scenario.waves;\n'+s[b:]
 s=replace_once(s,'health:20,gold:180','health:window.__scenario.health,gold:window.__scenario.gold')
 s=s.replace('+30 gold','+14 gold').replace(' / 20',' / '+str(config['health']))
 s=s.replace('state.wave===3','state.wave===waves.length').replace('Math.min(3,state.wave+1)','Math.min(waves.length,state.wave+1)').replace('Math.min(state.wave,2)','Math.min(state.wave,waves.length-1)').replace("state.gold+=30","state.gold+=14").replace('Three waves defeated.','Campaign waves defeated.').replace("'3 waves'","`${waves.length} waves`")
 s=s.replace("hurt(e,p.damage);burst", "hurt(e,p.damage*(1-e.ward));burst").replace('else hurt(p.target,p.damage);','else hurt(p.target,p.damage*(1-p.target.armor));')
 s=replace_once(s,'  function frame(time)',HOOK+'\n  function frame(time)')
 # Freeze autonomous rendering/time; actions advance the original combat engine at 30 Hz.
 setup='window.__scenario='+json.dumps(config,separators=(',',':'))+';window.requestAnimationFrame=()=>0;'
 html=(ROOT/'assets/index.html').read_text();css=(ROOT/'assets/style.css').read_text();css=re.sub(r'@font-face\s*\{[^}]*\}','',css)
 html=re.sub(r'<link[^>]*href="style.css"[^>]*>','<style>'+css+'</style>',html)
 html=re.sub(r'<script[^>]*src="game.js"[^>]*></script>',lambda m:'<script>'+setup+s+'</script>',html)
 return html

class Game:
 def __init__(self,browser,seed,pressure=2):
  self.context=browser.new_context(viewport={'width':1440,'height':1100},service_workers='block');self.context.route('**/*',lambda route:route.abort());self.page=self.context.new_page();self.page.set_content(document(scenario(seed,pressure)));self.page.wait_for_function('window.__td!==undefined')
 def observe(self):return self.page.evaluate('window.__td.observe()')
 def act(self,action):return self.page.evaluate('a=>window.__td.act(a)',action)
 def result(self):return self.page.evaluate('window.__td.result()')
 def close(self):self.context.close()

def validate_source(policy):
 tree=ast.parse(policy.read_bytes())
 permitted={'sys','json','math','random','itertools','collections','heapq','functools','bisect','statistics','copy','array','operator','time'}
 denied={'open','exec','eval','compile','__import__','getattr','setattr','delattr','globals','locals','vars','dir','input','breakpoint'}
 for n in ast.walk(tree):
  if isinstance(n,ast.Import) and any(x.name.split('.')[0] not in permitted for x in n.names):raise ValueError('Policy imports must be permitted standard-library computation only')
  if isinstance(n,ast.ImportFrom) and (n.level or (n.module or '').split('.')[0] not in permitted):raise ValueError('Policy imports must be permitted standard-library computation only')
  if isinstance(n,ast.Attribute) and (n.attr.startswith('__') or n.attr in {'modules','path','argv','environ','system','popen','open','read_bytes','read_text','write_text','write_bytes'}):raise ValueError('Filesystem/environment/interpreter access prohibited')
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in denied:raise ValueError('Dynamic access prohibited')


def evaluate(policy,seeds,pressure=2,output=None,verbose=True):
 validate_source(policy);rows=[];begin=time.monotonic()
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--disable-dev-shm-usage'])
  try:
   for seed in seeds:
    g=None;proc=None;start=time.monotonic();row={'seed':seed}
    try:
     g=Game(browser,seed,pressure);proc=subprocess.Popen([sys.executable,'-I','-B',str(policy.resolve())],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,bufsize=0);selector=selectors.DefaultSelector();selector.register(proc.stdout,selectors.EVENT_READ);os.set_blocking(proc.stdin.fileno(),False);obs=g.observe();buffer=b''
     for wave in range(WAVES):
      payload=(json.dumps({'observation':obs})+'\n').encode()
      while payload:
       remaining=CASE_SECONDS-(time.monotonic()-start)
       if remaining<=0 or not select.select([], [proc.stdin], [], remaining)[1]:raise TimeoutError('Policy input deadline exceeded')
       try:n=os.write(proc.stdin.fileno(),payload)
       except BlockingIOError:continue
       payload=payload[n:]
      while b'\n' not in buffer:
       remaining=CASE_SECONDS-(time.monotonic()-start)
       if remaining<=0 or not selector.select(remaining):raise TimeoutError('Candidate exceeded per-case deadline')
       chunk=os.read(proc.stdout.fileno(),65536)
       if not chunk:raise ValueError('Policy exited before completing campaign')
       buffer+=chunk
       if len(buffer)>65536:raise ValueError('Policy output exceeds 64 KiB')
      line,buffer=buffer.split(b'\n',1);action=json.loads(line);obs=g.act(action)
      if obs['phase'] in ('won','lost'):break
     outcome=g.result();assert time.monotonic()-start<=CASE_SECONDS,'Per-case wall deadline exceeded';assert outcome['phase'] in ('won','lost');row.update(outcome);row['score']=outcome['intercepted_threat']/outcome['total_threat'];row['error']=None
    except Exception as e:row.update(score=None,error=type(e).__name__+': '+str(e)[:500])
    finally:
     if proc:
      try:os.killpg(proc.pid,signal.SIGKILL)
      except ProcessLookupError:pass
      proc.wait();selector.close()
     if g:g.close()
    row['seconds']=round(time.monotonic()-start,3);rows.append(row)
    if output:output.write_text(json.dumps({'status':'in_progress','rows':rows},indent=2)+'\n')
    if verbose:print(json.dumps(row),flush=True)
  finally:browser.close()
 success=all(r['error'] is None for r in rows);result={'status':'scored' if success else 'invalid','score':sum(r['score'] for r in rows)/len(rows) if success else None,'cases':len(rows),'rows':rows,'seconds':round(time.monotonic()-begin,3),'policy_sha256':hashlib.sha256(policy.read_bytes()).hexdigest(),'metric':'mean threat-weighted enemy interception rate; future unspawned enemies receive zero credit'}
 if output:output.write_text(json.dumps(result,indent=2)+'\n')
 return result

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--policy',type=Path,required=True);a.add_argument('--seeds',type=int,nargs='+',required=True);a.add_argument('--pressure',type=float,default=2);a.add_argument('--output',type=Path,required=True);args=a.parse_args();print(json.dumps(evaluate(args.policy,args.seeds,args.pressure,args.output)));sys.exit(0 if json.loads(args.output.read_text())['status']=='scored' else 1)
