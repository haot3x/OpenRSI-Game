"""Deterministic authoring search: solvability, never control-policy scores."""
import random, json, collections, time
SHAPES={
'I':[[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
'J':[[1,0,0],[1,1,1],[0,0,0]],'L':[[0,0,1],[1,1,1],[0,0,0]],
'O':[[1,1],[1,1]],'S':[[0,1,1],[1,1,0],[0,0,0]],
'T':[[0,1,0],[1,1,1],[0,0,0]],'Z':[[1,1,0],[0,1,1],[0,0,0]]}
ROTS={}
for typ,initial in SHAPES.items():
 m=initial;ROTS[typ]=[]
 for _ in range(4):
  ROTS[typ].append(tuple((x,y) for y,row in enumerate(m) for x,v in enumerate(row) if v))
  m=[list(row) for row in zip(*m[::-1])]

def sequence(family,seed,count=8):
 state=seed;out=[]
 order=list('IJLOSTZ') if family=='a' else list('IOTSZJL')
 while len(out)<count:
  bag=order[:]
  for i in range(6,0,-1):
   state=(1664525*state+1013904223)&0xffffffff
   j=int(state/2**32*(i+1));bag[i],bag[j]=bag[j],bag[i]
  out.extend(bag[::-1] if family=='a' else bag)
 return out[:count]

def fits(board,typ,r,x,y):
 return all(0<=x+dx<10 and y+dy<20 and (y+dy<0 or not board[y+dy]>> (x+dx)&1) for dx,dy in ROTS[typ][r])

def placements(board,typ,family,tuck=False):
 start=(0,(10-len(SHAPES[typ]))//2,0 if family=='a' else -1)
 q=collections.deque([(start,())]);seen={start};landings={}
 while q:
  (r,x,y),path=q.popleft()
  if not fits(board,typ,r,x,y):continue
  drop=y
  while fits(board,typ,r,x,drop+1):drop+=1
  cells=tuple(sorted((x+dx,drop+dy) for dx,dy in ROTS[typ][r]))
  if min(cy for cx,cy in cells)>=0:
   nxt=list(board)
   for cx,cy in cells:nxt[cy]|=1<<cx
   full=sum(row==1023 for row in nxt)
   landing=(tuple(nxt),full,path+('Space',))
   if cells not in landings or len(landing[2])<len(landings[cells][2]):landings[cells]=landing
  moves=[(r,x-1,y,'ArrowLeft'),(r,x+1,y,'ArrowRight')]
  if tuck:moves.append((r,x,y+1,'ArrowDown'))
  nr=(r+1)%4
  if typ!='O':
   kicks=((0,0),(-1,0),(1,0),(-2,0),(2,0),(0,-1),(-1,-1),(1,-1),(0,-2)) if family=='a' else ((0,0),(-1,0),(1,0),(-2,0),(2,0))
   for dx,dy in kicks:
    if fits(board,typ,nr,x+dx,y+dy):
     moves.append((nr,x+dx,y+dy,'ArrowUp'));break
  for nr,nx,ny,key in moves:
   s=(nr,nx,ny)
   if s not in seen and len(path)<29 and fits(board,typ,nr,nx,ny):
    seen.add(s);q.append((s,path+(key,)))
 return list(landings.values())

def quality(board):
 heights=[20-next((y for y in range(20) if board[y]>>x&1),20) for x in range(10)]
 holes=sum(sum(not board[y]>>x&1 for y in range(20-heights[x],20)) for x in range(10))
 # Authoring search prioritizes progressing near-complete rows and few holes.
 near=sum((bin(row).count("1")/10)**8 for row in board)
 return near*12-holes*2-sum(heights)*.22-sum(abs(a-b) for a,b in zip(heights,heights[1:]))*.5

def solve(board,seq,family,tuck,beam=24):
 nodes=[(tuple(board),('Enter',))]
 for depth,typ in enumerate(seq[:5]):
  choices={}
  for b,path in nodes:
   for nb,full,step in placements(b,typ,family,tuck):
    np=path+step
    if len(np)>32:continue
    if full:return list(np)
    if nb not in choices or len(np)<len(choices[nb]):choices[nb]=np
  nodes=sorted(choices.items(),key=lambda item:quality(item[0]),reverse=True)[:beam]
  if not nodes:return None
 return None

def raw_board(kind,rng):
 b=[0]*20
 if kind in ('staggered','uneven'):
  width=rng.choice((7,8,9));left=rng.randrange(11-width)
  h=rng.choice((4,5,6,7))
  for x in range(10):
   height=h if not left<=x<left+width else rng.randrange(0,3)
   for y in range(20-height,20):b[y]|=1<<x
 elif kind=='separated':
  # Isolated floor gaps interspersed with short stacks, still open from above.
  gaps=set(range(rng.randrange(2),10,2))
  for x in range(10):
   if x not in gaps:
    for y in range(20-rng.choice((2,3,4,5,6)),20):b[y]|=1<<x
 else:
  # A roof covers floor holes; its lateral shaft stays open. Natural entry
  # requires descending before a horizontal move for some placements.
  left=rng.randrange(0,5);width=rng.choice((4,5,6));width=min(width,10-left)
  for y in range(16,20):
   for x in range(10):
    if not left<=x<left+width:b[y]|=1<<x
  roof=rng.choice((16,17));cover=rng.choice((1,2))
  if rng.randrange(2):
   for x in range(left,left+cover):b[roof]|=1<<x
  else:
   for x in range(left+width-cover,left+width):b[roof]|=1<<x
 return b

def overhang_board(family, seed):
 # A sparse roof over an indispensable floor gap avoids the old near-full
 # roof shortcut. The first natural bag piece fits after down-then-sideways.
 seq = sequence(family, seed)
 cells = ROTS[seq[0]][0]
 maxx = max(x for x,y in cells); maxy = max(y for x,y in cells)
 right = bool(random.Random(seed*103+ord(family)*17).randrange(2))
 target = 9-maxx if right else 0
 floor_gaps = [target+x for x,y in cells if y==maxy]
 roof_col = max(floor_gaps) if right else min(floor_gaps)
 entry = roof_col-1-maxx if right else roof_col+1-min(x for x,y in cells)
 board = [0]*20
 board[19] = 1023-sum(1<<x for x in floor_gaps)
 board[16] = 1<<roof_col
 spawn_x = (10-len(SHAPES[seq[0]]))//2
 spawn_y = 0 if family=='a' else -1
 shift = entry-spawn_x
 path = ['Enter'] + [('ArrowRight' if shift>0 else 'ArrowLeft')]*abs(shift)
 path += ['ArrowDown']*(18-maxy-spawn_y)
 path += ['ArrowRight' if target>entry else 'ArrowLeft']*abs(target-entry) + ['Space']
 assert len(path)<=32
 # The same placement made from above must be blocked by the sparse roof.
 assert not any(full for nb,full,step in placements(board,seq[0],family,False))
 return {'family':family,'seed':seed,'structure':'overhang','attempt':0,
         'board':[['J' if row>>x&1 else None for x in range(10)] for row in board],
         'witness':[{'key':key} for key in path],'sequence':seq,
         'witness_actions':len(path)}

def generate(family,seed,kind):
 if kind=='overhang':return overhang_board(family,seed)
 rng=random.Random(seed*103+ord(family)*17)
 seq=sequence(family,seed)
 for attempt in range(400):
  board=raw_board(kind,rng)
  if any(r==1023 for r in board):continue
  # Avoid fixtures that already expose a one-piece clear to the current bag.
  if any(full for nb,full,step in placements(board,seq[0],family,False)):continue
  path=solve(board,seq,family,kind=='overhang',beam=18)
  minimum_pieces = 3 if kind=='staggered' else 4
  if path and path.count('Space')>=minimum_pieces:
   return {'family':family,'seed':seed,'structure':kind,'attempt':attempt,'board':[["J" if row>>x&1 else None for x in range(10)] for row in board],'witness':[{'key':key} for key in path],'sequence':seq,'witness_actions':len(path),'witness_pieces':path.count('Space')}
 raise RuntimeError(f'No reachable fixture for {family}/{seed}/{kind}')

if __name__=='__main__':
 import argparse
 from pathlib import Path
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--family',default='ab');p.add_argument('--split',choices=('dev','judge'),default='dev');a=p.parse_args()
 records=[];begin=time.monotonic()
 for family in a.family:
  for k,kind in enumerate(('staggered','separated','overhang','uneven')):
   for i in range(a.count):
    seed=(10 if a.split=='dev' else 100)+k*a.count+i
    row=generate(family,seed,kind);records.append(row)
    print(f"{family}/{seed}/{kind}: actions={row['witness_actions']} attempts={row['attempt']} seconds={time.monotonic()-begin:.1f}",flush=True)
 Path(a.output).write_text(json.dumps({'algorithm':'board-only deterministic feasibility search; no policy-control feedback','split':a.split,'records':records},indent=2)+'\n')
