import sys
from multiprocessing import Pool as ThreadPool
from datetime import datetime
from temperature import tempControl
from tqdm import tqdm

_num_queens = 12    # default number of queens
_num_thread = 4     # default number of threads
_its_safe = 0       # queen on a safe position
_not_safe = 1       # queen not safe

    
class nQueen():
    
    def __init__(self, queens=_num_queens, threads=_num_thread):
        self._nthreads = threads
        self._nq = queens
        
        self._queen_on = x = [[0 for i in range(self._nq )] for j in range(self._nq)]
        self._solution = 0
        self._solutions = [0] * self._nthreads
        
    def solve(self):     
        self._processes = []

        pool = ThreadPool(self._nthreads)
           
        print("Starting calculation")
        start_time = datetime.now()
        
        self._solutions = pool.map(self.nqueens, range(self._nthreads))
        
        script_time = datetime.now() - start_time
        
        pool.close() 
        pool.join()                 
        
        print("\nElapsed time: %d.%d" %(script_time.seconds, script_time.microseconds))
        print("\nThere are %d solutions for %d queens." %(sum(self._solutions), self._nq));    
        
        return script_time.seconds, script_time.microseconds, sum(self._solutions)
                        
    def nqueens(self, thr_index, col=0, depth=0):
        #print(thr_index)
        
        start = 0 if (col > 0) else int(thr_index * (self._nq / self._nthreads))
        end = self._nq - 1 if ((col > 0) or (thr_index == self._nthreads - 1)) else int((thr_index + 1) * (self._nq / self._nthreads) - 1)
        
        if (col == self._nq):                   # tried N queens permutations
            self._solution += 1     # peer found one solution
            
        # Backtracking - try next column on recursive call for current thd
        for i in range(start, end + 1):
            j = 0
            while(j < col and self.is_safe(i, j, col, thr_index)):
                j += 1
            if(j < col):
                continue
            
            self._queen_on[thr_index][col] = i
            self.nqueens(thr_index, col + 1, depth + 1)
            
        if(depth == 0):
            return self._solution
           
            
    def is_safe(self, i, j, col, thr_index):
        if (self._queen_on[thr_index][j] == i):
            return _its_safe
        
        if (abs(self._queen_on[thr_index][j] - i) == col - j):
            return _its_safe
        
        return _not_safe
    


def main(argv):
    if len(argv) < 3:
        queens = _num_queens
    else:
        queens = int(sys.argv[2])
        
    if len(argv) < 4:
        threads = _num_thread
    else:
        threads=int(argv[3])        
    
    if len(argv) < 5:
        repeat = 1000
    else:
        repeat = int(argv[4])
        
    if len(argv) < 2:
        print('please enter a file name')
    else:
        filename = str(sys.argv[1])
        
    nqueen_obj = nQueen(queens, threads)
    temp_obj = tempControl()
    
    with open(filename, "w") as myfile:
        myfile.write("time,queen,threads,solutions,seconds,microseconds,cpu_temp,gpu_temp\n")
        
    for i in (range(repeat)):
        print("Calculating loop number %s (of %s)" %(i+1, repeat))
        seconds, microseconds, solutions = nqueen_obj.solve()
        temp_cpu, temp_gpu = temp_obj.get_temp()
        now = datetime.now()
        now_epoch = now.strftime('%s')
        
        with open(filename, "a") as myfile:
            myfile.write("%s, %d, %d, %d, %d, %d, %.2f, %.2f\n" %(now_epoch, queens, threads, solutions, seconds, microseconds, temp_cpu, temp_gpu))

        print("%s, %d, %d, %d, %d, %d, %.2f, %.2f\n" %(now_epoch, queens, threads, solutions, seconds, microseconds, temp_cpu, temp_gpu))
        
if __name__ == "__main__":    
    main(sys.argv)

