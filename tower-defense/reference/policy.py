"""Fixed geometric-coverage greedy reference; public tower/price rules only."""
import sys,json,math

def coverage(pad,route,radius):
 total=0
 for a,b in zip(route,route[1:]):
  n=max(1,int(math.hypot(b['x']-a['x'],b['y']-a['y'])*5))
  total+=sum(math.hypot(pad['x']-(a['x']+(b['x']-a['x'])*i/n),pad['y']-(a['y']+(b['y']-a['y'])*i/n))<=radius for i in range(n+1))/5
 return total
for line in sys.stdin:
 o=json.loads(line)['observation'];gold=o['gold'];pads=o['pads'];types=o['tower_types'];actions=[]
 for _ in range(min(8,o['actions_remaining'])):
  choices=[]
  for p in pads:
   if p['tower'] is None:
    kind='arrow';c=types[kind];price=c['cost'];value=coverage(p,o['route'],c['range'][0])*c['damage'][0]/c['interval'][0]/price
    if price<=gold:choices.append((value,p['id'],'build',kind,price))
   else:
    t=p['tower'];c=types[t['type']];level=t['level'];price=c['upgrades'][level-1] if level<3 else 10**9
    if price<=gold:
     gain=coverage(p,o['route'],c['range'][level])*c['damage'][level]/c['interval'][level]-coverage(p,o['route'],c['range'][level-1])*c['damage'][level-1]/c['interval'][level-1]
     choices.append((gain/price,p['id'],'upgrade',t['type'],price))
  if not choices:break
  value,pad,action,kind,price=max(choices);gold-=price;p=next(p for p in pads if p['id']==pad)
  if action=='build':actions.append({'type':'build','pad':pad,'kind':kind});p['tower']={'type':kind,'level':1}
  else:actions.append({'type':'upgrade','pad':pad});p['tower']['level']+=1
 print(json.dumps({'actions':actions,'start_wave':True}),flush=True)
