from aiohttp import web
import json
import numpy as np
from itertools import groupby

def check_winner(lst):
    grp = {}
    flag = 0
    if lst.count(1) >= 4:
        groups = groupby(lst)
        tup_to_dict([(label, sum(1 for _ in group)) for label, group in groups], grp)
        for grpsz in grp[1]:
            if grpsz >= 4:
                flag = flag + 1
    if lst.count(2) >= 4:
        groups = groupby(lst)
        tup_to_dict([(label, sum(2 for _ in group)) for label, group in groups], grp)
        for grpsz in grp[2]:
            if grpsz >= 4:
                flag = flag + 2
    return flag

def get_win_status(win, winner1, winner2):
    if winner1 == 0 and winner2 == 0:
        if win == 3:
            winner1 = 0.5
            winner2 = 0.5
        elif win == 2:
            winner1 = 0
            winner2 = 1
        elif win == 1:
            winner1 = 1
            winner2 = 0
    return winner1, winner2
    
  
def tup_to_dict(tup, di): 
    for a, b in tup: 
        di.setdefault(a, []).append(b) 
    return di 

def column(matrix, i):
    return [row[i] for row in matrix]    

async def handle(request):
    responseObj = {'status' : 'success'}
    return web.Response(text=json.dumps(response_obj))

async def checkboard(request):
    try:
        n,m = 6,7 #as defined
        winner1 = 0
        winner2 = 0
        rawData = json.loads(request.query['data'])
        board = np.array(rawData['board'])
        print(board)

        if board.shape != (n,m):
            print('Board size sucks.', board.shape)
            responseObj = {'status' : 'failed', 'Board shape is weird': board.shape }
            return web.Response(text=json.dumps(responseObj), status=418)

        unique, counts = np.unique(board, return_counts=True)
        sanity = 0
        if 1 in unique:
            sanity += 1
        if 2 in unique:
            sanity += 1
        if 0 in unique:
            sanity += 1
        if sanity != len(unique):
            print('Elements have something weird.', unique)
            responseObj = {'status' : 'failed', 'Elements have something weired': unique }
            return web.Response(text=json.dumps(responseObj), status=418)          
        #TODO. Implement elements consistancy check. Make sure it's only 0,1,2

        for i in range(max(m,n)):
            if i<len(board):
                win = check_winner(list(board[i]))
                winner1, winner2 = get_win_status(win, winner1, winner2)
                
            if i<len(board[0]):
                win = check_winner(column(board,i))
                winner1, winner2 = get_win_status(win, winner1, winner2)

        #diagonales
        diags = [board[::-1,:].diagonal(i) for i in range(-board.shape[0]+1,board.shape[1])]
        diags.extend(board.diagonal(i) for i in range(board.shape[1]-1,-board.shape[0],-1))
        win = check_winner([n.tolist() for n in diags if len(n) >= 4])
        winner1, winner2 = get_win_status(win, winner1, winner2)
     
        responseObj = {'status' : 'success', 'Black': winner1, 'Red': winner2}
        return web.Response(text=json.dumps(responseObj), status=200)

    except Exception as e:
        responseObj = {'status' : 'failed', 'reason': str(e) }
        return web.Response(text=json.dumps(responseObj), status=500)    


def main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_post('/evaluate_board_state', checkboard)

    web.run_app(app)

if __name__ == "__main__":
    main()

