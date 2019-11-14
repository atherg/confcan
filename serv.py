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
    # if win != 0 and (winner1 != 0 or winner2 != 0):
        # return 'Smth not right. Double win?'
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
    return web.Response(text=json.dumps(responseObj))

async def checkboard(request):
    try:
        n,m = 6,7 #as defined
        winner1 = 0
        winner2 = 0
        rawData = json.loads(request.query['data'])
        board = np.array(rawData['board'])
        print(board)

        #check board size
        if board.shape != (n,m):
            print('Board size sucks.', board.shape)
            responseObj = {'status' : 'fail', 'desc': 'Board shape is weird '+str(board.shape) }
            return web.Response(text=json.dumps(responseObj), status=418)

        #check elements
        unique, counts = np.unique(board, return_counts=True)
        elementsDict = dict(zip(unique, counts))
        countCheck0 = elementsDict[0] if 0 in elementsDict else 0
        countCheck1 = elementsDict[1] if 1 in elementsDict else 0
        countCheck2 = elementsDict[2] if 2 in elementsDict else 0
        if sum(counts) != countCheck0 + countCheck1 + countCheck2:
            print('Elements have something weird.', unique)
            responseObj = {'status' : 'fail', 'desc': 'Elements have something weired '+str(unique) }
            return web.Response(text=json.dumps(responseObj), status=418)          
        if countCheck1 == countCheck2 or countCheck1 == countCheck2+1:
            pass
        else:
            print('Black and Red checks are not matched', countCheck1, countCheck2)
            responseObj = {'status' : 'fail', 'desc': 'Black and Red checks are not matched', 'Black': str(countCheck1), 'Red': str(countCheck2)}
            return web.Response(text=json.dumps(responseObj), status=418)  

        for i in range(max(m,n)):
            if i<len(board):
                win = check_winner(list(board[i]))
                winner1, winner2 = get_win_status(win, winner1, winner2)
                
            if i<len(board[0]):
                #make sure that elemnts order in columns is correct
                columnToLst = column(board,i)
                colIndex = [index for index, value in enumerate(columnToLst) if value == 0]
                for i in range(len(colIndex)):
                    if columnToLst[i] != 0: 
                        print('board is not consistant. Checkers are flying in the air')
                        responseObj = {'status' : 'fail', 'desc': 'board is not consistant. Checkers are flying in the air'}
                        return web.Response(text=json.dumps(responseObj), status=418)  
                    
                win = check_winner(columnToLst)
                winner1, winner2 = get_win_status(win, winner1, winner2)

        #diagonales
        diags = [board[::-1,:].diagonal(i) for i in range(-board.shape[0]+1,board.shape[1])]
        diags.extend(board.diagonal(i) for i in range(board.shape[1]-1,-board.shape[0],-1))
        allDiags = [n.tolist() for n in diags if len(n) >= 4]
        for aDiag in allDiags:
            win = check_winner(aDiag)
            winner1, winner2 = get_win_status(win, winner1, winner2)
     
        if winner1 !=0 or winner2 !=0:
            responseObj = {'status' : 'success', 'desc': 'Final score', 'Black': winner1, 'Red': winner2}
        elif countCheck0 == 0:
            responseObj = {'status' : 'success', 'desc': 'Game over. Tie - no empty places to move'}
        elif countCheck1 == countCheck2:
            responseObj = {'status' : 'success', 'desc': 'Game is on. Black\'s turn.'}
        elif countCheck1 == countCheck2+1:
            responseObj = {'status' : 'success', 'desc': 'Game is on. Red\'s turn.'}
        else:
            responseObj = {'status' : 'fail', 'desc': 'Unknown status, let devs know.'}
            return web.Response(text=json.dumps(responseObj), status=418)
        return web.Response(text=json.dumps(responseObj), status=200)

    except Exception as e:
        responseObj = {'status' : 'fail', 'reason': str(e) }
        return web.Response(text=json.dumps(responseObj), status=500)    


def main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_post('/evaluate_board_state', checkboard)

    web.run_app(app)

if __name__ == "__main__":
    main()

